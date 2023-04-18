# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#      http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from abc import ABC
from collections.abc import Sequence

from quri_parts.circuit import GateSequence, UnboundParametricQuantumCircuitProtocol

from .state import GeneralCircuitQuantumState, QuantumState


class ParametricCircuitQuantumStateMixin(ABC):
    def __init__(
        self, n_qubits: int, circuit: UnboundParametricQuantumCircuitProtocol
    ) -> None:
        if circuit.qubit_count != n_qubits:
            raise ValueError(
                f"n_qubits={n_qubits} does not match with circuit.qubit_count="
                f"{circuit.qubit_count}"
            )
        self._circuit = circuit.freeze()

    @property
    def parametric_circuit(self) -> UnboundParametricQuantumCircuitProtocol:
        """Parametric circuit to build the quantum state."""
        return self._circuit


class ParametricCircuitQuantumState(ParametricCircuitQuantumStateMixin, QuantumState):
    r"""ParametricCircuitQuantumState represents a quantum state generated by
    applying a parametric circuit to \|00...0> state.

    This class holds an unbound parametric circuit, thus circuit
    parameters are not bound to concrete values. Use
    :meth:`~bind_parameters` when you need to bind concrete parameter
    values.
    """

    def __init__(
        self,
        n_qubits: int,
        circuit: UnboundParametricQuantumCircuitProtocol,
    ) -> None:
        ParametricCircuitQuantumStateMixin.__init__(self, n_qubits, circuit)
        self._n_qubits: int = n_qubits

    def __repr__(self) -> str:
        return "{}(n_qubits={}, circuit={})".format(
            self.__class__.__name__,
            self._n_qubits,
            self.parametric_circuit,
        )

    @property
    def qubit_count(self) -> int:
        return self._n_qubits

    def with_primitive_circuit(self) -> "ParametricCircuitQuantumState":
        """Returns a new ParametricCircuitQuantumState whose circuit is
        replaced with the corresponding primitive circuit.

        The original state is not changed. For details about the
        primitive circuit, please refer to `.primitive_circuit()` in
        :class:`UnboundParametricQuantumCircuitProtocol`.
        """
        return ParametricCircuitQuantumState(
            self._n_qubits, self._circuit.primitive_circuit()
        )

    def with_gates_applied(
        self, gates: GateSequence
    ) -> "ParametricCircuitQuantumState":
        """Returns a new state with the gates applied.

        The original state is not changed.
        """
        circuit = self.parametric_circuit.get_mutable_copy()
        circuit.extend(gates)
        return ParametricCircuitQuantumState(self._n_qubits, circuit)

    def bind_parameters(self, params: Sequence[float]) -> GeneralCircuitQuantumState:
        """Returns a new state with the circuit parameters assigned concrete
        values.

        This method does not modify self but returns a newly created
        state.
        """
        circuit = self.parametric_circuit.bind_parameters(params)
        return GeneralCircuitQuantumState(self._n_qubits, circuit)
