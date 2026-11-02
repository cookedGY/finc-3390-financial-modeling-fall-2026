"""Consistent plotting helpers for course analyses."""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.axes import Axes

from .macro import recession_spans
from .returns import cumulative_percentage_return


def plot_growth_comparison(
    prices: pd.DataFrame,
    *,
    recession_indicator: pd.Series | None = None,
    title: str = "Cumulative Growth Comparison",
    ax: Axes | None = None,
) -> Axes:
    """Plot securities in comparable cumulative percentage-growth units."""
    if ax is None:
        _, ax = plt.subplots(figsize=(12, 6))
    cumulative_percentage_return(prices).plot(ax=ax, linewidth=1.8)
    if recession_indicator is not None:
        for start, end in recession_spans(recession_indicator):
            ax.axvspan(start, end, color="gray", alpha=0.18, linewidth=0)
    ax.axhline(0, color="black", linewidth=0.8, alpha=0.6)
    ax.set(title=title, xlabel="Date", ylabel="Cumulative return (%)")
    ax.grid(alpha=0.25)
    return ax
