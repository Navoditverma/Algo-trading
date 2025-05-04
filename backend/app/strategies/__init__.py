# __init__.py

from .rsi_strategy import rsi_strategy
from .sma_crossover import sma_crossover_strategy
from .momentum import momentum_strategy
from .bollinger import bollinger_strategy
from .ml_predictor import ml_predictor_strategy

# Strategy registry (for dynamic loading via name)
STRATEGY_MAP = {
    "rsi": rsi_strategy,
    "sma_crossover": sma_crossover_strategy,
    "momentum": momentum_strategy,
    "bollinger": bollinger_strategy,
    "ml": ml_predictor_strategy,
}

