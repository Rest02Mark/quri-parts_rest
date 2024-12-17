from math import pi
from quri_parts.circuit import QuantumCircuit

# A circuit with 4 qubits
circuit = QuantumCircuit(4)
circuit.add_X_gate(0)
circuit.add_H_gate(1)
circuit.add_Y_gate(2)
circuit.add_CNOT_gate(1, 2)
circuit.add_RX_gate(3, pi/4)

from quri_parts.qulacs.sampler import create_qulacs_vector_sampler

# Create the sampler
sampler = create_qulacs_vector_sampler()
sampling_result = sampler(circuit, shots=1000)
print(sampling_result)

import numpy as np
from quri_parts.core.operator import pauli_label, Operator, PAULI_IDENTITY

# 演算子の定義
op1 = Operator({
    pauli_label("X0 Y1"): 2,
    pauli_label("Z0 Y1"): 2j,
    PAULI_IDENTITY: 8,
})
op2 = pauli_label("X0 Y1 Z3")
op3 = pauli_label("X0 X1 X3")

from quri_parts.core.state import quantum_state
from quri_parts.circuit import QuantumCircuit, X, CNOT, H

n_qubits = 4  # 量子ビット数

# 量子状態の定義
state1 = quantum_state(
    n_qubits, circuit=QuantumCircuit(n_qubits, gates=[X(0), H(1), H(2), CNOT(1, 2)])
)
state2 = quantum_state(n_qubits, bits=0b1101)
state3 = quantum_state(
    n_qubits, vector=np.array([1/np.sqrt(2**n_qubits) for _ in range(2**n_qubits)])
)
