from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
import os

router = APIRouter()

@router.get("/log", response_class=PlainTextResponse)
def get_logs():
    log_path = "logs/trading.log"  
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            return f.read()
    return "[INFO] No logs found yet."
