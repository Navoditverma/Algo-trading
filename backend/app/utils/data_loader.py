# backend/app/utils/data_loader.py

import pandas as pd
import os

DATA_DIR = "data/processed"  # Adjust path as needed

def load_data(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Loads and filters historical market data for a given symbol and date range.
    """
    file_path = os.path.join(DATA_DIR, f"{symbol}.csv")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file for {symbol} not found.")
    
    df = pd.read_csv(file_path)
    df['date'] = pd.to_datetime(df['date'])  # Ensure 'date' is in datetime format
    df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    
    return df
