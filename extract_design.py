import os
import networkx as nx
from pyverilog.vparser.parser import parse
from collections import defaultdict

verilog_file = "combinational_circuit.v"

def extract_design_data(ast):
    signals, modules, connections = set(), {}, defaultdict(list)

    def get_signal_name(node):
        """Extracts the signal name from AST Pointer or Identifier."""
        if hasattr(node, 'name'):
            return node.name
        elif hasattr(node, 'var') and hasattr(node.var, 'name'):
            return node.var.name
        else:
            return str(node)

    def traverse(node):
        if node is None:
            return

        if node.__class__.__name__ in ['Input', 'Output', 'Wire']:
            signals.add(node.name)

        if node.__class__.__name__ == 'Instance':
            modules[node.name] = node.module
            for param in node.portlist:
                signal_name = get_signal_name(param.argname)
                connections[node.name].append(signal_name)

        for child in node.children():
            traverse(child)

    traverse(ast)
    return signals, modules, connections

# Parse the Verilog file
ast, _ = parse([verilog_file])
signals, modules, connections = extract_design_data(ast)

# Create a directed graph for circuit representation
circuit_graph = nx.DiGraph()

# Add edges from extracted signal dependencies (connections)
for module, signals in connections.items():
    for signal in signals:
        circuit_graph.add_edge(module, signal)

# Ensure output directory exists
output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Save the graph to a file for further analysis
netlist_path = os.path.join(output_dir, "circuit_netlist.graphml")
nx.write_graphml(circuit_graph, netlist_path)

print(f"\n📌 Circuit netlist saved as '{netlist_path}'")
