from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen
import json
import math
import random

import pandas as pd

try:
    import streamlit as st
except ModuleNotFoundError:
    class _StreamlitFallback:
        @staticmethod
        def cache_data(**_kwargs):
            def decorator(func):
                func.clear = lambda: None
                return func

            return decorator

    st = _StreamlitFallback()


INDEX_OPTIONS = {
    "Nasdaq Composite": {
        "symbol": "^IXIC",
        "label": "Nasdaq Composite",
        "sina_url": "https://stock.sina.com.cn/usstock/quotes/.IXIC.html",
    },
    "Nasdaq 100": {
        "symbol": "^NDX",
        "label": "Nasdaq 100",
        "sina_url": "https://stock.sina.com.cn/usstock/quotes/.NDX.html",
    },
}


def _as_float(value: Any) -> float | None:
    try:
        if value is None:
            return None
        result = float(value)
        if math.isnan(result):
            return None
        return result
    except (TypeError, ValueError):
        return None


def _fetch_yahoo_chart(symbol: str, range_value: str, interval: str) -> dict:
    encoded_symbol = quote(symbol, safe="")
    url = (
        "https://query1.finance.yahoo.com/v8/finance/chart/"
        f"{encoded_symbol}?range={range_value}&interval={interval}&includePrePost=true"
    )
    request = Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
            ),
            "Accept": "application/json",
        },
    )

    try:
        with urlopen(request, timeout=8) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raise RuntimeError(f"Yahoo Finance returned HTTP {exc.code}.") from exc
    except URLError as exc:
        raise RuntimeError(f"Unable to reach Yahoo Finance: {exc.reason}") from exc
    except TimeoutError as exc:
        raise RuntimeError("Yahoo Finance request timed out.") from exc


def _parse_chart_payload(payload: dict, symbol: str) -> tuple[pd.DataFrame, dict]:
    chart = payload.get("chart", {})
    error = chart.get("error")
    if error:
        raise RuntimeError(error.get("description") or str(error))

    results = chart.get("result") or []
    if not results:
        raise RuntimeError("Yahoo Finance did not return chart data.")

    result = results[0]
    meta = result.get("meta", {})
    timestamps = result.get("timestamp") or []
    quote_data = (result.get("indicators", {}).get("quote") or [{}])[0]

    close_values = quote_data.get("close") or []
    volume_values = quote_data.get("volume") or []

    if not timestamps or not close_values:
        raise RuntimeError("Chart payload does not contain timestamp and close series.")

    timezone_name = meta.get("exchangeTimezoneName") or "America/New_York"
    rows = []
    for index, ts in enumerate(timestamps):
        close = _as_float(close_values[index] if index < len(close_values) else None)
        if close is None:
            continue

        volume = _as_float(volume_values[index] if index < len(volume_values) else None)
        rows.append(
            {
                "time": pd.to_datetime(ts, unit="s", utc=True).tz_convert(timezone_name),
                "price": close,
                "volume": volume or 0,
            }
        )

    df = pd.DataFrame(rows)
    if df.empty:
        raise RuntimeError("No usable price rows were returned.")

    previous_close = (
        _as_float(meta.get("previousClose"))
        or _as_float(meta.get("chartPreviousClose"))
        or _as_float(df["price"].iloc[0])
    )
    latest_price = _as_float(meta.get("regularMarketPrice")) or _as_float(df["price"].iloc[-1])
    change = latest_price - previous_close if latest_price is not None and previous_close is not None else None
    change_pct = change / previous_close * 100 if change is not None and previous_close not in [None, 0] else None

    summary = {
        "symbol": symbol,
        "exchange_name": meta.get("exchangeName") or "NASDAQ",
        "currency": meta.get("currency") or "USD",
        "timezone": timezone_name,
        "regular_market_time": meta.get("regularMarketTime"),
        "price": latest_price,
        "previous_close": previous_close,
        "change": change,
        "change_pct": change_pct,
        "day_high": _as_float(meta.get("regularMarketDayHigh")) or _as_float(df["price"].max()),
        "day_low": _as_float(meta.get("regularMarketDayLow")) or _as_float(df["price"].min()),
        "volume": _as_float(meta.get("regularMarketVolume")) or _as_float(df["volume"].sum()),
        "data_source": "Yahoo Finance chart API",
        "is_demo": False,
    }
    return df, summary


@st.cache_data(ttl=30, show_spinner=False)
def load_market_chart(symbol: str, range_value: str = "1d", interval: str = "1m") -> tuple[pd.DataFrame, dict]:
    payload = _fetch_yahoo_chart(symbol, range_value, interval)
    return _parse_chart_payload(payload, symbol)


def build_demo_chart(symbol: str, points: int = 240) -> tuple[pd.DataFrame, dict]:
    seed = sum(ord(char) for char in symbol)
    random.seed(seed)

    base_price = 18500 if symbol == "^IXIC" else 21500
    start_time = datetime.now().replace(second=0, microsecond=0) - timedelta(minutes=points - 1)
    rows = []
    price = float(base_price)

    for offset in range(points):
        drift = math.sin(offset / 22) * 3.2 + random.uniform(-8.5, 8.5)
        price = max(base_price * 0.94, price + drift)
        rows.append(
            {
                "time": start_time + timedelta(minutes=offset),
                "price": price,
                "volume": int(800000 + abs(drift) * 110000 + random.randint(0, 250000)),
            }
        )

    df = pd.DataFrame(rows)
    previous_close = base_price
    latest_price = float(df["price"].iloc[-1])
    change = latest_price - previous_close
    summary = {
        "symbol": symbol,
        "exchange_name": "NASDAQ",
        "currency": "USD",
        "timezone": "Local demo time",
        "regular_market_time": None,
        "price": latest_price,
        "previous_close": previous_close,
        "change": change,
        "change_pct": change / previous_close * 100,
        "day_high": float(df["price"].max()),
        "day_low": float(df["price"].min()),
        "volume": float(df["volume"].sum()),
        "data_source": "Local simulated demo data",
        "is_demo": True,
    }
    return df, summary


def format_market_number(value: float | int | None, decimals: int = 2) -> str:
    if value is None or pd.isna(value):
        return "N/A"
    return f"{value:,.{decimals}f}"


def format_market_percent(value: float | int | None) -> str:
    if value is None or pd.isna(value):
        return "N/A"
    return f"{value:+.2f}%"
