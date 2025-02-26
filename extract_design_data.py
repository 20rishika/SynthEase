import os
from pyverilog.vparser.parser import parse
from collections import defaultdict

verilog_file = "combinational_circuit.v"

def extract_design_data(ast):
    signals, modules, connections = set(), {}, defaultdict(list)

    def traverse(node):
        if node is None:
            return

        if node.__class__.__name__ in ['Input', 'Output', 'Wire']:
            signals.add(node.name)

        if node.__class__.__name__ == 'Instance':
            modules[node.name] = node.module
            for param in node.portlist:
                connections[node.name].append(param.argname)

        for child in node.children():
            traverse(child)

    traverse(ast)
    return signals, modules, connections

ast, _ = parse([verilog_file])
signals, modules, connections = extract_design_data(ast)

print("\n📌 Extracted Signals:", signals)
print("\n📌 Module Instances:", modules)
print("\n📌 Signal Dependencies:", connections)
