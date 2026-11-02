"""Helpers for adding macroeconomic regimes to financial charts."""

from __future__ import annotations

import pandas as pd


def recession_spans(indicator: pd.Series) -> list[tuple[pd.Timestamp, pd.Timestamp]]:
    """Convert a binary recession indicator into contiguous date spans."""
    active = indicator.fillna(0).astype(bool)
    starts = active & ~active.shift(1, fill_value=False)
    ends = active & ~active.shift(-1, fill_value=False)
    return list(zip(indicator.index[starts], indicator.index[ends]))
