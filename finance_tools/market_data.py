"""Download public market and macroeconomic data."""

from __future__ import annotations

from datetime import date, datetime, timezone
from io import StringIO
from typing import Iterable

import pandas as pd
import requests


def _unix_seconds(value: str | date | datetime) -> int:
    timestamp = pd.Timestamp(value)
    if timestamp.tzinfo is None:
        timestamp = timestamp.tz_localize("UTC")
    return int(timestamp.timestamp())


def download_yahoo_prices(
    tickers: Iterable[str],
    start: str | date | datetime,
    end: str | date | datetime | None = None,
    *,
    adjusted: bool = True,
    timeout: int = 30,
) -> pd.DataFrame:
    """Return daily closing prices from Yahoo's public chart endpoint.

    The end date is exclusive. Missing observations remain missing so callers
    can choose an explicit alignment policy instead of silently filling data.
    """
    symbols = list(dict.fromkeys(symbol.upper().strip() for symbol in tickers))
    if not symbols:
        raise ValueError("Provide at least one ticker.")

    end_value = end or datetime.now(timezone.utc)
    frames: list[pd.Series] = []
    for symbol in symbols:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        params = {
            "period1": _unix_seconds(start),
            "period2": _unix_seconds(end_value),
            "interval": "1d",
            "events": "div,splits",
        }
        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        payload = response.json()
        error = payload["chart"].get("error")
        if error:
            raise RuntimeError(f"Yahoo returned an error for {symbol}: {error}")

        result = payload["chart"]["result"][0]
        timestamps = pd.to_datetime(result["timestamp"], unit="s", utc=True).tz_localize(None)
        quote = result["indicators"]["quote"][0]
        values = quote["close"]
        if adjusted:
            adjclose = result["indicators"].get("adjclose")
            if adjclose:
                values = adjclose[0]["adjclose"]
        frames.append(pd.Series(values, index=timestamps, name=symbol, dtype="float64"))

    return pd.concat(frames, axis=1).sort_index()


def download_fred_series(
    series_id: str,
    *,
    start: str | date | datetime | None = None,
    end: str | date | datetime | None = None,
    timeout: int = 30,
) -> pd.Series:
    """Download a FRED series as numeric observations without an API key."""
    url = "https://fred.stlouisfed.org/graph/fredgraph.csv"
    response = requests.get(url, params={"id": series_id}, timeout=timeout)
    response.raise_for_status()
    frame = pd.read_csv(StringIO(response.text))
    frame.columns = ["date", series_id]
    frame["date"] = pd.to_datetime(frame["date"])
    values = pd.to_numeric(frame[series_id], errors="coerce")
    series = pd.Series(values.to_numpy(), index=frame["date"], name=series_id).dropna()
    if start is not None:
        series = series.loc[pd.Timestamp(start) :]
    if end is not None:
        series = series.loc[: pd.Timestamp(end)]
    return series
