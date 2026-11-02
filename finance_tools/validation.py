"""Basic validation checks for downloaded financial data."""

from __future__ import annotations

import pandas as pd


def validate_prices(prices: pd.DataFrame) -> None:
    """Raise a clear error when a price table is unusable."""
    if prices.empty:
        raise ValueError("The price table is empty.")
    if not isinstance(prices.index, pd.DatetimeIndex):
        raise TypeError("Price data must use a DatetimeIndex.")
    if prices.index.has_duplicates:
        raise ValueError("Price dates contain duplicates.")
    if not prices.index.is_monotonic_increasing:
        raise ValueError("Price dates must be sorted in ascending order.")
    empty_columns = prices.columns[prices.notna().sum() == 0].tolist()
    if empty_columns:
        raise ValueError(f"No observations found for: {empty_columns}")
    if (prices.dropna(how="all") <= 0).any().any():
        raise ValueError("Prices must be positive.")
