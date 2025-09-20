# backend/app/ml/data_ingest.py

import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"
PROCESSED_DIR = Path(__file__).resolve().parents[2] / "data" / "processed"

# Mapping dataset names to filenames
FILENAME_MAP = {
    "loan_train": "train_u6lujuX_CVtuZ9i.csv",
    "loan_predication": "loan_predication.csv",  # ninzaami dataset
    "loan_approval_archit": "loan_approval_archit.csv",  # architsharma01 dataset
}


def load_dataset(dataset_name: str) -> pd.DataFrame:
    """
    Load a dataset by name.
    """
    fname = FILENAME_MAP.get(dataset_name)
    if fname is None:
        raise ValueError(f"Unknown dataset '{dataset_name}'. Available: {list(FILENAME_MAP.keys())}")

    file_path = DATA_DIR / fname
    if not file_path.exists():
        raise FileNotFoundError(f"Dataset file not found: {file_path}")

    df = pd.read_csv(file_path)
    return df


def save_processed(df: pd.DataFrame, name: str):
    """
    Save a processed DataFrame to the processed folder.
    """
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_DIR / name, index=False)


# Test: load all datasets and print a summary
if __name__ == "__main__":
    for ds_name in FILENAME_MAP.keys():
        print(f"\n=== Loading dataset: {ds_name} ===")
        df = load_dataset(ds_name)
        print("Shape:", df.shape)
        print("Columns:", df.columns.tolist())
        print("Head:\n", df.head(3))
