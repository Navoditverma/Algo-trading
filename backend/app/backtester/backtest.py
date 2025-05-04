# backend/app/backtester/backtest.py

import pandas as pd
import numpy as np
from app.strategies import bollinger, momentum, sma_crossover  # import your strategies

class Backtester:
    def __init__(self, data: pd.DataFrame, strategy_name: str):
        self.data = data
        self.strategy_name = strategy_name
        self.initial_balance = 10000  # starting capital
        self.balance = self.initial_balance
        self.position = 0  # current position in the market (0 = no position, 1 = in position)
        self.trade_history = []  # to store trade details
        self.performance_metrics = None

    def apply_strategy(self):
        if self.strategy_name == "bollinger_band":
            return bollinger.bollinger_bands_strategy(self.data)
        elif self.strategy_name == "momentum":
            return momentum.momentum_strategy(self.data)
        elif self.strategy_name == "sma_crossover":
            return sma_crossover.sma_crossover_strategy(self.data)
        else:
            raise ValueError(f"Strategy {self.strategy_name} not recognized")

    def execute_trade(self, signal: int, price: float):
        # If signal is 1 (buy)
        if signal == 1 and self.position == 0:
            # Buying, assuming 100% of capital is used
            quantity = self.balance / price
            self.balance = 0  # capital is now used to buy
            self.position = quantity
            self.trade_history.append({"action": "buy", "price": price, "quantity": quantity})
        
        # If signal is -1 (sell)
        elif signal == -1 and self.position > 0:
            # Selling all positions
            self.balance = self.position * price  # cash from selling
            self.position = 0  # no position anymore
            self.trade_history.append({"action": "sell", "price": price, "quantity": quantity})

    def backtest(self):
        # Apply the selected strategy
        self.data = self.apply_strategy()
        
        for index, row in self.data.iterrows():
            signal = row['signal']
            price = row['close']
            self.execute_trade(signal, price)

        # Calculate performance metrics
        self.calculate_performance()
        
        return self.balance, self.trade_history

    def calculate_performance(self):
        # Calculate profit/loss and other metrics here
        total_profit_loss = self.balance - self.initial_balance
        total_returns = total_profit_loss / self.initial_balance
        self.performance_metrics = {
            "total_profit_loss": total_profit_loss,
            "total_returns": total_returns,
        }

    def get_performance_metrics(self):
        return self.performance_metrics
