from collections.abc import Mapping, Sequence
from typing import Callable, Union, cast

import scaluq
from numpy.typing import ArrayLike
from typing_extensions import assert_never



def scaluq_circuit_helper_function():
    print("helper function from scaluq/circuit")

_single_qubit_gate_scaluq: Mapping[
    Single
]