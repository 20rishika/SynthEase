import networkx as nx
import pandas as pd

# Load Netlist Graph
netlist_graph = nx.read_graphml("circuit_netlist.graphml")

# Extract Fan-in and Fan-out Information
fan_data = []
for node in netlist_graph.nodes:
    fan_data.append({
        "Signal": node,
        "Fan-in": netlist_graph.in_degree(node),
        "Fan-out": netlist_graph.out_degree(node)
    })

# Convert extracted data into a DataFrame
df = pd.DataFrame(fan_data)

# Function to Determine Gate Type
def get_gate_type(signal_name):
    if "and" in signal_name.lower():
        return "AND"
    elif "or" in signal_name.lower():
        return "OR"
    elif "xor" in signal_name.lower():
        return "XOR"
    elif "nand" in signal_name.lower():
        return "NAND"
    else:
        return "UNKNOWN"

# Apply function to add Gate Type column
df["Gate Type"] = df["Signal"].apply(get_gate_type)

# Save DataFrame to CSV
df.to_csv("fan_in_out_data.csv", index=False)

print("\n📌 Fan-in & Fan-out Data Saved to 'fan_in_out_data.csv'")
print(df.head())  # Display first few rows
