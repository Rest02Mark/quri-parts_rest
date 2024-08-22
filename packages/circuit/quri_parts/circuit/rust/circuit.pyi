from typing import Optional, Sequence, Union

from .gate import QuantumGate

GateSequence = Union[ImmutableQuantumCircuit, Sequence[QuantumGate]]

class ImmutableQuantumCircuit:
    def __new__(
        cls, circuit: "ImmutableQuantumCircuit"
    ) -> "ImmutableQuantumCircuit": ...
    def __eq__(self, other: object) -> bool: ...
    @property
    def qubit_count(self) -> int: ...
    @property
    def cbit_count(self) -> int: ...
    @property
    def gates(self) -> Sequence[QuantumGate]: ...
    @property
    def depth(self) -> int: ...
    def combine(self, gates: GateSequence) -> "QuantumCircuit": ...
    def __add__(self, gates: GateSequence) -> "QuantumCircuit": ...
    def freeze(self) -> "ImmutableQuantumCircuit": ...
    def get_mutable_copy(self) -> "QuantumCircuit": ...

class QuantumCircuit(ImmutableQuantumCircuit):
    def __new__(
        cls, qubit_count: int, cbit_count: int = 0, gates: Sequence[QuantumGate] = []
    ) -> "QuantumCircuit": ...
    def add_gate(self, gate: QuantumGate, gate_index: Optional[int] = None) -> None: ...
    def extend(self, gates: GateSequence) -> None: ...
    def __iadd__(self, gates: GateSequence) -> "QuantumCircuit": ...
    def add_Identity_gate(self, qubit_index: int) -> None: ...
    def add_X_gate(self, qubit_index: int) -> None: ...
    def add_Y_gate(self, qubit_index: int) -> None: ...
    def add_Z_gate(self, qubit_index: int) -> None: ...
    def add_H_gate(self, qubit_index: int) -> None: ...
    def add_S_gate(self, qubit_index: int) -> None: ...
    def add_Sdag_gate(self, qubit_index: int) -> None: ...
    def add_SqrtX_gate(self, qubit_index: int) -> None: ...
    def add_SqrtXdag_gate(self, qubit_index: int) -> None: ...
    def add_SqrtY_gate(self, qubit_index: int) -> None: ...
    def add_SqrtYdag_gate(self, qubit_index: int) -> None: ...
    def add_T_gate(self, qubit_index: int) -> None: ...
    def add_Tdag_gate(self, qubit_index: int) -> None: ...
    def add_U1_gate(self, qubit_index: int, lmd: float) -> None: ...
    def add_U2_gate(self, qubit_index: int, phi: float, lmd: float) -> None: ...
    def add_U3_gate(
        self, qubit_index: int, theta: float, phi: float, lmd: float
    ) -> None: ...
    def add_RX_gate(self, qubit_index: int, angle: float) -> None: ...
    def add_RY_gate(self, qubit_index: int, angle: float) -> None: ...
    def add_RZ_gate(self, qubit_index: int, angle: float) -> None: ...
    def add_CNOT_gate(self, control_index: int, target_index: int) -> None: ...
    def add_CZ_gate(self, control_index: int, target_index: int) -> None: ...
    def add_SWAP_gate(self, target_index1: int, target_index2: int) -> None: ...
    def add_TOFFOLI_gate(
        self, control_index1: int, control_index2: int, target_index: int
    ) -> None: ...
    def add_UnitaryMatrix_gate(
        self,
        target_indices: Sequence[int],
        unitary_matrix: Sequence[Sequence[complex]],
    ) -> None: ...
    def add_SingleQubitUnitaryMatrix_gate(
        self,
        target_index: int,
        unitary_matrix: Sequence[Sequence[complex]],
    ) -> None: ...
    def add_TwoQubitUnitaryMatrix_gate(
        self,
        target_index1: int,
        target_index2: int,
        unitary_matrix: Sequence[Sequence[complex]],
    ) -> None: ...
    def add_Pauli_gate(
        self, target_indices: Sequence[int], pauli_ids: Sequence[int]
    ) -> None: ...
    def add_PauliRotation_gate(
        self,
        target_qubits: Sequence[int],
        pauli_id_list: Sequence[int],
        angle: float,
    ) -> None: ...
    def measure(
        self,
        qubit_indices: Union[int, Sequence[int]],
        classical_indices: Union[int, Sequence[int]],
    ) -> None: ...
