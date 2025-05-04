# backend/app/services/alpaca_client.py

import os
from alpaca_trade_api.rest import REST
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame

API_KEY = os.getenv("APCA_API_KEY_ID")
SECRET_KEY = os.getenv("APCA_API_SECRET_KEY")
BASE_URL = os.getenv("APCA_API_BASE_URL")
print("API AND SCREET KEY ARE ",API_KEY,SECRET_KEY)

api = REST(API_KEY, SECRET_KEY, BASE_URL)
crypto_client = CryptoHistoricalDataClient(API_KEY, SECRET_KEY)

def place_order(symbol: str, qty: float, side: str):
    try:
        order = api.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,  # 'buy' or 'sell'
            type='market',
            time_in_force='gtc'
        )
        return {"status": "success", "order_id": order.id}
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