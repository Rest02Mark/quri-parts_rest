from collections.abc import Mapping, Sequence
from typing import Callable, Union, cast

import scaluq
from numpy.typing import ArrayLike
from typing_extensions import assert_never

from quri_parts.circuit import (
    ImmutableLinearMappedParametricQuantumCircuit,
    ImmutableParametricQuantumCircuit,
    ParametricQuantumCircuitProtocol,
    QuantumGate,
    gate_names,
)
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
#TODO
#from quri_parts.rust.qulacs import convert_circuit

from .. import cast_to_list
from .compiled_circuit import compile_circuit, compile_parametric_circuit
#TODO
#from .qulacs_circuit_converter import circuit_from_qulacs

def scaluq_circuit_helper_function():
    print("helper function from scaluq/circuit")

#TODO gatebase?
_single_qubit_gate_scaluq_f32: Mapping[
    SingleQubitGateNameType, Callable[[int], qulacs.QuantumGateBase]
] = {
    gate_names.Identity: scaluq.f32.gate.Identity,
    gate_names.X: scaluq.f32.gate.X,
    gate_names.Y: scaluq.f32.gate.Y,
    gate_names.Z: scaluq.f32.gate.Z,
    gate_names.H: scaluq.f32.gate.H,
    gate_names.S: scaluq.f32.gate.S,
    gate_names.Sdag: scaluq.f32.gate.Sdag,
    gate_names.SqrtX: scaluq.f32.gate.sqrtX,
    gate_names.SqrtXdag: scaluq.f32.gate.sqrtXdag,
    gate_names.SqrtY: scaluq.f32.gate.sqrtY,
    gate_names.SqrtYdag: scaluq.f32.gate.sqrtYdag,
    gate_names.T: scaluq.f32.gate.T,
    gate_names.Tdag: scaluq.f32.gate.Tdag,
}

_single_qubit_gate_scaluq_f64: Mapping[
