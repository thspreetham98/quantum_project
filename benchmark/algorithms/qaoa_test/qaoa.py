import itertools
import networkx as nx
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.circuit import Parameter

def test_graph(nqubits):
    # regular graph
    G = nx.Graph()
    G.add_nodes_from(range(nqubits))
    G.add_edges_from(itertools.combinations(list(G.nodes), 2))
    return G

def maxcut_obj(x, G):
    """
    Given a bitstring as a solution, this function returns
    the number of edges shared between the two partitions
    of the graph.
    
    Args:
        x: str
           solution bitstring
           
        G: networkx graph
        
    Returns:
        obj: float
             Objective
    """
    obj = 0
    for i, j in G.edges():
        if x[i] != x[j]:
            obj -= 1
            
    return obj


def compute_expectation(counts, G):
    
    """
    Computes expectation value based on measurement results
    
    Args:
        counts: dict
                key as bitstring, val as count
           
        G: networkx graph
        
    Returns:
        avg: float
             expectation value
    """
    
    avg = 0
    sum_count = 0
    for bitstring, count in counts.items():
        
        obj = maxcut_obj(bitstring[::-1], G)
        avg += obj * count
        sum_count += count
        
    return avg/sum_count


# We will also bring the different circuit components that
# build the qaoa circuit under a single function
def create_qaoa_circ(G, theta):
    
    """
    Creates a parametrized qaoa circuit
    
    Args:  
        G: networkx graph
        theta: list
               unitary parameters
                     
    Returns:
        qc: qiskit circuit
    """
    
    nqubits = len(G.nodes())
    p = len(theta)//2  # number of alternating unitaries
    qc = QuantumCircuit(nqubits)
    
    beta = theta[:p]
    gamma = theta[p:]
    
    # initial_state
    for i in range(0, nqubits):
        qc.h(i)
    
    for irep in range(0, p):
        
        # problem unitary
        for pair in list(G.edges()):
            qc.rzz(2 * gamma[irep], pair[0], pair[1])

        # mixer unitary
        for i in range(0, nqubits):
            qc.rx(2 * beta[irep], i)
            
    qc.measure_all()
        
    return qc

# Finally we write a function that executes the circuit on the chosen backend
def get_expectation(G, backend, shots=512):
    
    """
    Runs parametrized circuit
    
    Args:
        G: networkx graph
        p: int,
           Number of repetitions of unitaries
    """
    
    backend.shots = shots
    
    def execute_circ(theta):
        
        qc = create_qaoa_circ(G, theta)
        counts = backend.run(qc, seed_simulator=10, 
                             nshots=512).result().get_counts()
        
        return compute_expectation(counts, G)
    
    return execute_circ



# Finally we write a function that executes the circuit on the chosen backend
# def get_expectation(G, shots=512):
    
#     """
#     Runs parametrized circuit
    
#     Args:
#         G: networkx graph
#         p: int,
#            Number of repetitions of unitaries
#     """
    
#     backend = Aer.get_backend('qasm_simulator')
#     backend.shots = shots
    
#     def execute_circ(theta):
        
#         qc = create_qaoa_circ(G, theta)
#         counts = backend.run(qc, seed_simulator=10, 
#                              nshots=512).result().get_counts()
        
#         return compute_expectation(counts, G)
    
#     return execute_circ

# def test(nqubits) -> QuantumCircuit:
#     qc_qaoa = QuantumCircuit(nqubits)
#     G = test_graph(nqubits)
#     qc_0 = initial_state(nqubits)
#     beta = Parameter("$\\beta$")
#     gamma = Parameter("$\\gamma$")
#     qc_p = problem_unitary(G, gamma)
#     qc_mix = mixing_unitary(G, beta)
#     qc_qaoa = qc_qaoa.compose(qc_0, [i for i in range(0, nqubits)])
#     qc_qaoa = qc_qaoa.compose(qc_p, [i for i in range(0, nqubits)])
#     qc_qaoa = qc_qaoa.compose(qc_mix, [i for i in range(0, nqubits)])
#     return qc_qaoa


# def test(n) -> QuantumCircuit:
#     qc = QuantumCircuit(n)
#     qc.h(range(n))
#     qc.barrier()
#     qft(qc, n)
#     qc.measure_all()
#     return qc