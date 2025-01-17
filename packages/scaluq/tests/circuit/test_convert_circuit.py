# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#      http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections.abc import Mapping
from typing import Callable, cast

import numpy as np
import scaluq

from quri_parts.circuit import (
    LinearMappedParametricQuantumCircuit,
    ParametricQuantumCircuit,
    QuantumCircuit,
    QuantumGate,
    gates,
)

from quri_parts.circuit.transpile import (
    SingleQubitUnitaryMatrix2RYRZTranspiler,
    TwoQubitUnitaryMatrixKAKTranspiler,
)

import sys
sys.path.append("/home/rest/baito/quri-parts/packages/scaluq")
#import

from quri_parts.scaluq.circuit import (
    scaluq_circuit_helper_function,
    convert_circuit_f32,
    convert_gate_f32
)

def a():
    scaluq_circuit_helper_function()

#a()

def helper():
    print("helper: test_convert_circuit.py")

def gates_equal_f32(g1: scaluq.f32.Gate, g2: scaluq.f32.Gate) -> bool:
    def gate_info(
            g: scaluq.f32.Gate,
    ) -> tuple[str,list[int],list[int]]:
        return (
            g.gate_type(),
            g.target_qubit_list(),
            g.control_qubit_list(),
        )
    
    return (gate_info(g1) == gate_info(g2)) and cast(
        bool, np.all(g1.get_matrix() == g2.get_matrix())
    )

single_qubit_gate_mapping_f32: Mapping[
    Callable[[int], QuantumGate], Callable[[int], scaluq.f32.Gate]
] = {
    gates.Identity: scaluq.f32.gate.I,
    gates.X: scaluq.f32.gate.X,
    gates.Y: scaluq.f32.gate.Y,
    gates.Z: scaluq.f32.gate.Z,
    gates.H: scaluq.f32.gate.H,
    gates.S: scaluq.f32.gate.S,
    gates.Sdag: scaluq.f32.gate.Sdag,
    gates.SqrtX: scaluq.f32.gate.SqrtX,
    gates.SqrtXdag: scaluq.f32.gate.SqrtXdag,
    gates.SqrtY: scaluq.f32.gate.SqrtY,
    gates.SqrtYdag: scaluq.f32.gate.SqrtYdag,
    gates.T: scaluq.f32.gate.T,
    gates.Tdag: scaluq.f32.gate.Tdag,
}


def test_convert_single_qubit_gate_f32() -> None:
    for qp_fac, sq_gate in single_qubit_gate_mapping_f32.items():
        #TODO I のみtargetを引数として受け取らないようになっている　確認
        g = qp_fac(7)
        if g.name == "Identity":
            continue
        print("g: ", g)
        converted = convert_gate_f32(g)
        expected = sq_gate(7)
        assert gates_equal_f32(converted, expected)

two_qubit_gate_mapping_f32: Mapping[
    Callable[[int,int],QuantumGate],Callable[[int,int],scaluq.f32.Gate]
] = {
    gates.CNOT: scaluq.f32.gate.CX,
    gates.SWAP: scaluq.f32.gate.Swap,
    gates.CZ: scaluq.f32.gate.CZ,
}

def test_convert_two_qubit_gate_f32() -> None:
    for qp_fac, sq_gate in two_qubit_gate_mapping_f32.items():
        g = qp_fac(11, 7)
        print("g: ", g)
        converted = convert_gate_f32(g)
        expected = sq_gate(11, 7)
        assert gates_equal_f32(converted, expected)

three_qubit_gate_mapping_f32: Mapping[
    Callable[[int,int,int],QuantumGate],
    Callable[[int,int,int],scaluq.f32.Gate]
] = {
    gates.TOFFOLI: scaluq.f32.gate.Toffoli,
}

def test_convert_three_qubit_gate_f32() -> None:
    for qp_fac, sq_gate in three_qubit_gate_mapping_f32.items():
        g = qp_fac(11, 7, 5)
        print("g: ", g)
        converted = convert_gate_f32(g)
        expected = sq_gate(11, 7, 5)
        assert gates_equal_f32(converted, expected)

rotation_gate_mapping_f32: Mapping[
    Callable[[int,float],QuantumGate],Callable[[int,float],scaluq.f32.Gate]
] = {
    gates.RX: scaluq.f32.gate.RX,
    gates.RY: scaluq.f32.gate.RY,
    gates.RZ: scaluq.f32.gate.RZ,
}

#TODO
def test_convert_rotation_gate_f32() -> None:
    for qp_fac, sq_gate in rotation_gate_mapping_f32.items():
        g = qp_fac(7, 0.125)
        converted = convert_gate_f32(g)
        expercted = sq_gate(7, 0.125)
        assert gates_equal_f32(converted, expercted)   