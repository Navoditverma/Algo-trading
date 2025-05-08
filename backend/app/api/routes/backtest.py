from fastapi import APIRouter, Query, HTTPException
import pandas as pd
import os
from app.backtester.backtest import Backtester
import app.services.alpaca_client as api
from datetime import datetime
import json
import logging
logger = logging.getLogger(__name__)

HISTORY_FILE = "data/logs/backtest_history.json"

router = APIRouter()

@router.post("/run")
def run_backtest(
    symbol: str = Query(...),
    strategy_name: str = Query(...),
    start_date: str = Query(...),
    end_date: str = Query(...)
):
    logger.info("Starting backtest for" +  symbol + "using" +strategy_name )
    
    # Example log points
    logger.info("Fetching historical data...")
    logger.info("Running strategy logic...")

    logger.info("[TRADE] Buy BTC at $62,000")
    symbol = symbol.upper().strip()
    full_symbol = symbol + "/USD"
    print(f"Loading data for {symbol}...")
    timeframe = "1Day"
    bars = api.get_crypto_bars(full_symbol, timeframe, start=start_date, end=end_date).df

    if bars.empty:
        raise HTTPException(status_code=404, detail="No data found for the given date range.")

    bars = bars.reset_index()
    bars.rename(columns={
        "timestamp": "date",
        "open": "open",
        "high": "high",
        "low": "low",
        "close": "close",
        "volume": "volume"
    }, inplace=True)

    bars["date"] = pd.to_datetime(bars["date"])
    df = bars

    backtester = Backtester(df, strategy_name)
    final_balance, trade_history = backtester.backtest()
    performance_metrics = backtester.get_performance_metrics()

    # Save backtest to history
    history_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "symbol": symbol,
        "strategy": strategy_name,
        "start_date": start_date,
        "end_date": end_date,
        "final_balance": final_balance,
        "performance_metrics": performance_metrics
    }

    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []
    else:
        history = []

    history.append(history_entry)
    print(performance_metrics)

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)
    logger.info("Backtest complete.")

    return {
        "final_balance": final_balance,
        "performance_metrics": performance_metrics,
        "trade_history": trade_history
    }