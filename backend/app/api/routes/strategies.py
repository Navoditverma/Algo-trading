# backend/app/api/routes/strategies.py

from fastapi import APIRouter, HTTPException, Query
import app.services.alpaca_client as api
from app.strategies import sma_crossover, rsi_strategy,bollinger,momentum,ml_predictor
import pandas as pd

router = APIRouter()

@router.get("/list")
def get_strategies():
    return ["sma_crossover", "rsi_strategy", "bollinger_band", "momentum", "ml_predictor"]

@router.post("/run")
def run_strategy(
    strategy_name: str = Query(...),
    symbol: str = Query(..., regex="^[A-Za-z0-9/]+$"),  # Allow / for crypto pairs
    start_date: str = Query(...),
    end_date: str = Query(...),
    timeframe: str = Query("1Day")  # Optional: 1Min, 5Min, 1Hour, 1Day
):
    try:
        # Check if symbol is a cryptocurrency pair (contains '/')
        if '/' in symbol:
            # For cryptocurrency pairs like BTC/USD
            bars = api.get_crypto_bars(symbol, timeframe, start=start_date, end=end_date).df
        else:
            # For stock symbols like AAPL
            bars = api.get_bars(symbol, timeframe, start=start_date, end=end_date).df  # use get_bars instead of get_barset

        # Remove duplicate columns if any
        bars = bars.loc[:, ~bars.columns.duplicated()]  # Remove duplicate columns

        # Process bars
        bars = bars.reset_index()
        bars["date"] = bars["timestamp"].dt.strftime('%Y-%m-%d')  # Add simple date column
        bars = bars.rename(columns={"close": "close", "timestamp": "date"})  # keep compatibility

        if bars.empty:
            raise HTTPException(status_code=404, detail="No data available for given range")

        # Run selected strategy
        if strategy_name == "sma_crossover":
            result = sma_crossover.sma_crossover_strategy(bars)
        elif strategy_name == "rsi_strategy":
            result = rsi_strategy(bars)
        elif strategy_name == "bollinger_band":
            result = bollinger.bollinger_strategy(bars)
        elif strategy_name == "momentum":
            result = momentum.momentum_strategy(bars)
        elif strategy_name == "ml_predictor":
            result, accuracy = ml_predictor.ml_predictor_strategy(bars)
            print(f"Model accuracy: {accuracy:.2f}")  # Print accuracy for debugging
        
        else:
            raise HTTPException(status_code=400, detail="Unknown strategy")

        return {
            "symbol": symbol,
            "strategy": strategy_name,
            "signals": result[['date', 'close', 'signal']].tail(50).to_dict(orient="records")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# curl -X POST "http://127.0.0.1:8000/strategies/run?strategy_name=bollinger_band&symbol=BTC/USD&start_date=2024-01-01&end_date=2024-05-01&timeframe=1Day"# curl -X POST "http://127.0.0.1:8000/strategies/run?strategy_name=momentum&symbol=BTC/USD&start_date=2024-01-01&end_date=2024-05-01&timeframe=1Day"