# backend/app/main.py

from fastapi import FastAPI
from app.api.routes import trading, backtest, data, strategies,history,logs
from app.db import models, session
from app.core.config import Config
from fastapi.middleware.cors import CORSMiddleware
import logging
import os

os.makedirs("logs", exist_ok=True)

# Initialize the FastAPI app
app = FastAPI()

# Set up CORS (Cross-Origin Resource Sharing) if you're using a frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for simplicity, adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API routers for different routes
app.include_router(trading.router, prefix="/trading", tags=["Trading"])
app.include_router(backtest.router, prefix="/backtest", tags=["Backtest"])
app.include_router(data.router, prefix="/data", tags=["Data"])
app.include_router(strategies.router, prefix="/strategies", tags=["Strategies"])
app.include_router(history.router, prefix="/history")
app.include_router(logs.router, prefix="/logs")
# Create the database tables (if they don't exist)
models.Base.metadata.create_all(bind=session.engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Algorithmic Trading API"}
for route in app.routes:
    logging.warning(f"Registered route: {route.path}")