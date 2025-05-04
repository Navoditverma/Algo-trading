# backend/app/trading/paper_trader.py

class PaperTrader:
    def __init__(self, initial_balance: float = 10000):
        self.balance = initial_balance
        self.positions = {}
        self.trade_history = []

    def place_order(self, symbol: str, qty: float, side: str, price: float):
        """
        Simulate placing an order.
        """
        if side == "buy":
            cost = qty * price
            if self.balance >= cost:
                self.balance -= cost
                self.positions[symbol] = self.positions.get(symbol, 0) + qty
                self.trade_history.append({"action": "buy", "symbol": symbol, "qty": qty, "price": price})
                return {"status": "success", "balance": self.balance, "positions": self.positions}
            else:
                return {"error": "Insufficient balance."}
        
        elif side == "sell":
            if symbol in self.positions and self.positions[symbol] >= qty:
                self.balance += qty * price
                self.positions[symbol] -= qty
                self.trade_history.append({"action": "sell", "symbol": symbol, "qty": qty, "price": price})
                return {"status": "success", "balance": self.balance, "positions": self.positions}
            else:
                return {"error": "Not enough positions to sell."}
        else:
            return {"error": "Invalid side."}

    def get_balance(self):
        return self.balance

    def get_positions(self):
        return self.positions

    def get_trade_history(self):
        return self.trade_history


