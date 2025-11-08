import pandas as pd
import os
from logger import log

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_data():
    """Load preprocessed data_fast.pkl"""
    path = os.path.join(BASE_DIR, "data_fast.pkl")
    log("🔍 Loading preprocessed data...")
    df = pd.read_pickle(path)
    log(f"✅ Loaded {len(df)} rows with columns: {list(df.columns)}")
    return df
