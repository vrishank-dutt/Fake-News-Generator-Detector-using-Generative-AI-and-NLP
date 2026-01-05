import pandas as pd
from sklearn.model_selection import train_test_split

# Load full dataset
df = pd.read_csv("train.csv")

# Encode labels as integers
df["label"] = df["label"].map({"FAKE": 0, "REAL": 1})

# Split into train/test (80/20)
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df["label"])

# Save to CSV files
train_df.to_csv("train.csv", index=False)
test_df.to_csv("test.csv", index=False)

print("✅ train.csv and test.csv created.")
