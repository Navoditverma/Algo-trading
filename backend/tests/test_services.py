# tests/test_services.py

from unittest.mock import patch
from app.services.alpaca_client import place_order

@patch("app.services.alpaca_client.AlpacaAPI.place_order")
def test_place_order(mock_place_order):
    # Simulate a successful order response
    mock_place_order.return_value = {"status": "success", "symbol": "AAPL", "side": "buy", "qty": 10}
    
    result = place_order("AAPL", 10, "buy")
    assert result == {"status": "success", "symbol": "AAPL", "side": "buy", "qty": 10}
