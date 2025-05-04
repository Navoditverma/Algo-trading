# backend/app/core/settings.py

from app.core.config import Config

class Settings:
    def __init__(self):
        self.project_name = Config.PROJECT_NAME
        self.api_v1_str = Config.API_V1_STR
        self.database_url = Config.DATABASE_URL
        self.alpaca_api_key = Config.ALPACA_API_KEY
        self.alpaca_secret_key = Config.ALPACA_SECRET_KEY
        self.mode = Config.MODE

    def as_dict(self):
        return {
            "PROJECT_NAME": self.project_name,
            "API_V1_STR": self.api_v1_str,
            "DATABASE_URL": self.database_url,
            "ALPACA_API_KEY": self.alpaca_api_key,
            "ALPACA_SECRET_KEY": self.alpaca_secret_key,
            "MODE": self.mode
        }
