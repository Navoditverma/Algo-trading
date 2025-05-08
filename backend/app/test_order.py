from app.services.alpaca_client import place_order

# Test parameters
symbol = "AAPL"  # or "BTC/USD" if crypto
qty = 1
side = "buy"

result = place_order(symbol, qty, side)
print("Order Result:", result)
