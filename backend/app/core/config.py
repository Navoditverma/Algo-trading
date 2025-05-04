# backend/app/core/config.py

import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Config:
    """
    Config class to store application-level settings.
    This is where all your global configuration goes.
    """
    PROJECT_NAME = "Algorithmic Trading Project"
    API_V1_STR = "/api/v1"
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")  # Example: Database URL
    ALPACA_API_KEY = os.getenv("ALPACA_API_KEY", "your-alpaca-api-key")  # Example: Alpaca API Key
    ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY", "your-alpaca-secret-key")  # Example: Alpaca Secret Key
    MODE = os.getenv("MODE", "paper")  # "paper" or "live" mode

    @staticmethod
    def init_app(app):
        """
        Initialize any necessary configurations.
        """
        pass
