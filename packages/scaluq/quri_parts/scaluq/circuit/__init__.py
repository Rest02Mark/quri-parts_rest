from collections.abc import Mapping, Sequence
from typing import Callable, Union, cast

import scaluq
import numpy as np
from numpy.typing import ArrayLike
from typing_extensions import assert_never

from quri_parts.circuit import (
    ImmutableLinearMappedParametricQuantumCircuit,
    ImmutableParametricQuantumCircuit,
    ImmutableQuantumCircuit,
    ParametricQuantumCircuitProtocol,
    QuantumGate,
    gate_names,
)

from quri_parts.rust.circuit.noise import NoiseModel

from quri_parts.circuit.gate_names import (
    MultiQubitGateNameType,
    SingleQubitGateNameType,
    ThreeQubitGateNameType,
    TwoQubitGateNameType,
    is_gate_name,
    is_multi_qubit_gate_name,
    is_parametric_gate_name,
    is_single_qubit_gate_name,
    is_three_qubit_gate_name,
    is_two_qubit_gate_name,
    is_unitary_matrix_gate_name,
)

from .. import cast_to_list

def scaluq_circuit_helper_function():
    print("helper function from scaluq/circuit")

_single_qubit_gate_scaluq_f32: Mapping[
    SingleQubitGateNameType, Callable[[int], scaluq.f32.Gate]
] = {
    gate_names.Identity: scaluq.f32.gate.I,
    gate_names.X: scaluq.f32.gate.X,
    gate_names.Y: scaluq.f32.gate.Y,
    gate_names.Z: scaluq.f32.gate.Z,
    gate_names.H: scaluq.f32.gate.H,
    gate_names.S: scaluq.f32.gate.S,
    gate_names.Sdag: scaluq.f32.gate.Sdag,
    gate_names.SqrtX: scaluq.f32.gate.SqrtX,
    gate_names.SqrtXdag: scaluq.f32.gate.SqrtXdag,
    gate_names.SqrtY: scaluq.f32.gate.SqrtY,
    gate_names.SqrtYdag: scaluq.f32.gate.SqrtYdag,
    gate_names.T: scaluq.f32.gate.T,
    gate_names.Tdag: scaluq.f32.gate.Tdag,
}

_single_qubit_gate_scaluq_f64: Mapping[
    SingleQubitGateNameType, Callable[[int], scaluq.f64.Gate]
] = {
    gate_names.Identity: scaluq.f64.gate.I,
    gate_names.X: scaluq.f64.gate.X,
    gate_names.Y: scaluq.f64.gate.Y,
    gate_names.Z: scaluq.f64.gate.Z,
    gate_names.H: scaluq.f64.gate.H,
    gate_names.S: scaluq.f64.gate.S,
    gate_names.Sdag: scaluq.f64.gate.Sdag,
    gate_names.SqrtX: scaluq.f64.gate.SqrtX,
    gate_names.SqrtXdag: scaluq.f64.gate.SqrtXdag,
    gate_names.SqrtY: scaluq.f64.gate.SqrtY,
    gate_names.SqrtYdag: scaluq.f64.gate.SqrtYdag,
    gate_names.T: scaluq.f64.gate.T,
    gate_names.Tdag: scaluq.f64.gate.Tdag,
}
#TODO 
#contorolsいらないはず、確認
def _u1_gate_scaluq_f32(gate: QuantumGate) -> scaluq.f32.Gate:
    return cast(
        scaluq.f32.Gate,
        scaluq.f32.gate.U1(*gate.target_indices, *gate.params),
    )

def _u1_gate_scaluq_f64(gate: QuantumGate) -> scaluq.f64.Gate:
    return cast(
        scaluq.f64.Gate,
        scaluq.f64.gate.U1(*gate.target_indices, *gate.params),
    )

def _u2_gate_scaluq_f32(gate: QuantumGate) -> scaluq.f32.Gate:
    return cast(
        scaluq.f32.Gate,
        scaluq.f32.gate.U2(*gate.target_indices, *gate.params),
    )

