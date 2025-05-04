# backend/app/api/routes/trading.py

from fastapi import APIRouter, HTTPException
from app.api.deps import get_settings
from app.services.alpaca_client import place_order

router = APIRouter()

@router.post("/start")
def start_trading(symbol: str, strategy_name: str):
    settings = get_settings()

    if settings["MODE"] == "paper":
        return {
            "status": "paper trading session initialized",
            "symbol": symbol,
            "strategy": strategy_name
        }
    elif settings["MODE"] == "live":
        # You could trigger strategy signal + trade placement here
        return {
            "status": "live trading session initialized",
            "symbol": symbol,
            "strategy": strategy_name
        }
    else:
        raise HTTPException(status_code=400, detail="Invalid mode in settings")


@router.post("/trade")
def execute_trade(symbol: str, qty: float, side: str):
    """
    Executes a market buy/sell order using Alpaca.
    """
    if side.lower() not in ("buy", "sell"):
        raise HTTPException(status_code=400, detail="Invalid order side: must be 'buy' or 'sell'")
    
    if qty <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")

    try:
        result = place_order(symbol, qty, side.lower())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
