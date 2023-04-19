# %%
from qiskit import QuantumCircuit
import numpy as np

# %%
def random_2_qubit_circuit_one_way_cnot(no_of_cnots, depth) -> QuantumCircuit:
    if depth < no_of_cnots:
        raise ValueError("depth should be greater than no_of_cnots")
    qc = QuantumCircuit(2)
    cnot_count = 0
    for i in range(depth, 0, -1):
        prob_of_cnot = (no_of_cnots-cnot_count)/i
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
        else:
            qc.cx(0, 1)
            cnot_count += 1
    return qc

# %%
def random_2_qubit_circuit_two_way_cnot(no_of_cnots, depth) -> QuantumCircuit:
    if depth < no_of_cnots:
        raise ValueError("depth should be greater than no_of_cnots")
    qc = QuantumCircuit(2)
    cnot_count = 0
    for i in range(depth, 0, -1):
        prob_of_cnot = (no_of_cnots-cnot_count)/i
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
        else:
            if np.random.randint(2) == 0:
                qc.cx(0, 1)
            else:
                qc.cx(1, 0)
            cnot_count += 1
    return qc


