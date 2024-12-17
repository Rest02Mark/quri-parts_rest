import json
from cmath import phase
from collections.abc import Mapping

import numpy as np

from scaluq import Circuit as scaluqQuantumCircuit

from quri_parts.circuit import ImmutableQuantumCircuit as NPQC
from quri_parts.circuit import (
    PauliRotation,
    QuantumCircuit,
    QuantumGate,
    UnitaryMatrix,
    gate_names,
)
from quri_parts.circuit.gate_names import (
    MultiQubitGateNameType,
    SingleQubitGateNameType,
    TwoQubitGateNameType,
)

_single_qubit_gate_scaluq_quri_parts: Mapping[str, SingleQubitGateNameType] = {
    "I": gate_names.Identity,
    "X": gate_names.X,
    "Y": gate_names.Y,
    "Z": gate_names.Z,
    "H": gate_names.H,
    "S": gate_names.S,
    "Sdag": gate_names.Sdag,
    "T": gate_names.T,
    "Tdag": gate_names.Tdag,
    "sqrtX": gate_names.SqrtX,
    "sqrtXdag": gate_names.SqrtXdag,
    "sqrtY": gate_names.SqrtY,
    "sqrtYdag": gate_names.SqrtYdag,
}

#TODO 確認
_single_qubit_rotation_gate_scaluq_quri_parts: Mapping[str, SingleQubitGateNameType] = {
    "RX": gate_names.RX,
    "RY": gate_names.RY,
    "RZ": gate_names.RZ,
}

_two_qubit_gate_scaluq_quri_parts: Mapping[str, TwoQubitGateNameType] = {
    "CNOT": gate_names.CNOT,
    "CZ": gate_names.CZ,
    "SWAP": gate_names.SWAP,
}
