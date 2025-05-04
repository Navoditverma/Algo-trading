from fastapi import APIRouter
from .routes import strategies, backtest, trading, data

router = APIRouter()
router.include_router(strategies.router, prefix="/strategies", tags=["Strategies"])
router.include_router(backtest.router, prefix="/backtest", tags=["Backtest"])
router.include_router(trading.router, prefix="/trading", tags=["Trading"])
router.include_router(data.router, prefix="/data", tags=["Data"])
