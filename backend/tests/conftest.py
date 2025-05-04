# tests/conftest.py

import pytest

@pytest.fixture
def mock_data():
    # Setup mock data for testing
    return {
        "symbol": "AAPL",
        "start_date": "2022-01-01",
        "end_date": "2022-12-31",
    }
