# backend/app/strategies/rsi_strategy.py

import pandas as pd

def rsi_strategy(df: pd.DataFrame, rsi_period: int = 14):
    """
    RSI Strategy
    - Buy when RSI crosses below 30 (oversold)
    - Sell when RSI crosses above 70 (overbought)
    """
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)

    avg_gain = gain.rolling(window=rsi_period).mean()
    avg_loss = loss.rolling(window=rsi_period).mean()

    rs = avg_gain / avg_loss
    df['rsi'] = 100 - (100 / (1 + rs))

    # Generate signals
    df['signal'] = 0
    df['signal'] = [1 if rsi < 30 else -1 if rsi > 70 else 0 for rsi in df['rsi']]

    return df
