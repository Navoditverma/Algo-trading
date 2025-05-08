# backend/app/db/models.py

from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.db.session import Base  # ← ✅ Import shared Base

class TradeHistory(Base):
    __tablename__ = 'trade_history'
    id = Column(Integer, primary_key=True, index=True)
    strategy_name = Column(String) 
    symbol = Column(String, index=True)
    qty = Column(Float)
    side = Column(String)  # "buy" or "sell"
    price = Column(Float)
    pnl = Column(Float, default=0.0)  
    timestamp = Column(DateTime, default=datetime.utcnow)

class MarketData(Base):
    __tablename__ = 'market_data'
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    close_price = Column(Float)
    volume = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
