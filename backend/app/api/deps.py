# backend/app/api/deps.py

from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()  # load from .env

@lru_cache()
def get_settings():
    return {
        "ALPACA_API_KEY": os.getenv("ALPACA_API_KEY"),
        "ALPACA_SECRET_KEY": os.getenv("ALPACA_SECRET_KEY"),
        "BROKER_API_KEY": os.getenv("BROKER_API_KEY"),
        "MODE": os.getenv("MODE", "paper"),  # paper or live
    }
