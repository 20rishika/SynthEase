from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
import pandas as pd

# Load extracted signal data
df = pd.read_csv("fan_in_out_data.csv")

# Ensure that 'Gate Type' and 'Signal' do not interfere with numerical processing
if "Signal" in df.columns:
    df.drop(columns=["Signal"], inplace=True)  # Drop signal names

# Check if 'Gate Type' exists before applying One-Hot Encoding
if "Gate Type" in df.columns:
    encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
    gate_encoded = encoder.fit_transform(df[["Gate Type"]])

    # Convert encoded features to DataFrame
    gate_encoded_df = pd.DataFrame(gate_encoded, columns=encoder.get_feature_names_out(["Gate Type"]))

    # Add one-hot encoded values to DataFrame
    df = pd.concat([df, gate_encoded_df], axis=1)

    # Drop the original 'Gate Type' column
    df.drop(columns=["Gate Type"], inplace=True)

# Normalize only numerical columns (Fan-in, Fan-out, Depth)
numerical_cols = ["Fan-in", "Fan-out", "Depth"]
df[numerical_cols] = MinMaxScaler().fit_transform(df[numerical_cols])

# Save transformed dataset
df.to_csv("circuit_features.csv", index=False)

print("\n📌 Feature Engineering Completed! Data saved as 'circuit_features.csv'")
print(df.head())
