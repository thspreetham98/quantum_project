import numpy as np
from qiskit import QuantumCircuit

def qft_rotations(qc, n):
    if n == 0:
        return qc
    n -= 1
    qc.h(n)
    for qubit in range(n):
        qc.cp(np.pi/2**(n-qubit), qubit, n)
    qft_rotations(qc, n)

def flip_qubits(qc, n):
    for i in range(n//2):
        qc.swap(i, n-i-1)
    return qc

def qft(qc, n):
    qft_rotations(qc, n)
    flip_qubits(qc, n)
    return qc

def test(n) -> QuantumCircuit:
    qc = QuantumCircuit(n)
    qc.h(range(n))
    qc.barrier()
    qft(qc, n)
    qc.measure_all()
    return qc