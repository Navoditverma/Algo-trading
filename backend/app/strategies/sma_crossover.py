import pandas as pd

def sma_crossover_strategy(df: pd.DataFrame):
    """
    SMA Crossover Strategy
    - Buy when short SMA crosses above long SMA
    - Sell when short SMA crosses below long SMA
    """

    short_window = 20
    long_window = 50
    strong_threshold = 0.01  # 1% threshold for strong signals

    # Remove duplicate columns
    df = df.loc[:, ~df.columns.duplicated()].copy()

    # Ensure proper datetime format and sort
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').reset_index(drop=True)

    # Check data length
    if len(df) < long_window + 1:
        raise ValueError("Not enough data to compute long SMA.")

    # Compute SMAs
    df['short_sma'] = df['close'].rolling(window=short_window).mean()
    df['long_sma'] = df['close'].rolling(window=long_window).mean()

    df['signal'] = 0  # Default to Hold

    for i in range(1, len(df)):
        prev_short = df.at[i - 1, 'short_sma']
        prev_long = df.at[i - 1, 'long_sma']
        curr_short = df.at[i, 'short_sma']
        curr_long = df.at[i, 'long_sma']

        # Only proceed if values are not NaN
        if pd.notna(prev_short) and pd.notna(prev_long) and pd.notna(curr_short) and pd.notna(curr_long):
            # BUY signal: crossover up
            if curr_short > curr_long and prev_short <= prev_long:
                spread = abs(curr_short - curr_long) / curr_long
                df.at[i, 'signal'] = 2 if spread > strong_threshold else 1
                print(f"BUY {'STRONG' if spread > strong_threshold else 'WEAK'} @ {df.at[i, 'date']} | Spread: {spread:.4f}")
            # SELL signal: crossover down
            elif curr_short < curr_long and prev_short >= prev_long:
                spread = abs(curr_short - curr_long) / curr_long
                df.at[i, 'signal'] = -2 if spread > strong_threshold else -1
                print(f"SELL {'STRONG' if spread > strong_threshold else 'WEAK'} @ {df.at[i, 'date']} | Spread: {spread:.4f}")

    # Label mapping for readability
    signal_map = {
        2: 'Strong Buy',
        1: 'Buy',
        0: 'Hold',
        -1: 'Sell',
        -2: 'Strong Sell'
    }
    df['signal_label'] = df['signal'].map(signal_map)

    return df[['date', 'close', 'short_sma', 'long_sma', 'signal', 'signal_label']]
