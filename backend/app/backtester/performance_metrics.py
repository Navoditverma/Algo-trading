# backend/app/backtester/performance_metrics.py
import pandas as pd

def calculate_sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.0):
    """
    Calculate the Sharpe ratio: (Mean Portfolio Return - Risk-Free Rate) / Standard Deviation of Portfolio Return
    """
    excess_returns = returns - risk_free_rate
    return excess_returns.mean() / excess_returns.std()

def calculate_max_drawdown(returns: pd.Series):
    """
    Calculate the maximum drawdown of a portfolio.
    """
    cumulative_returns = (1 + returns).cumprod()
    peak = cumulative_returns.expanding(min_periods=1).max()
    drawdown = (cumulative_returns - peak) / peak
    return drawdown.min()

def calculate_annualized_return(returns: pd.Series, periods_per_year: int = 252):
    """
    Calculate the annualized return of a strategy.
    """
    total_return = (1 + returns).prod() - 1
    return (1 + total_return) ** (periods_per_year / len(returns)) - 1
