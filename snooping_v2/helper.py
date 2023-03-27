from qiskit.converters import circuit_to_dag
from qiskit.dagcircuit.dagcircuit import DAGCircuit, DAGOpNode

def circuit_runtime_in_ms(tqc, backend):
    props = backend.properties()
    dag = circuit_to_dag(tqc)
    circuit_execution_time = 0
    qubits_map = {}
    for q_index, qubit in enumerate(dag.qubits):
        qubits_map[qubit] = q_index

    for s in dag.layers():
        graph: DAGCircuit = s['graph']
        gate: DAGOpNode
        max_gate_time_in_layer = 0
        for gate in graph.gate_nodes():
            q_index = [qubits_map[qarg] for qarg in gate.qargs]
            g_time = props.gate_length(gate.name, q_index)
            if g_time > max_gate_time_in_layer:
                max_gate_time_in_layer = g_time
        circuit_execution_time += max_gate_time_in_layer
    return circuit_execution_time*1000