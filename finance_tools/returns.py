"""Core return and risk calculations."""

from __future__ import annotations

import numpy as np
import pandas as pd


def simple_returns(prices: pd.Series | pd.DataFrame) -> pd.Series | pd.DataFrame:
    """Calculate period-over-period simple returns."""
    return prices.pct_change(fill_method=None)


def log_returns(prices: pd.Series | pd.DataFrame) -> pd.Series | pd.DataFrame:
    """Calculate continuously compounded returns."""
    return np.log(prices / prices.shift(1))


def cumulative_percentage_return(
    prices: pd.Series | pd.DataFrame,
) -> pd.Series | pd.DataFrame:
    """Rebase each price series to zero-percent growth at its first valid value."""
    first = prices.apply(lambda column: column.dropna().iloc[0]) if isinstance(prices, pd.DataFrame) else prices.dropna().iloc[0]
    return (prices.divide(first) - 1.0) * 100.0


def annualized_volatility(
    returns: pd.Series | pd.DataFrame,
    periods_per_year: int = 252,
) -> pd.Series | float:
    """Annualize sample standard deviation using the square-root-of-time rule."""
    return returns.std(ddof=1) * np.sqrt(periods_per_year)


def drawdown(prices: pd.Series | pd.DataFrame) -> pd.Series | pd.DataFrame:
    """Calculate decline from the running peak."""
    return prices.divide(prices.cummax()) - 1.0
