# backend/app/api/routes/backtest.py

from fastapi import APIRouter, Query
from app.backtester.backtest import Backtester
import pandas as pd

router = APIRouter()

@router.post("/backtest/run")
def run_backtest(
    symbol: str = Query(...),
    strategy_name: str = Query(...),
    start_date: str = Query(...),
    end_date: str = Query(...)
):
    # Load historical data (you may already have this as CSV or through an API)
    df = pd.read_csv(f"data/processed/{symbol}.csv")
    df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    
    # Initialize the backtester
    backtester = Backtester(df, strategy_name)
    final_balance, trade_history = backtester.backtest()
    
    performance_metrics = backtester.get_performance_metrics()
    
    return {
        "final_balance": final_balance,
        "performance_metrics": performance_metrics,
        "trade_history": trade_history
    }
