import pandas as pd
import networkx as nx

# Load the netlist graph
netlist_graph = nx.read_graphml("circuit_netlist.graphml")

# Compute combinational depth
depth = nx.dag_longest_path_length(netlist_graph)

# Add Depth information to CSV
fan_df = pd.read_csv("fan_in_out_data.csv")
fan_df["Depth"] = depth  # Add depth as a new column
fan_df.to_csv("fan_in_out_data.csv", index=False)

print(f"\n📌 Combinational Depth ({depth}) added to 'fan_in_out_data.csv'")
