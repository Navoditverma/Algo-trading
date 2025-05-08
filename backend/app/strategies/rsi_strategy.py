# backend/app/strategies/rsi_strategy.py
import pandas as pd

def rsi_strategy(df, period=14):
    delta = df['close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1/period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/period, adjust=False).mean()

    rs = avg_gain / avg_loss
    df['rsi'] = 100 - (100 / (1 + rs))

    # Initialize signal
    df['signal'] = 0

    # Assign multi-level signals
    df.loc[df['rsi'] < 25, 'signal'] = 2    # Strong buy
    df.loc[(df['rsi'] >= 20) & (df['rsi'] < 40), 'signal'] = 1  # Weak buy
    df.loc[(df['rsi'] > 70) & (df['rsi'] <= 80), 'signal'] = -1  # Weak sell
    df.loc[df['rsi'] > 80, 'signal'] = -2   # Strong sell

    return df

