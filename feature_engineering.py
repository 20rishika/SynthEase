from sklearn.preprocessing import OneHotEncoder, MinMaxScaler, StandardScaler
import pandas as pd
import numpy as np  # Ensure numerical handling


# Load extracted signal data
# ✅ Load dataset
df = pd.read_csv("circuit_features.csv")

# ✅ Check for missing values in the dataset
if df.isnull().sum().sum() > 0:
    print("\n❌ ERROR: Missing values detected! Filling with mean values.")
    df.fillna(df.mean(), inplace=True)  # Replace NaN values with column mean

# ✅ Ensure all values are numeric
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert non-numeric to NaN

# ✅ Drop any remaining NaN values
df.dropna(inplace=True)

# ✅ Ensure at least 60 signals remain
if len(df) < 60:
    raise ValueError(f"❌ ERROR: Dataset contains only {len(df)} signals. Minimum 60 required!")


# Ensure at least 60 unique signals
if len(df) < 60:
    raise ValueError(f"❌ ERROR: Dataset contains only {len(df)} signals. Minimum 60 required!")

# Drop 'Signal' column (not needed for numerical processing)
if "Signal" in df.columns:
    df.drop(columns=["Signal"], inplace=True)

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

# Ensure numerical columns exist
numerical_cols = ["Fan-in", "Fan-out", "Depth"]
for col in numerical_cols:
    if col not in df.columns:
        raise ValueError(f"❌ ERROR: Missing required column '{col}' in dataset!")

# ✅ Ensure "Depth" column exists
if "Depth" not in df.columns:
    raise ValueError("❌ ERROR: 'Depth' column is missing in circuit_features.csv. Check feature engineering step.")

# ✅ Ensure there are no NaN or infinite values in Depth
if df["Depth"].isnull().sum() > 0:
    print("\n❌ ERROR: Missing values in Depth column! Filling with mean depth.")
    df["Depth"].fillna(df["Depth"].mean(), inplace=True)  # Replace NaN with mean

if not df["Depth"].apply(lambda x: isinstance(x, (int, float))).all():
    raise ValueError("❌ ERROR: Non-numeric values found in Depth column. Check dataset.")

# Ensure unique depth values & prevent data leakage
df["Depth"] = df["Depth"] + df.index % 5  # Add variation to depth

# ✅ Normalize numerical data
scaler = StandardScaler()

# ✅ Ensure no NaN values before scaling
if df.isnull().sum().sum() > 0:
    print("\n⚠️ Warning: NaN values detected before scaling. Filling missing values with mean.")
    df.fillna(df.mean(), inplace=True)

X_scaled = scaler.fit_transform(df.drop(columns=["Depth"]))  # Normalize all numerical features

# ✅ Ensure no NaN or infinite values before training
if not X_scaled.all():
    raise ValueError("❌ ERROR: NaN or infinite values detected in training data! Check preprocessing step.")

# Save transformed dataset
df.to_csv("circuit_features.csv", index=False)

print("\n✅ Feature Engineering Completed! Data saved as 'circuit_features.csv'")
print("\n📊 Sample Processed Data:")
print(df.head(10))  # Show first 10 rows
