# backend/app/api/routes/data.py

from fastapi import APIRouter, HTTPException
from  app.services.alpaca_client import api

router = APIRouter()

@router.get("/crypto-data")
def get_crypto_data(symbol: str = "BTC/USD", timeframe: str = "1Hour", limit: int = 100):
    """
    Fetch historical crypto OHLCV data from Alpaca
    """
    try:
        bars = api.get_crypto_bars(symbol, timeframe, limit=limit).df
        bars = bars.reset_index()
        bars["timestamp"] = bars["timestamp"].astype(str)  # Ensure JSON serializable
        return bars.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