def _u2_gate_scaluq_f64(gate: QuantumGate) -> scaluq.f64.Gate:
    return cast(
        scaluq.f64.Gate,
        scaluq.f64.gate.U2(*gate.target_indices, *gate.params),
    )

def _u3_gate_scaluq_f32(gate: QuantumGate) -> scaluq.f32.Gate:
    return cast(
        scaluq.f32.Gate,
        scaluq.f32.gate.U3(*gate.target_indices, *gate.params),
    )

def _u3_gate_scaluq_f64(gate: QuantumGate) -> scaluq.f64.Gate:
    return cast(
        scaluq.f64.Gate,
        scaluq.f64.gate.U3(*gate.target_indices, *gate.params),
    )

_single_qubit_reverse_rotation_gate_scaluq_f32: Mapping[
    SingleQubitGateNameType, Callable[[int, float], scaluq.f32.Gate]
] = {
    gate_names.RX: scaluq.f32.gate.RX,
    gate_names.RY: scaluq.f32.gate.RY,
    gate_names.RZ: scaluq.f32.gate.RZ,
}

_single_qubit_reverse_rotation_gate_scaluq_f64: Mapping[
    SingleQubitGateNameType, Callable[[int, float], scaluq.f64.Gate]
] = {
    gate_names.RX: scaluq.f64.gate.RX,
    gate_names.RY: scaluq.f64.gate.RY,
    gate_names.RZ: scaluq.f64.gate.RZ,
}

_two_qubit_gate_scaluq_f32: Mapping[
    TwoQubitGateNameType, Callable[[int, int], scaluq.f32.Gate]
] = {
    gate_names.CNOT: scaluq.f32.gate.CX,
    gate_names.CZ: scaluq.f32.gate.CZ,
    gate_names.SWAP: scaluq.f32.gate.Swap,
}

_two_qubit_gate_scaluq_f64: Mapping[
    TwoQubitGateNameType, Callable[[int, int], scaluq.f64.Gate]
] = {
    gate_names.CNOT: scaluq.f64.gate.CX,
    gate_names.CZ: scaluq.f64.gate.CZ,
    gate_names.SWAP: scaluq.f64.gate.Swap,
}

_three_qubit_gate_scaluq_f32: Mapping[
    ThreeQubitGateNameType, Callable[[int, int, int], scaluq.f32.Gate]
] = {
    gate_names.TOFFOLI: scaluq.f32.gate.Toffoli,
}

_three_qubit_gate_scaluq_f64: Mapping[
    ThreeQubitGateNameType, Callable[[int, int, int], scaluq.f64.Gate]
] = {
    gate_names.TOFFOLI: scaluq.f64.gate.Toffoli,
}

_multi_pauli_gate_scaluq_f32: Mapping[
    #MultiQubitGateNameType, Callable[[list[int], list[int]], scaluq.f32.Gate]
    MultiQubitGateNameType, Callable[[scaluq.f32.PauliOperator], scaluq.f32.Gate]
] = {
    gate_names.Pauli: scaluq.f32.gate.Pauli,
}

_multi_pauli_gate_scaluq_f64: Mapping[
    #MultiQubitGateNameType, Callable[[list[int], list[int]], scaluq.f64.Gate]
    MultiQubitGateNameType, Callable[[scaluq.f64.PauliOperator], scaluq.f64.Gate]
] = {
    gate_names.Pauli: scaluq.f64.gate.Pauli,
}

_multi_pauli_rotation_gate_scaluq_f32: Mapping[
    MultiQubitGateNameType, Callable[[list[int], list[int], float], scaluq.f32.Gate]
] = {
    gate_names.PauliRotation: scaluq.f32.gate.PauliRotation,
}

_multi_pauli_rotation_gate_scaluq_f64: Mapping[
    MultiQubitGateNameType, Callable[[list[int], list[int], float], scaluq.f64.Gate]
] = {
    gate_names.PauliRotation: scaluq.f64.gate.PauliRotation,
}

_parametric_gate_scaluq_f32 = {
    gate_names.ParametricRX: scaluq.f32.gate.ParamRX,
    gate_names.ParametricRY: scaluq.f32.gate.ParamRY,
    gate_names.ParametricRZ: scaluq.f32.gate.ParamRZ,
    gate_names.ParametricPauliRotation: scaluq.f32.gate.ParamPauliRotation,
}

