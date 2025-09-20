# backend/app/ml/train.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import accuracy_score, roc_auc_score, mean_squared_error
import joblib
import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

from backend.app.ml.preprocess import preprocess_data

# Directory to save models
MODELS_DIR = Path(__file__).resolve().parent / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

def train_models(dataset_name: str):
    print(f"\n--- Training models for dataset: {dataset_name} ---")

    # Preprocess dataset
    X, y_class, y_reg_amount, preprocessor = preprocess_data(dataset_name)

    # --------------------------
    # Classification (if target exists)
    # --------------------------
    if y_class is not None:
        try:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y_class, test_size=0.2, random_state=42, stratify=y_class
            )
        except ValueError:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y_class, test_size=0.2, random_state=42
            )

        if len(np.unique(y_train)) < 2:
            print(f"Skipping classification for {dataset_name}: only one class in training data")
            clf_pipeline = None
        else:
            clf_pipeline = Pipeline([
                ("preprocessor", preprocessor),
                ("scaler", StandardScaler(with_mean=False)),  # sparse OneHot
                ("clf", LogisticRegression(max_iter=500))
            ])
            clf_pipeline.fit(X_train, y_train)
            preds = clf_pipeline.predict(X_test)
            acc = accuracy_score(y_test, preds)
            auc = roc_auc_score(y_test, clf_pipeline.predict_proba(X_test)[:, 1])
            print("Classification Acc:", acc)
            print("AUC:", auc)

            # Save classification model
            clf_file = MODELS_DIR / f"{dataset_name}_eligibility_model.joblib"
            joblib.dump(clf_pipeline, clf_file)
            print(f"Saved classification model to: {clf_file}")

    # --------------------------
    # Regression (if target exists)
    # --------------------------
    if y_reg_amount is not None:
        # Fill missing values
        y_reg_amount = y_reg_amount.fillna(y_reg_amount.median())

        X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(
            X, y_reg_amount, test_size=0.2, random_state=42
        )
        reg_pipeline = Pipeline([
            ("preprocessor", preprocessor),
            ("regressor", LinearRegression())
        ])
        reg_pipeline.fit(X_train_r, y_train_r)
        preds_r = reg_pipeline.predict(X_test_r)
        rmse = np.sqrt(mean_squared_error(y_test_r, preds_r))
        print("LoanAmount RMSE:", rmse)

        # Save regression model
        reg_file = MODELS_DIR / f"{dataset_name}_amount_model.joblib"
        joblib.dump(reg_pipeline, reg_file)
        print(f"Saved regression model to: {reg_file}")


# --------------------------
# Train all datasets
# --------------------------
if __name__ == "__main__":
    for ds_name in ["loan_train", "loan_predication", "loan_approval_archit"]:
        train_models(ds_name)
