# backend/app/utils/signal_generator.py

def generate_buy_signal(data: pd.DataFrame, sma_period: int = 50, rsi_period: int = 14) -> pd.DataFrame:
    """
    Generates buy signals based on simple conditions (e.g., SMA crossovers, RSI).
    """
    data['sma'] = data['close'].rolling(window=sma_period).mean()
    data['rsi'] = calculate_rsi(data, rsi_period)
    data['buy_signal'] = (data['close'] > data['sma']) & (data['rsi'] < 30)
    return data

def generate_sell_signal(data: pd.DataFrame, sma_period: int = 50, rsi_period: int = 14) -> pd.DataFrame:
    """
    Generates sell signals based on simple conditions (e.g., RSI overbought, SMA crossovers).
    """
    data['sma'] = data['close'].rolling(window=sma_period).mean()
    data['rsi'] = calculate_rsi(data, rsi_period)
    data['sell_signal'] = (data['close'] < data['sma']) & (data['rsi'] > 70)
    return data
