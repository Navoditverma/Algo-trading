# backend/app/db/crud.py

from sqlalchemy.orm import Session
from app.db import models

def create_trade(db: Session, symbol: str, qty: float, side: str, price: float, strategy_name: str, pnl: float = 0.0):
    db_trade = models.TradeHistory(
        symbol=symbol,
        qty=qty,
        side=side,
        price=price,
        strategy_name=strategy_name,
        pnl=pnl
    )
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    return db_trade


def get_trades(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TradeHistory).offset(skip).limit(limit).all()

def get_market_data(db: Session, symbol: str, skip: int = 0, limit: int = 100):
    return db.query(models.MarketData).filter(models.MarketData.symbol == symbol).offset(skip).limit(limit).all()
