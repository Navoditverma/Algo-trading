# backend/app/services/alpaca_client.py

import os
from alpaca_trade_api.rest import REST
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

API_KEY = os.getenv("APCA_API_KEY_ID")
SECRET_KEY = os.getenv("APCA_API_SECRET_KEY")
BASE_URL = os.getenv("APCA_API_BASE_URL")
print("API AND SCREET KEY ARE ",API_KEY,SECRET_KEY)
trading_client = TradingClient(API_KEY, SECRET_KEY, paper=True)

api = REST(API_KEY, SECRET_KEY, BASE_URL)
crypto_client = CryptoHistoricalDataClient(API_KEY, SECRET_KEY)

def place_order(symbol: str, qty: float, side: str):
    try:
        print("Placing Order")
        market_order_data = MarketOrderRequest(
                    symbol=symbol,
                    qty=qty,
                    side=OrderSide.BUY if side.lower() == "buy" else OrderSide.SELL,
                    time_in_force=TimeInForce.DAY
                    )
        market_order = trading_client.submit_order(
                order_data=market_order_data
               )
        print("Placed")

        return {
            "status": "success",
            "order_id": market_order.id,
            "filled_avg_price": getattr(market_order, "filled_avg_price", None),
            "price": getattr(market_order, "price", None),
            }

    except Exception as e:
        return {"status": "error", "message": str(e)}
def get_account():
    return api.get_account()._raw

def get_crypto_bars(symbol: str, timeframe: str, start: str = None, end: str = None, limit: int = None):
    tf_map = {
        "1Min": TimeFrame.Minute,
        "5Min": TimeFrame.Minute,  # Just use TimeFrame.Minute for 5 minutes
        "1Hour": TimeFrame.Hour,
        "1Day": TimeFrame.Day,
    }
    tf = tf_map.get(timeframe, TimeFrame.Day)

    request_params = CryptoBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=tf,
        start=datetime.fromisoformat(start) if start else None,
        end=datetime.fromisoformat(end) if end else None,
        limit=limit,
    )

    return crypto_client.get_crypto_bars(request_params)