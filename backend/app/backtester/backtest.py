import pandas as pd
import numpy as np
from app.strategies import bollinger, momentum, sma_crossover,ml_predictor ,rsi_strategy # import your strategies

class Backtester:
    def __init__(self, data: pd.DataFrame, strategy_name: str):
        self.data = data
        self.strategy_name = strategy_name
        self.initial_balance = 10000  # starting capital
        self.balance = self.initial_balance
        self.position = 0  # number of units held
        self.trade_history = []  # to store trade details
        self.performance_metrics = None

    def apply_strategy(self):
        if self.strategy_name == "bollinger_band":
            return bollinger.bollinger_strategy(self.data)
        elif self.strategy_name == "momentum":
            return momentum.momentum_strategy(self.data)
        elif self.strategy_name == "sma_crossover":
            return sma_crossover.sma_crossover_strategy(self.data)
        elif self.strategy_name == "ml_predictor":
            df, _ = ml_predictor.ml_predictor_strategy(self.data)
            return df
        elif self.strategy_name == "rsi_strategy":
            return rsi_strategy(self.data)
        else:
            raise ValueError(f"Strategy {self.strategy_name} not recognized")

    def execute_trade(self, signal: int, price: float):
        # Buy signal
        if signal == 1 and self.position == 0:
            quantity = self.balance / price
            self.position = quantity
            self.balance = 0
            self.trade_history.append({"action": "buy", "price": price, "quantity": quantity})

        # Sell signal
        elif signal == -1 and self.position > 0:
            quantity = self.position
            self.balance = quantity * price
            self.position = 0
            self.trade_history.append({"action": "sell", "price": price, "quantity": quantity})

    def backtest(self):
        # Apply the selected strategy
        self.data = self.apply_strategy()

        for _, row in self.data.iterrows():
            signal = row['signal']
            price = row['close']
            self.execute_trade(signal, price)

        # Final liquidation if still in position
        if self.position > 0:
            final_price = self.data.iloc[-1]['close']
            quantity = self.position
            self.balance = quantity * final_price
            self.trade_history.append({"action": "final_sell", "price": final_price, "quantity": quantity})
            self.position = 0

        # Calculate performance metrics
        self.calculate_performance()
        return self.balance, self.trade_history

    def calculate_performance(self):
        total_profit_loss = self.balance - self.initial_balance
        total_returns = total_profit_loss / self.initial_balance

        # Calculate individual trade profits
        trade_profits = []
        for i in range(1, len(self.trade_history), 2):
            buy = self.trade_history[i - 1]
            sell = self.trade_history[i]
            if buy["action"] == "buy" and sell["action"] in ["sell", "final_sell"]:
                profit = (sell["price"] - buy["price"]) * buy["quantity"]
                trade_profits.append(profit)

        self.performance_metrics = {
            "total_profit_loss": total_profit_loss,
            "total_returns": total_returns,
            "individual_trade_profits": trade_profits,
            "average_trade_profit": np.mean(trade_profits) if trade_profits else 0,
            "number_of_trades": len(self.trade_history)
        }

    def get_performance_metrics(self):
        return self.performance_metrics
