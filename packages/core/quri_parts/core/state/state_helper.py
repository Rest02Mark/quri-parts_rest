# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#      http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import TYPE_CHECKING, Optional, Union, overload

if TYPE_CHECKING:
    import numpy.typing as npt

from quri_parts.circuit import (
    NonParametricQuantumCircuit,
    UnboundParametricQuantumCircuitProtocol,
)

from . import ComputationalBasisState, GeneralCircuitQuantumState
from .state import CircuitQuantumState, QuantumState
from .state_parametric import ParametricCircuitQuantumState
from .state_vector import QuantumStateVector, StateVectorType
from .state_vector_parametric import ParametricQuantumStateVector


@overload
def apply_circuit(
    circuit: NonParametricQuantumCircuit,
    state: CircuitQuantumState,
) -> CircuitQuantumState:
    ...


@overload
def apply_circuit(
    circuit: NonParametricQuantumCircuit,
    state: QuantumStateVector,
) -> QuantumStateVector:
    ...


@overload
def apply_circuit(
    circuit: NonParametricQuantumCircuit,
    state: ParametricCircuitQuantumState,
) -> ParametricCircuitQuantumState:
    ...


@overload
def apply_circuit(
    circuit: NonParametricQuantumCircuit,
    state: ParametricQuantumStateVector,
) -> ParametricQuantumStateVector:
    ...


@overload
def apply_circuit(
    circuit: UnboundParametricQuantumCircuitProtocol,
    state: CircuitQuantumState,
) -> ParametricCircuitQuantumState:
    ...


@overload
def apply_circuit(
    circuit: UnboundParametricQuantumCircuitProtocol,
    state: QuantumStateVector,
) -> ParametricQuantumStateVector:
    ...


@overload
def apply_circuit(
    circuit: UnboundParametricQuantumCircuitProtocol,
    state: ParametricCircuitQuantumState,
) -> ParametricCircuitQuantumState:
    ...


@overload
def apply_circuit(
    circuit: UnboundParametricQuantumCircuitProtocol,
    state: ParametricQuantumStateVector,
) -> ParametricQuantumStateVector:
    ...


def apply_circuit(
    circuit: Union[
        NonParametricQuantumCircuit, UnboundParametricQuantumCircuitProtocol
    ],
    state: QuantumState,
) -> QuantumState:
    """Returns a new state with the circuit applied.

    The original state is not changed.
    """
    if isinstance(state, CircuitQuantumState):
        combined_circuit = state.circuit + circuit
        return quantum_state(state.qubit_count, circuit=combined_circuit)
    elif isinstance(state, QuantumStateVector):
        combined_circuit = state.circuit + circuit
        return quantum_state(
            state.qubit_count, vector=state.vector, circuit=combined_circuit
        )
    elif isinstance(state, ParametricCircuitQuantumState):
        combined_circuit = state.parametric_circuit + circuit
        return quantum_state(state.qubit_count, circuit=combined_circuit)
    elif isinstance(state, ParametricQuantumStateVector):
        combined_circuit = state.parametric_circuit + circuit
        return quantum_state(
            state.qubit_count, vector=state.vector, circuit=combined_circuit
        )
    else:
        raise ValueError(f"Unsupported state type: {state}")


@overload
def quantum_state(n_qubits: int) -> ComputationalBasisState:
    ...


@overload
def quantum_state(n_qubits: int, *, bits: int) -> ComputationalBasisState:
    ...


@overload
def quantum_state(
    n_qubits: int, *, bits: int, circuit: NonParametricQuantumCircuit
) -> GeneralCircuitQuantumState:
    ...


@overload
def quantum_state(
    n_qubits: int, *, circuit: NonParametricQuantumCircuit
) -> GeneralCircuitQuantumState:
    ...


@overload
def quantum_state(
    n_qubits: int, *, bits: int, circuit: UnboundParametricQuantumCircuitProtocol
) -> ParametricCircuitQuantumState:
    ...


@overload
def quantum_state(
    n_qubits: int, *, circuit: UnboundParametricQuantumCircuitProtocol
) -> ParametricCircuitQuantumState:
    ...


@overload
def quantum_state(
    n_qubits: int, *, vector: Union[StateVectorType, "npt.ArrayLike"]
) -> QuantumStateVector:
    ...


@overload
def quantum_state(
    n_qubits: int,
    *,
    vector: Union[StateVectorType, "npt.ArrayLike"],
    circuit: NonParametricQuantumCircuit,
) -> QuantumStateVector:
    ...


@overload
def quantum_state(
    n_qubits: int,
    *,
    vector: Union[StateVectorType, "npt.ArrayLike"],
    circuit: UnboundParametricQuantumCircuitProtocol,
) -> ParametricQuantumStateVector:
    ...


def quantum_state(
    n_qubits: int,
    *,
    vector: Optional[Union[StateVectorType, "npt.ArrayLike"]] = None,
    bits: int = 0,
    circuit: Optional[
        Union[NonParametricQuantumCircuit, UnboundParametricQuantumCircuitProtocol]
    ] = None,
) -> QuantumState:
    """Returns a quantum state generated by a given vector, bits, and a
    circuit.

    Raises ValueError if both a vector and bits input at the same time.
    """
    if vector is None:
        cb_state = ComputationalBasisState(n_qubits, bits=bits)
        if circuit is None:
            return cb_state
        else:
            comb_circuit = cb_state.circuit + circuit
            return _circuit_quantum_state(n_qubits, comb_circuit)
    if bits != 0:
        raise ValueError("vector and bits cannot input at the same time")
    return _quantum_state_vector(n_qubits, vector, circuit)


def _circuit_quantum_state(
    n_qubits: int,
    circuit: Union[
        NonParametricQuantumCircuit, UnboundParametricQuantumCircuitProtocol
    ],
) -> QuantumState:
    if isinstance(circuit, NonParametricQuantumCircuit):
        return ComputationalBasisState(n_qubits, bits=0).with_gates_applied(circuit)
    else:
        return ParametricCircuitQuantumState(n_qubits, circuit)


def _quantum_state_vector(
    n_qubits: int,
    vector: Union[StateVectorType, "npt.ArrayLike"],
    circuit: Optional[
        Union[NonParametricQuantumCircuit, UnboundParametricQuantumCircuitProtocol]
    ] = None,
) -> QuantumState:
    if circuit is None or isinstance(circuit, NonParametricQuantumCircuit):
        return QuantumStateVector(n_qubits, vector=vector, circuit=circuit)
    else:
        return ParametricQuantumStateVector(n_qubits, vector=vector, circuit=circuit)
