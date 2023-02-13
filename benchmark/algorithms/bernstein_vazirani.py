from qiskit import QuantumCircuit

def bv_initialize(secret_number):
    n = len(secret_number)
    qc = QuantumCircuit(n+1, n)
    qc.h(range(n))

    qc.x(n)
    qc.h(n)
    qc.barrier()
    return qc

def apply_secret(secret_number):
    n = len(secret_number)
    qc = QuantumCircuit(n+1, n)
    for i in range(len(secret_number)):
        if secret_number[i] == '1':
            qc.cx(n-(i+1), n)
    qc.barrier()
    return qc

def bv_final_steps(secret_number):
    n = len(secret_number)
    qc = QuantumCircuit(n+1, n)
    qc.h(range(n))
    qc.measure(range(n), range(n))
    return qc

def bv_algorithm(secret_number):
    qc = bv_initialize(secret_number)
    qc = qc.compose(apply_secret(secret_number))
    qc = qc.compose(bv_final_steps(secret_number))
    return qc

def test(n) -> QuantumCircuit:
    secret_number = '1'*(n-1)
    qc = bv_initialize(secret_number)
    qc = qc.compose(apply_secret(secret_number))
    qc = qc.compose(bv_final_steps(secret_number))
    return qc