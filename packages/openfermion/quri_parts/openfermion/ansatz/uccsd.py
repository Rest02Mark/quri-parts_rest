# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#      http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from quri_parts.chem.utils.excitations import (
    DoubleExcitation,
    SingleExcitation,
    excitations,
    spin_symmetric_excitations,
)
from quri_parts.circuit import (
    ImmutableLinearMappedUnboundParametricQuantumCircuit,
    LinearMappedUnboundParametricQuantumCircuit,
    Parameter,
)

from ..transforms import OpenFermionQubitMapping, jordan_wigner
from ..utils import (
    add_exp_excitation_gates_trotter_decomposition,
    add_spin_symmetric_exp_excitation_gates_trotter_decomposition,
)


class TrotterSingletUCCSD(ImmutableLinearMappedUnboundParametricQuantumCircuit):
    """Unitary coupled-cluster singles and doubles (UCCSD) ansatz. The ansatz
    consists of the exponentials of single excitation and double excitation
    operator decomposed by first-order Trotter product formula. Note that the ansatz
    only supports singlet state and the occupied orbitals are the lowest
    :attr:`n_fermions` spin orbitals. The decomposition using Trotter product formula
    is executed for each qubit operators obtained by mapping excitation operators.

    Args:
        n_spin_orbitals: Number of spin orbitals.
        n_fermions: Number of fermions.
        fermion_qubit_mapping: Mapping from :class:`FermionOperator` to
          :class:`Operator`
        trotter_number: Number for first-order Trotter product formula.
        use_singles: If ``True``, single-excitation gates are applied.
    """

    def __init__(
        self,
        n_spin_orbitals: int,
        n_fermions: int,
        fermion_qubit_mapping: OpenFermionQubitMapping = jordan_wigner,
        trotter_number: int = 1,
        use_singles: bool = True,
        spin_symmetric: bool = False,
    ):
        n_vir_sorbs = n_spin_orbitals - n_fermions

        if n_fermions % 2:
            raise ValueError("Number of electrons must be even for SingletUCCSD.")

        if n_vir_sorbs <= 0:
            raise ValueError("Number of virtual orbitals must be a non-zero integer.")

        circuit = (
            _construct_spin_symmetric_circuit(
                n_spin_orbitals,
                n_fermions,
                fermion_qubit_mapping,
                trotter_number,
                use_singles,
            )
            if spin_symmetric
            else _construct_circuit(
                n_spin_orbitals,
                n_fermions,
                fermion_qubit_mapping,
                trotter_number,
                use_singles,
            )
        )

        super().__init__(circuit)


def _construct_circuit(
    n_spin_orbitals: int,
    n_fermions: int,
    fermion_qubit_mapping: OpenFermionQubitMapping,
    trotter_number: int,
    use_singles: bool,
) -> LinearMappedUnboundParametricQuantumCircuit:
    n_qubits = fermion_qubit_mapping.n_qubits_required(n_spin_orbitals)

    s_excs, d_excs = excitations(n_spin_orbitals, n_fermions, delta_sz=0)

    circuit = LinearMappedUnboundParametricQuantumCircuit(n_qubits)
    if use_singles:
        s_exc_params = [
            circuit.add_parameter(f"theta_s_{i}") for i in range(len(s_excs))
        ]
    d_exc_params = [circuit.add_parameter(f"theta_d_{i}") for i in range(len(d_excs))]
    op_mapper = fermion_qubit_mapping.get_of_operator_mapper(
        n_spin_orbitals, n_fermions
    )
    for _ in range(trotter_number):
        add_exp_excitation_gates_trotter_decomposition(
            circuit, d_excs, d_exc_params, op_mapper, 1 / trotter_number
        )
        if use_singles:
            add_exp_excitation_gates_trotter_decomposition(
                circuit, s_excs, s_exc_params, op_mapper, 1 / trotter_number
            )

    return circuit


def _construct_spin_symmetric_circuit(
    n_spin_orbitals: int,
    n_fermions: int,
    fermion_qubit_mapping: OpenFermionQubitMapping,
    trotter_number: int,
    use_singles: bool,
) -> LinearMappedUnboundParametricQuantumCircuit:
    n_qubits = fermion_qubit_mapping.n_qubits_required(n_spin_orbitals)

    s_excs, d_excs = spin_symmetric_excitations(n_spin_orbitals, n_fermions)

    circuit = LinearMappedUnboundParametricQuantumCircuit(n_qubits)
    if use_singles:
        s_exc_params: dict[SingleExcitation, Parameter] = {}
        s_exc_param_names: dict[SingleExcitation, str] = {}
        for occ, vir in s_excs:
            param_name = f"theta_s_{occ//2}_{vir//2}"
            if param_name not in s_exc_param_names.values():
                s_exc_params[(occ // 2, vir // 2)] = circuit.add_parameter(param_name)
            s_exc_param_names[(occ, vir)] = param_name

    d_exc_params: dict[DoubleExcitation, Parameter] = {}
    d_exc_param_names: dict[DoubleExcitation, str] = {}
    for occ1, occ2, vir1, vir2 in d_excs:
        param_name = f"theta_d_{occ1//2}_{occ2//2}_{vir1//2}_{vir2//2}"
        if param_name not in d_exc_param_names.values():
            d_exc_params[
                (occ1 // 2, occ2 // 2, vir1 // 2, vir2 // 2)
            ] = circuit.add_parameter(param_name)
        d_exc_param_names[(occ1, occ2, vir1, vir2)] = param_name

    op_mapper = fermion_qubit_mapping.get_of_operator_mapper(
        n_spin_orbitals, n_fermions
    )
    for _ in range(trotter_number):
        add_spin_symmetric_exp_excitation_gates_trotter_decomposition(
            circuit, d_excs, d_exc_params, op_mapper, 1 / trotter_number
        )
        if use_singles:
            add_spin_symmetric_exp_excitation_gates_trotter_decomposition(
                circuit, s_excs, s_exc_params, op_mapper, 1 / trotter_number
            )

    return circuit
