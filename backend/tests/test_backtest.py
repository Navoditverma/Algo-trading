# tests/test_backtest.py

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def mock_backtest_data():
    return {
        "symbol": "AAPL",
        "strategy_name": "sma_crossover",
        "start_date": "2022-01-01",
        "end_date": "2022-12-31"
    }

def test_run_backtest(mock_backtest_data):
    response = client.post("/backtest/run", params=mock_backtest_data)
    assert response.status_code == 200
    assert "stats" in response.json()  # Ensure backtest results are returned
