# backend/app/trading/alpaca_trader.py
from fastapi import Depends
import alpaca_trade_api as tradeapi
from app.api.deps import get_settings
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db import crud

db: Session = Depends(get_db)

class AlpacaTrader:
    def __init__(self):
        settings = get_settings()
        self.api_key = settings["BROKER_API_KEY"]
        self.secret_key = settings["BROKER_SECRET_KEY"]
        self.base_url = "https://paper-api.alpaca.markets" if settings["MODE"] == "paper" else "https://api.alpaca.markets"
        self.api = tradeapi.REST(self.api_key, self.secret_key, self.base_url, api_version='v2')

    def get_account(self):
        account = self.api.get_account()
        return account

    def place_order(self, symbol: str, qty: float, side: str, strategy_name: str, db: Session):
        try:
            order = self.api.submit_order(
                symbol=symbol,
                qty=qty,
                side=side,
                type="market",
                time_in_force="gtc"
            )

        
            filled_price = 0.0  
            pnl = 0.0 

            crud.create_trade(
                db=db,
                symbol=symbol,
                qty=qty,
                side=side,
                price=filled_price,
                strategy_name=strategy_name,
                pnl=pnl
            )

            return order
        except Exception as e:
            return {"error": str(e)}


    def get_positions(self):
        positions = self.api.list_positions()
        return positions

    def get_balance(self):
        account = self.api.get_account()
        return account.cash

    def close_position(self, symbol: str):
        position = self.api.get_account().get_position(symbol)
        if position:
            return self.api.close_position(symbol)
        else:
            return {"error": "No position to close."}
