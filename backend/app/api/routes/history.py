from fastapi import APIRouter
import json
import os

router = APIRouter()

BACKTEST_HISTORY_PATH = "data/logs/backtest_history.json"
LIVE_TRADE_HISTORY_PATH = "data/logs/live_trades.json"

# Load backtest history
@router.get("/backtests")
def get_backtest_history():
    if os.path.exists(BACKTEST_HISTORY_PATH):
        with open(BACKTEST_HISTORY_PATH, "r") as f:
            return json.load(f)
    return []

# Load live trade history
@router.get("/live-trades")
def get_live_trade_history():
    if os.path.exists(LIVE_TRADE_HISTORY_PATH):
        with open(LIVE_TRADE_HISTORY_PATH, "r") as f:
            return json.load(f)
    return []
