# backend/app/backtester/__init__.py

# This can be left empty or you can import the Backtester class to make it accessible.
from .backtest import Backtester
from .performance_metrics import calculate_sharpe_ratio, calculate_max_drawdown, calculate_annualized_return
