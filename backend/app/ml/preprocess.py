# backend/app/ml/preprocess.py

import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

from backend.app.ml.data_ingest import load_dataset

def preprocess_data(dataset_name: str):
    # Load dataset
    df = load_dataset(dataset_name)

    # Drop ID columns if present
    if "Loan_ID" in df.columns or "loan_id" in df.columns:
        df = df.drop(columns=[col for col in ["Loan_ID", "loan_id"] if col in df.columns])

    # --------------------------
    # Target mapping (classification)
    # --------------------------
    target_cols = ["Loan_Status", "Approved", "Status", "loan_status"]
    y_class = None
    for col in target_cols:
        if col in df.columns:
            unique_vals = set(df[col].dropna().unique())
            if unique_vals == {"y", "n"}:
                y_class = df[col].map({"y": 1, "n": 0})
            elif unique_vals == {"approved", "rejected"}:
                y_class = df[col].map({"approved": 1, "rejected": 0})
            else:
                # fallback for text: approved/rejected (case insensitive)
                y_class = df[col].map(lambda x: 1 if str(x).strip().lower() == "approved" else 0)
            break

    if y_class is None:
        raise ValueError(f"No recognizable target column found. Checked: {target_cols}")

    # --------------------------
    # Regression target (LoanAmount)
    # --------------------------
    y_reg_amount = None
    for col in ["LoanAmount", "loan_amount"]:
        if col in df.columns:
            y_reg_amount = df[col]
            break

    # --------------------------
    # Feature matrix
    # --------------------------
    drop_cols = [col for col in target_cols + ["LoanAmount", "loan_amount"] if col in df.columns]
    X = df.drop(columns=drop_cols, errors=False)

    # Identify categorical vs numeric
    categorical_cols = X.select_dtypes(include=["object"]).columns.tolist()
    numeric_cols = X.select_dtypes(include=["number"]).columns.tolist()

    # --------------------------
    # Debug prints
    # --------------------------
    print("\nDataset:", dataset_name)
    print("Categorical cols:", categorical_cols)
    print("Numeric cols:", numeric_cols)
    print("Sample features:\n", X.head(3))
    print("Sample target:\n", y_class.head(3))

    # --------------------------
    # Preprocessing pipeline
    # --------------------------
    numeric_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="median"))
    ])
    categorical_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer([
        ("num", numeric_transformer, numeric_cols),
        ("cat", categorical_transformer, categorical_cols)
    ])

    return X, y_class, y_reg_amount, preprocessor


# --------------------------
# Test all datasets
# --------------------------
if __name__ == "__main__":
    for ds_name in ["loan_train", "loan_predication", "loan_approval_archit"]:
        print(f"\n=== Preprocessing dataset: {ds_name} ===")
        X, y_class, y_reg_amount, preprocessor = preprocess_data(ds_name)
        print("Feature shape:", X.shape)
        print("Target shape:", y_class.shape)
        if y_reg_amount is not None:
            print("Regression target shape:", y_reg_amount.shape)
