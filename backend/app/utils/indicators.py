# backend/app/utils/indicators.py

import pandas as pd

def calculate_sma(data: pd.DataFrame, period: int) -> pd.Series:
    """
    Calculates Simple Moving Average (SMA) for a given period.
    """
    return data['close'].rolling(window=period).mean()

def calculate_rsi(data: pd.DataFrame, period: int = 14) -> pd.Series:
    """
    Calculates Relative Strength Index (RSI) for a given period.
    """
    delta = data['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_bollinger_bands(data: pd.DataFrame, period: int = 20) -> pd.DataFrame:
    """
    Calculates Bollinger Bands for a given period.
    """
    sma = calculate_sma(data, period)
    rolling_std = data['close'].rolling(window=period).std()
    upper_band = sma + (rolling_std * 2)
    lower_band = sma - (rolling_std * 2)

    return pd.DataFrame({
        'sma': sma,
        'upper_band': upper_band,
        'lower_band': lower_band
    })
