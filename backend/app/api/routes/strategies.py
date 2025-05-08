# backend/app/api/routes/strategies.py

from fastapi import APIRouter, HTTPException, Query,Depends
import app.services.alpaca_client as api
from app.strategies import sma_crossover, rsi_strategy,bollinger,momentum,ml_predictor
import pandas as pd
from datetime import datetime
import random
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db import models  

router = APIRouter()

@router.get("/list")
def get_strategies():
    strategy_names = [
        "sma_crossover",
        "rsi_strategy",
        "bollinger_band",
        "momentum",
        "ML_predictor"
    ]

    def generate_mock_strategy(name):
        return {
            "id": name,
            "name": name.replace("_", " ").title(),
            "createdAt": datetime.utcnow().isoformat(),
            "performance": {
                "pnl": round(random.uniform(-5, 15), 2),
                "sharpe_ratio": round(random.uniform(0.5, 2.0), 2),
                "trades": random.randint(10, 50)
            }
        }

    return [generate_mock_strategy(name) for name in strategy_names]


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
            # For cryptocurrency pairs like BTC/USD
        symbol = symbol.upper().strip()
        full_symbol = symbol 
        print(full_symbol)

        bars = api.get_crypto_bars(full_symbol, timeframe, start=start_date, end=end_date).df
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
    
db: Session = Depends(get_db)

@router.get("/strategies/stats/{strategy_name}")
def get_strategy_stats(strategy_name: str, db: Session = Depends(get_db)):
    trades = db.query(models.TradeHistory).filter(models.TradeHistory.strategy_name == strategy_name).all()
    total_pnl = sum([t.pnl for t in trades])
    trade_count = len(trades)
    return {
        "strategy": strategy_name,
        "pnl": total_pnl,
        "trades": trade_count
    }



# curl -X POST "http://127.0.0.1:8000/strategies/run?strategy_name=sma_crossover&symbol=BTC/USD&start_date=2024-01-01&end_date=2024-05-01&timeframe=1Day"


# uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
