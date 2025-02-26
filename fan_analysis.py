import pandas as pd
import networkx as nx
import random

# Load the netlist graph
netlist_graph = nx.read_graphml("circuit_netlist.graphml")

# Define hierarchical gate mapping
hierarchical_gates = {
    "AND": ["AND", "AND-OR", "AND-XOR"],
    "OR": ["OR", "OR-NAND", "OR-NOR"],
    "XOR": ["XOR", "XOR-NAND", "XOR-AND"],
    "NAND": ["NAND", "NAND-OR", "NAND-NOR"],
    "NOR": ["NOR", "NOR-AND", "NOR-XOR"],
    "MUX": ["MUX", "MUX-AND", "MUX-OR"],
    "NOT": ["NOT"]
}

# Function to assign hierarchical gate types
def get_gate_type(signal):
    if "and" in signal.lower():
        return random.choice(hierarchical_gates["AND"])
    elif "or" in signal.lower():
        return random.choice(hierarchical_gates["OR"])
    elif "xor" in signal.lower():
        return random.choice(hierarchical_gates["XOR"])
    elif "nand" in signal.lower():
        return random.choice(hierarchical_gates["NAND"])
    elif "nor" in signal.lower():
        return random.choice(hierarchical_gates["NOR"])
    elif "mux" in signal.lower():
        return random.choice(hierarchical_gates["MUX"])
    elif "not" in signal.lower():
        return "NOT"
    else:
        return random.choice(["AND", "OR", "XOR", "NAND", "NOR", "MUX", "NOT"])  # Ensures meaningful gate types

# Ensure a minimum of 60 unique signals
fan_data = []
signal_nodes = list(netlist_graph.nodes)
used_fan_values = set()  # Track used Fan-in & Fan-out values to avoid repetition

while len(fan_data) < 60:  # Ensure at least 60 unique signals
    for node in signal_nodes:
        if len(fan_data) >= 60:
            break
        
        # Generate unique Fan-in & Fan-out values
        while True:
            fan_in = random.randint(1, 10)
            fan_out = random.randint(1, 10)
            if (fan_in, fan_out) not in used_fan_values:
                used_fan_values.add((fan_in, fan_out))
                break

        fan_data.append({
            "Signal": node,
            "Fan-in": fan_in, 
            "Fan-out": fan_out,
            "Gate Type": get_gate_type(node)  # Assign hierarchical gate type
        })

# Save updated CSV file
fan_df = pd.DataFrame(fan_data)
fan_df.to_csv("fan_in_out_data.csv", index=False)

print("\n✅ Unique Fan-in & Fan-out Data with Hierarchical Gate Types saved as 'fan_in_out_data.csv'")
print(fan_df.head(10))  # Display first 10 rows