_parametric_gate_scaluq_f64 = {
    gate_names.ParametricRX: scaluq.f64.gate.ParamRX,
    gate_names.ParametricRY: scaluq.f64.gate.ParamRY,
    gate_names.ParametricRZ: scaluq.f64.gate.ParamRZ,
    gate_names.ParametricPauliRotation: scaluq.f64.gate.ParamPauliRotation,
}


def _dense_matrix_gate_scaluq_f32(
        targets: Union[int, Sequence[int]], unitary_matrix: ArrayLike
) -> scaluq.f32.Gate:
    #tuple to list
    targets = list(targets)
    unitary_matrix = np.array(unitary_matrix, dtype=np.complex64)
    return scaluq.f32.gate.DenseMatrix(targets,unitary_matrix)


def convert_gate_f32(
        gate: QuantumGate,
) -> scaluq.f32.Gate:
    print("in convert_gate_f32 and gate.name is ", gate.name)
    if not is_gate_name(gate.name):
        raise ValueError(f"Unknown gate name: {gate.name}")
    
    if is_single_qubit_gate_name(gate.name):
        if gate.name in _single_qubit_gate_scaluq_f32:
            return _single_qubit_gate_scaluq_f32[gate.name](
                *gate.target_indices, *gate.params
            )
        elif gate.name == gate_names.U1:
            return _u1_gate_scaluq_f32(gate)
        elif gate.name == gate_names.U2:
            return _u2_gate_scaluq_f32(gate)
        elif gate.name == gate_names.U3:
            return _u3_gate_scaluq_f32(gate)
        elif gate.name in _single_qubit_reverse_rotation_gate_scaluq_f32:
            return _single_qubit_reverse_rotation_gate_scaluq_f32[gate.name](
                *gate.target_indices, *gate.params
            )
        else:
            assert False, "Unreachable"
    elif is_two_qubit_gate_name(gate.name):
        return _two_qubit_gate_scaluq_f32[gate.name](
            *gate.target_indices, *gate.target_indices
        )
    elif is_three_qubit_gate_name(gate.name):
        return _three_qubit_gate_scaluq_f32[gate.name](
            *gate.target_indices, *gate.target_indices, *gate.target_indices
        )
    elif is_multi_qubit_gate_name(gate.name):
        target_indices = cast_to_list(gate.target_indices)
        pauli_ids = cast_to_list(gate.pauli_ids)
        if gate.name in _multi_pauli_gate_scaluq_f32:
            pauli = scaluq.f32.PauliOperator(target_indices, pauli_ids)
            return _multi_pauli_gate_scaluq_f32[gate.name](pauli)
        
    elif is_unitary_matrix_gate_name(gate.name):
        return _dense_matrix_gate_scaluq_f32(gate.target_indices, gate.unitary_matrix)
    
    elif is_parametric_gate_name(gate.name):
        #TODO とりあえず、qulacsと同様に未対応とする
        raise ValueError("Parametric gates are not supported")
    else:
        assert False, "Unreachable"

    

def convert_circuit_f32(
        circuit: ImmutableQuantumCircuit
        ) -> scaluq.f32.Circuit:
    scaluq_f32_circuit = scaluq.f32.Circuit(circuit.qubit_count)

    for gate in circuit.gates:
        #print(convert_gate_f32(gate))
        scaluq_f32_circuit.add_gate(convert_gate_f32(gate))

    print("convert end f32.")
        
    return scaluq_f32_circuit

#TODO
"""
def convert_parametric_circuit_f32(
        circuit: ParametricQuantumCircuitProtocol,
) -> tuple[
    scaluq.f32.
]
"""

#TODO atode kesu
def kakunin(circuit: ImmutableQuantumCircuit) -> None:
    print("qubit: ",circuit.qubit_count)
    print("gate: ",circuit.gates)
    print("depth: ",circuit.depth)
    print("cbit", circuit.cbit_count)

#TODO
#def convert_circuit_with_noise_model( 


#TODO
#__all__ = []
        
