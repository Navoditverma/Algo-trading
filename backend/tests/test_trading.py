# tests/test_trading.py

from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

@patch("app.services.alpaca_client.place_order")
def test_execute_trade(mock_place_order):
    mock_place_order.return_value = {"status": "success", "symbol": "AAPL", "side": "buy", "qty": 10}
    
    response = client.post("/trading/trade", params={"symbol": "AAPL", "qty": 10, "side": "buy"})
    assert response.status_code == 200
    assert response.json() == {"status": "success", "symbol": "AAPL", "side": "buy", "qty": 10}
