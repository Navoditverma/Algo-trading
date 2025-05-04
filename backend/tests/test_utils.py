# tests/test_utils.py

import pytest
from app.utils.indicators import calculate_sma, calculate_bollinger_bands
from app.utils.time_utils import convert_to_datetime

def test_calculate_sma():
    prices = [150, 152, 154, 155, 157]
    window = 3
    sma_values = calculate_sma(prices, window)
    assert len(sma_values) == 3  # Only 3 values should be returned for window=3
    assert sma_values == [152.0, 153.66666666666666, 155.33333333333334]

def test_calculate_bollinger_bands():
    prices = [150, 152, 154, 155, 157]
    window = 3
    sma, upper_band, lower_band = calculate_bollinger_bands(prices, window)
    assert len(sma) == 3
    assert len(upper_band) == 3
    assert len(lower_band) == 3
    assert upper_band[0] > sma[0]
    assert lower_band[0] < sma[0]

def test_convert_to_datetime():
    date_str = "2022-01-01"
    date_obj = convert_to_datetime(date_str)
    assert date_obj.year == 2022
    assert date_obj.month == 1
    assert date_obj.day == 1
