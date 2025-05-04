# backend/app/strategies/sma_crossover.py

import pandas as pd

def sma_crossover_strategy(df: pd.DataFrame):
    """
    Simple Moving Average Crossover Strategy
    - Buy when short-term SMA crosses above long-term SMA
    - Sell when short-term SMA crosses below long-term SMA
    """
    short_window = 50
    long_window = 100
    print("Length of dataset:", len(df))


    # Ensure enough data for short SMA
    if len(df) < short_window:
        raise ValueError(f"Not enough data for short-term SMA (requires {short_window} data points)")

    # If not enough data for long SMA, adjust to available data
    if len(df) < long_window:
        print(f"Warning: Not enough data for long-term SMA. Using available data length ({len(df)}).")
        long_window = len(df)

    # Compute short and long moving averages
    df['short_sma'] = df['close'].rolling(window=short_window).mean()
    df['long_sma'] = df['close'].rolling(window=long_window).mean()

    # Debugging: Print the short and long SMAs for inspection
    print(df[['date', 'short_sma', 'long_sma']].tail(50))    # Print first 60 rows for better visibility

    # Generate signals based on crossovers
    df['signal'] = 0

    # Detect crossover - check for short SMA crossing above long SMA (buy) and below (sell)
    for i in range(1, len(df)):
        if df['short_sma'][i] > df['long_sma'][i] and df['short_sma'][i-1] <= df['long_sma'][i-1]:
            print(f"Buy Signal: {df['date'][i]} - Short SMA: {df['short_sma'][i]} > Long SMA: {df['long_sma'][i]}")
            df.at[i, 'signal'] = 1  # Buy signal
        elif df['short_sma'][i] < df['long_sma'][i] and df['short_sma'][i-1] >= df['long_sma'][i-1]:
            print(f"Sell Signal: {df['date'][i]} - Short SMA: {df['short_sma'][i]} < Long SMA: {df['long_sma'][i]}")
            df.at[i, 'signal'] = -1  # Sell signal

    # Add position (buy or sell action based on signal change)
    df['position'] = df['signal'].diff()
    print(df[['date', 'short_sma', 'long_sma']].isna().sum())

    return df
