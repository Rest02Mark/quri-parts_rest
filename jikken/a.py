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

#qulacs_circuit = convert_circuit(circuit)
#print(qulacs_circuit)

import sys


sys.path.append("/home/rest/baito/quri-parts/packages/scaluq/quri_parts")
print(sys.path)

#scaluq_aaaをimport
import scaluq_aaa 
import scaluq_aaa.circuit
#scaluq_aaa.helper_function()
#scaluq_aaa.circuit.scaluq_circuit_helper_function()
#scaluq_aaa.circuit.kakunin(circuit)

c = QuantumCircuit(2)
c.add_X_gate(0)
c.add_Pauli_gate([0, 1], [1, 2])


scaluq_circuit = scaluq_aaa.circuit.convert_circuit_f32(c)
scaluq_aaa.circuit.kakunin(circuit)
print(scaluq_circuit)

#from packages.scaluq.quri_parts import scaluq_aaa

#scaluq_aaa.helper_function()

