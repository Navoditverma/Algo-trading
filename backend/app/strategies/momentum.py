# backend/app/strategies/momentum.py

import pandas as pd

def momentum_strategy(df: pd.DataFrame, window: int = 14):
    """
    Momentum Strategy
    - Buy when the momentum is greater than 0
    - Sell when the momentum is less than 0
    """
    # Calculate momentum: difference between current price and price `window` periods ago
    df['momentum'] = df['close'] - df['close'].shift(window)

    # Generate signals
    df['signal'] = 0
    df['signal'] = [1 if df['momentum'][i] > 0 else -1 if df['momentum'][i] < 0 else 0 for i in range(len(df))]
    df['position'] = df['signal'].diff()

    return df
