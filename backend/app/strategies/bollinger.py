import pandas as pd

def bollinger_strategy(df, window=20, num_std=2, rsi_period=14):
    # Calculate Bands
    df['ma'] = df['close'].rolling(window).mean()
    df['std'] = df['close'].rolling(window).std()
    df['upper_band'] = df['ma'] + num_std * df['std']
    df['lower_band'] = df['ma'] - num_std * df['std']
    # Band Width & Squeeze
    df['band_width'] = df['upper_band'] - df['lower_band']
    squeeze_window = 20
    squeeze_quantile = 0.2
    df['squeeze'] = df['band_width'] < df['band_width'].rolling(20).quantile(0.2)

    # Calculate RSI
    delta = df['close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1/rsi_period, min_periods=rsi_period).mean()
    avg_loss = loss.ewm(alpha=1/rsi_period, min_periods=rsi_period).mean()
    rs = avg_gain / avg_loss
    df['rsi'] = 100 - (100 / (1 + rs))
    
    # Signals: 1=long, -1=short, 0=flat
    df['signal'] = 0
    print(df)
    for i in range(window, len(df)):
        if df['squeeze'].iloc[i-1] and df['close'].iloc[i] > df['upper_band'].iloc[i] and df['rsi'].iloc[i] > 50:
            df.at[i, 'signal'] = 1  # Long breakout confirmed by RSI
        elif df['squeeze'].iloc[i-1] and df['close'].iloc[i] < df['lower_band'].iloc[i] and df['rsi'].iloc[i] < 50:
            df.at[i, 'signal'] = -1  # Short breakout confirmed by RSI

    return df[['date','close','upper_band','lower_band','rsi','signal']]
