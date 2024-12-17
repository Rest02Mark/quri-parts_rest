from scaluq.f64 import *
import math

n_qubits = 3
state = StateVector.Haar_random_state(n_qubits, 0)

circuit = Circuit(n_qubits)
circuit.add_gate(gate::X(0))
circuit.add_gate(gate::CNot(0, 1))
circuit.add_gate(gate::Y(1))
circuit.add_gate(gate::RX(1, math.pi / 2))
circuit.update_quantum_state(state)

observable = Operator(n_qubits)
observable.add_random_operator(1, 0)
value = observable.get_expectation_value(state)
print(value)