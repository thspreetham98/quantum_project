# %%
from qiskit import QuantumCircuit
import numpy as np

# %%
def __random_2_qubit_init():
    qc = QuantumCircuit(2)
    for q in range(2):
        qc.rx(np.random.random()*(2*np.pi), q)
        qc.ry(np.random.random()*(2*np.pi), q)
        qc.rz(np.random.random()*(2*np.pi), q)
    qc.barrier()
    return qc

# %%
def random_2_qubit_circuit(no_of_cnots, prob_of_cnot) -> QuantumCircuit:
    '''
        no_of_cnots: # of CNOTs
        prob_of_cnot: probability of CNOT
    '''
    cnot_depth = 0
    other_depth = 0
    qc = __random_2_qubit_init()
    while cnot_depth < no_of_cnots:
        p = np.random.random()
        if p > prob_of_cnot:
            for q in range(2):
                op_type = np.random.randint(0, 4)
                match op_type:
                    case 0:
                        qc.rz(np.random.random()*(2*np.pi), q)
                    case 1:
                        qc.sx(q)
                    case 2:
                        qc.x(q)
                    case 3:
                        qc.id(q)
            other_depth += 1
        else:
            qc.cx(0, 1)
            cnot_depth += 1
    return qc



