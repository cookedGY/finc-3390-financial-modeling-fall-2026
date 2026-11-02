"""Compare broad US stocks, international stocks, bonds, and gold."""

import matplotlib.pyplot as plt

from finance_tools.market_data import download_fred_series, download_yahoo_prices
from finance_tools.plotting import plot_growth_comparison
from finance_tools.validation import validate_prices


prices = download_yahoo_prices(
    ["SPY", "EFA", "AGG", "GLD"],
    start="2020-01-01",
)
validate_prices(prices)
recessions = download_fred_series("USREC", start=prices.index.min())

plot_growth_comparison(
    prices,
    recession_indicator=recessions,
    title="Growth of $1: Stocks, Bonds, and Gold",
)
plt.tight_layout()
plt.show()
