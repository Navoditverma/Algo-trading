# tests/test_data.py

import os
import pytest
from fastapi.testclient import TestClient
from app.main import app
import pandas as pd

client = TestClient(app)
DATA_DIR = "data/processed"

@pytest.fixture
def mock_data_file():
    # Create a mock CSV file for testing upload
    df = pd.DataFrame({
        "date": ["2022-01-01", "2022-01-02"],
        "symbol": ["AAPL", "AAPL"],
        "close": [150.0, 155.0]
    })
    file_path = os.path.join(DATA_DIR, "AAPL.csv")
    df.to_csv(file_path, index=False)
    return file_path

def test_upload_data(mock_data_file):
    with open(mock_data_file, "rb") as file:
        response = client.post("/data/upload", files={"file": ("AAPL.csv", file, "text/csv")})
        assert response.status_code == 200
        assert response.json()["status"] == "uploaded"
        assert response.json()["filename"] == "AAPL.csv"

def test_load_data(mock_data_file):
    response = client.get("/data/load?symbol=AAPL")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["symbol"] == "AAPL"
    assert "close" in data[0]  # Ensure that the "close" column exists

def test_load_data_file_not_found():
    response = client.get("/data/load?symbol=INVALID")
    assert response.status_code == 200
    assert response.json() == {"error": "Data file not found"}
