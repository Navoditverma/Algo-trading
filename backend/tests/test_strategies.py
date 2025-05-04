# tests/test_strategies.py

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_strategies():
    response = client.get("/strategies/list")
    assert response.status_code == 200
    assert "sma_crossover" in response.json()
    assert "rsi_strategy" in response.json()

@pytest.fixture
def strategy_params():
    return {
        "strategy_name": "sma_crossover",
        "symbol": "AAPL",
        "start_date": "2022-01-01",
        "end_date": "2022-12-31"
    }

def test_run_strategy(strategy_params):
    response = client.post("/strategies/run", params=strategy_params)
    assert response.status_code == 200
    assert "signals" in response.json()  # Ensure the signals are returned
