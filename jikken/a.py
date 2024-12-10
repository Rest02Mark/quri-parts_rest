from quri_parts.circuit import X, RX, CNOT
from math import pi
from quri_parts.qulacs.circuit import convert_circuit
from quri_parts.circuit import QuantumCircuit


# Create a circuit for 3 qubits
circuit = QuantumCircuit(3)
# Add an already created QuantumGate object
circuit.add_gate(X(0))
# Or use methods to add gates
circuit.add_X_gate(0)
circuit.add_RX_gate(1, pi/3)
circuit.add_CNOT_gate(2, 1)
circuit.add_PauliRotation_gate(target_qubits=(0, 1, 2), pauli_id_list=(1, 2, 3), angle=pi/3)

qulacs_circuit = convert_circuit(circuit)
print(qulacs_circuit)