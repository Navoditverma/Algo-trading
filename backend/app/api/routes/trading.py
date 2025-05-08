# backend/app/api/routes/trading.py

from fastapi import APIRouter, HTTPException,Depends,Query
from app.api.deps import get_settings
from app.services.alpaca_client import place_order
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.db import models, crud  
from datetime import datetime
import threading
import time


router = APIRouter()
# db: Session = Depends(get_db)

live_trading_threads = {}
@router.post("/start")
def start_trading(symbol: str, strategy_name: str):
    if live_trading_threads.get(strategy_name, {}).get("running"):
        raise HTTPException(status_code=400, detail="Strategy already running")
    
    live_trading_threads[strategy_name] = {"running": True}
    db_session = next(get_db())

    thread = threading.Thread(target=run_live_trading, args=(symbol, strategy_name, db_session))
    thread.start()

    return {"status": "live trading started"}


@router.get("/stop")
def stop_trading(strategy_name: str = Query(...)):
    if strategy_name in live_trading_threads:
        live_trading_threads[strategy_name]["running"] = False
        del live_trading_threads[strategy_name]
        return {"status": "stopped"}
    else:
        raise HTTPException(status_code=404, detail="Strategy not running")


def run_live_trading(symbol, strategy_name, db_session):
    while True:
        # You can implement a flag to stop the thread later
        if not live_trading_threads.get(strategy_name, {}).get("running"):
            break

        
        try:
            qty = 1
            side = "buy"
            result = place_order(symbol, qty,side)
            print("Order result:", result)

            price = result.get("filled_avg_price") or result.get("price") or 0.0
            if price is None:
                print("Price not available yet, skipping DB insert.")
                continue
            pnl = 0.0  # You can compute real PnL based on price logic

            crud.create_trade(
                db=db_session,
                symbol=symbol,
                qty=1,
                side="buy",
                price=price,
                strategy_name=strategy_name,
                pnl=pnl
            )
        except Exception as e:
            print("Trade failed:", e)

        time.sleep(10)  # Wait before next trade


# @router.post("/trade")
# def execute_trade(symbol: str, qty: float, side: str):
#     """
#     Executes a market buy/sell order using Alpaca.
#     """
#     if side.lower() not in ("buy", "sell"):
#         raise HTTPException(status_code=400, detail="Invalid order side: must be 'buy' or 'sell'")
    
#     if qty <= 0:
#         raise HTTPException(status_code=400, detail="Quantity must be greater than 0")

#     try:
#         result = place_order(symbol, qty, side.lower())
#         return result
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


@router.post("/trade")
def execute_trade(
    symbol: str,
    qty: float,
    side: str,
    strategy_name: str,
    db: Session = Depends(get_db)
):
    if side.lower() not in ("buy", "sell"):
        raise HTTPException(status_code=400, detail="Invalid order side")

    if qty <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be > 0")

    try:
        result =  place_order(symbol, qty, side.lower())

        # Simulate/compute a PnL for now
        pnl = 0.0

        if "error" not in result:
            # Optionally extract filled price if Alpaca returns it
            price = result.get("filled_avg_price") or result.get("price") or 0.0
            crud.create_trade(
                db=db,
                symbol=symbol,
                qty=qty,
                side=side,
                price=price,
                strategy_name=strategy_name,
                pnl=pnl
            )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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


@router.get("/live/logs")
def get_live_logs(strategy_name: str, db: Session = Depends(get_db)):
    trades = db.query(models.TradeHistory).filter(models.TradeHistory.strategy_name == strategy_name).order_by(models.TradeHistory.timestamp.desc()).limit(10).all()
    logs = [
        f"{t.timestamp} - {t.side.upper()} {t.qty} {t.symbol} @ {t.price}" for t in trades
    ]
    pnl = sum([t.pnl for t in trades])
    return {"logs": logs, "pnl": pnl}

