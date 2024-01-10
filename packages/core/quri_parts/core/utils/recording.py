# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#      http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This module provides features of recording and logging intermediate data
from inside functions."""

import logging
import threading
from collections.abc import Callable, Hashable, Iterable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import IntEnum
from functools import update_wrapper
from typing import Any, NamedTuple, Optional, Protocol, TypeVar, cast

from typing_extensions import Concatenate, ParamSpec, TypeAlias


class RecordLevel(IntEnum):
    """Level of recording, which specifies importance of a recording event.

    A larger value means higher importance. Record level is a concept
    similar to :py:mod:`logging` level. Currently each record level has
    its counterpart :py:mod:`logging` level with the same integer value.
    """

    INFO = 20
    DEBUG = 10

    def __str__(self) -> str:
        return self.name


#: INFO level
INFO = RecordLevel.INFO
#: DEBUG level
DEBUG = RecordLevel.DEBUG


P = ParamSpec("P")
R = TypeVar("R", covariant=True)


class RecordableFunctionId(NamedTuple):
    """Represents an identifier for a recordable function."""

    #: Name of the module which the function belongs to.
    module: str
    #: Qualified name of the function.
    qualname: str
    #: Other parameters necessary for identifying a function. It is currently unused.
    param: Hashable

    def to_str(self, full: bool = True) -> str:
        """Returns a string representation of itself.

        If ``full`` is True, the returned string contains the module
        name.
        """
        if full:
            base = f"{self.module}.{self.qualname}"
        else:
            base = self.qualname
        if self.param:
            return f"{base}<{str(self.param)}>"
        else:
            return base

    def __str__(self) -> str:
        return self.to_str()


class RecordableFunction(Protocol[P, R]):
    """Represents an instance of a recordable function with its identifier,
    which can be accessed via :attr:`id` attribute."""

    id: RecordableFunctionId

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        ...


def recordable(f: Callable[Concatenate["Recorder", P], R]) -> RecordableFunction[P, R]:
    """A decorator for creating a recordable function.

    A function to which this decorator is applied must receive a
    :class:`Recorder` as its first positional argument, which can be
    used for recording in the function body. This decorator removes the
    :class:`Recorder` argument, so a user of the recordable function
    does not need to pass a :class:`Recorder` instance. This decorator
    also adds a :class:`RecordableFunctionId`, which can be accesed via
    :attr:`id` attribute.

    Note that when you store mutable data such as list, `RecordEntry`
    does not store the snapshot of the data. This means that the data
    you get is the latest one when you access it. If you want to get
    the snapshot of the data, you need to copy it by yourself.
    """
    # Currently `param` is an empty tuple. But we may add support for it in the future.
    param = ()
    f_id = RecordableFunctionId(f.__module__, f.__qualname__, param)

    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        recorder = _get_recorder(f_id)
        with recorder.start_func():
            return f(recorder, *args, **kwargs)

    wrapper = cast(RecordableFunction[P, R], wrapper)
    wrapper.id = f_id
    return update_wrapper(wrapper, f)


_DEFAULT_LOGGER_NAME = f"{logging.Logger.root.name}.quri_parts_recording"

_RecKey: TypeAlias = Hashable
_RecValue: TypeAlias = Any
_RecData: TypeAlias = tuple[_RecKey, _RecValue]


class Recorder:
    """Data recorder given to the function which uses data to record.

    For the function generated by :func:`recordable`, each function call
    starts with calling :meth:`start_func`, which creates a new
    :class:`RecordGroup` for the function. Note that you should first create
    :class:`RecordSession` to record the data.
    """

    def __init__(self, fid: RecordableFunctionId) -> None:
        self._func_id = fid

    @contextmanager
    def start_func(self) -> Iterator[None]:
        """Context manager to be called for each :class:`RecordableFunction`
        call."""
        for session in _active_sessions:
            session._enter_func(self._func_id)
        yield
        for session in _active_sessions:
            session._exit_func(self._func_id)

    def record(self, level: RecordLevel, key: _RecKey, value: _RecValue) -> None:
        r"""Records the given data to :class:`RecordGroup`\ s which belong to active
        :class:`RecordSession`\ s."""
        for session in _active_sessions:
            if session.is_enabled_for(level, self._func_id):
                session.handler(level, self._func_id, key, value)

    def debug(self, key: _RecKey, value: _RecValue) -> None:
        """Records the given data with `DEBUG` level."""
        self.record(DEBUG, key, value)

    def info(self, key: _RecKey, value: _RecValue) -> None:
        """Records the given data with `INFO` level."""
        self.record(INFO, key, value)

    def is_enabled_for(self, level: RecordLevel) -> bool:
        """Checks if there is any active :class:`RecordSession` which records
        the data with `level` or lower."""
        return any(
            session.is_enabled_for(level, self._func_id) for session in _active_sessions
        )


_recorders: dict[RecordableFunctionId, Recorder] = {}


def _get_recorder(fid: RecordableFunctionId) -> Recorder:
    """Returns :class:`Recorder` corresponding to the `fid`"""
    if fid in _recorders:
        return _recorders[fid]
    else:
        recorder = Recorder(fid)
        _recorders[fid] = recorder
        return recorder


@dataclass
class RecordEntry:
    """Represents a record data entry with its :class:`RecordLevel` and
    :class:`RecordableFunctionId`."""

    level: RecordLevel
    func_id: RecordableFunctionId
    data: _RecData

    def __str__(self) -> str:
        return f"{self.level}:{self.func_id}:{self.data}"


_group_id = threading.local()
_group_id.current = 0


def _next_group_id() -> int:
    id: int = _group_id.current
    _group_id.current += 1
    return id


@dataclass
class RecordGroup:
    r"""Represents a group of data, which contains the list of
    :class:`RecordEntry`\ s with :class:`RecordableFunctionId`. This group is created
    for every :class:`RecordableFunction` calls.
    """

    func_id: RecordableFunctionId
    entries: list[RecordEntry]
    id: int = field(default_factory=_next_group_id)

    def add_entry(self, entry: RecordEntry) -> None:
        """Adds entry to the group."""
        self.entries.append(entry)

    def __str__(self) -> str:
        return (
            f"""RecordGroup(
  func_id: {self.func_id},
  entries: [
"""
            + "\n".join(f"    {entry}," for entry in self.entries)
            + """
  ]
)"""
        )


class RecordSet:
    """Set of :class:`RecordGroup` stored in sequence."""

    def __init__(self) -> None:
        self._history: list[RecordGroup] = []

    def add_group(self, fid: RecordableFunctionId) -> RecordGroup:
        """Creates and adds a :class:`RecordGroup` for given
        :class:`RecordableFunctionId`."""
        group = RecordGroup(fid, [])
        self._history.append(group)
        return group

    def remove_last_group(self) -> None:
        r"""Remove the last group from the sequence of
        :class:`RecordGroup`\ s."""
        self._history.pop()

    def get_history(self, func: RecordableFunction[P, R]) -> Iterable[RecordGroup]:
        r"""Returns the :class:`RecordGroup`\ s corresponding to the
        :class:`RecordableFunction` as an Iterable."""
        return filter(lambda g: g.func_id == func.id, self._history)


def _to_logging_level(level: RecordLevel) -> int:
    # Each RecordLevel has the same value as a logging level at least at the moment
    return level.value


class RecordSession:
    """A session manages data recording from recordable functions.

    It internally stores recording data received from recordable
    functions. It also calls associated loggers when receiving data
    recording events.
    """

    def __init__(self) -> None:
        self._levels: dict[RecordableFunctionId, RecordLevel] = {}
        self._record_set = RecordSet()
        self._group_stack: list[RecordGroup] = []
        self._loggers: set[logging.Logger] = set()

    def set_level(self, level: RecordLevel, func: RecordableFunction[P, R]) -> None:
        """Set a record level for the specified recordable function in this
        session."""
        self._levels[func.id] = level

    def is_enabled_for(self, level: RecordLevel, fid: RecordableFunctionId) -> bool:
        """Checks if recording of the given level is enabled for the specified
        recordable function in this session.

        Returns true if the record level set for the function is equal
        to or smaller than given `level`.
        """
        return fid in self._levels and level >= self._levels[fid]

    def handler(
        self,
        level: RecordLevel,
        fid: RecordableFunctionId,
        key: _RecKey,
        value: _RecValue,
    ) -> None:
        """Handles a data recording event.

        Internally, a :class:`RecordEntry` for the event is created and
        loggers associated with the session are invoked.
        """
        entry = RecordEntry(level, fid, (key, value))
        group = self._group_stack[-1]
        group.add_entry(entry)
        self._log(entry, group)

    def _log(self, entry: RecordEntry, group: RecordGroup) -> None:
        log_level = _to_logging_level(entry.level)
        msg = ""
        for logger in self._loggers:
            if not logger.isEnabledFor(log_level):
                continue
            if not msg:
                k, v = entry.data
                msg = f"{entry.func_id.to_str(False)}: {k}={v}"
            logger.getChild(entry.func_id.module).log(
                log_level, msg, extra={"record_group": group.id}
            )

    @contextmanager
    def start(self) -> Iterator[None]:
        """Starts the data recording session."""
        _active_sessions.append(self)
        yield
        _active_sessions.pop()

    def _enter_func(self, fid: RecordableFunctionId) -> None:
        """A hook called on invocation of a recordable function.

        Internally it creates and pushes a new record group for the
        specified function.
        """
        group = self._record_set.add_group(fid)
        self._group_stack.append(group)

    def _exit_func(self, fid: RecordableFunctionId) -> None:
        """A hook called on exit of a recordable function.

        Internally it pops the record group for the specified function.
        """
        group = self._group_stack.pop()
        if not group.entries:
            self._record_set.remove_last_group()

    def get_records(self) -> RecordSet:
        """Returns all the records saved in the session."""
        return self._record_set

    def add_logger(self, logger: Optional[logging.Logger] = None) -> None:
        """Connect a logger which logs data recording events received by the
        session."""

        if logger is None:
            logger = logging.getLogger(_DEFAULT_LOGGER_NAME)
        self._loggers.add(logger)


_active_sessions: list[RecordSession] = []
