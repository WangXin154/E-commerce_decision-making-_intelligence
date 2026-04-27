from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components


# =========================================================
# Import fallback
# =========================================================
try:
    from utils.market_data import (
        INDEX_OPTIONS,
        build_demo_chart,
        format_market_number,
        format_market_percent,
        load_market_chart,
    )
except ModuleNotFoundError:
    DASHBOARD_ROOT = Path(__file__).resolve().parents[1]
    if str(DASHBOARD_ROOT) not in sys.path:
        sys.path.append(str(DASHBOARD_ROOT))

    from utils.market_data import (
        INDEX_OPTIONS,
        build_demo_chart,
        format_market_number,
        format_market_percent,
        load_market_chart,
    )


# =========================================================
# Page config
# =========================================================
st.set_page_config(
    page_title="Nasdaq Monitor",
    page_icon="ND",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# Helpers
# =========================================================
def build_intraday_chart(price_df: pd.DataFrame, summary: dict) -> go.Figure:
    line_color = "#16a34a" if (summary.get("change") or 0) >= 0 else "#dc2626"

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=price_df["time"],
            y=price_df["price"],
            mode="lines",
            name="Price",
            line=dict(color=line_color, width=2),
            hovertemplate="%{x}<br>Price: %{y:,.2f}<extra></extra>",
        )
    )

    previous_close = summary.get("previous_close")
    if previous_close is not None:
        fig.add_hline(
            y=previous_close,
            line_dash="dash",
            line_color="#64748b",
            annotation_text="Previous close",
            annotation_position="top left",
        )

    fig.update_layout(
        height=460,
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis_title="Time",
        yaxis_title=f"Index ({summary.get('currency', 'USD')})",
        hovermode="x unified",
    )
    return fig


def build_volume_chart(price_df: pd.DataFrame, summary: dict) -> go.Figure:
    bar_color = "#22c55e" if (summary.get("change") or 0) >= 0 else "#ef4444"

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=price_df["time"],
            y=price_df["volume"],
            name="Volume",
            marker_color=bar_color,
            opacity=0.72,
            hovertemplate="%{x}<br>Volume: %{y:,.0f}<extra></extra>",
        )
    )
    fig.update_layout(
        height=260,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis_title="Time",
        yaxis_title="Volume",
    )
    return fig


def inject_auto_refresh(enabled: bool, seconds: int) -> None:
    if not enabled:
        return

    components.html(
        f"""
        <script>
        setTimeout(function() {{
            window.parent.location.reload();
        }}, {seconds * 1000});
        </script>
        """,
        height=0,
    )


# =========================================================
# Sidebar
# =========================================================
with st.sidebar:
    st.page_link("Home.py", label="Home")
    st.page_link("pages/1_User_Insights.py", label="User Insights")
    st.page_link("pages/2_Recommendation_System.py", label="Recommendation System")
    st.page_link("pages/3_Product_Performance.py", label="Product Performance")
    st.page_link("pages/4_Geographic_Analysis.py", label="Geographic Analysis")
    st.page_link("pages/5_Nasdaq_Monitor.py", label="Nasdaq Monitor")

    st.markdown("---")
    st.header("Navigation")
    st.success("Current page: Nasdaq Monitor")

    st.markdown(
        """
        **Dashboard focus**
        - Near real-time index tracking
        - Intraday price movement
        - Volume monitoring
        - Market status notes
        """
    )


# =========================================================
# Controls
# =========================================================
st.title("Nasdaq Near Real-Time Monitor")
st.caption(
    "A lightweight watch board inspired by the article's market dashboard pattern: "
    "frequent polling, clear price state, intraday trend, and source transparency."
)

control_col1, control_col2, control_col3, control_col4 = st.columns([1.2, 1, 1, 1])

with control_col1:
    index_name = st.selectbox("Index", list(INDEX_OPTIONS.keys()), index=0)

with control_col2:
    interval = st.selectbox("Granularity", ["1m", "2m", "5m", "15m"], index=0)

with control_col3:
    refresh_seconds = st.selectbox("Refresh", [15, 30, 60, 120], index=1, format_func=lambda x: f"{x}s")

with control_col4:
    auto_refresh = st.toggle("Auto refresh", value=True)

use_demo_fallback = st.checkbox("Use demo data when live source is unavailable", value=True)
manual_refresh = st.button("Refresh now", type="primary")
if manual_refresh:
    load_market_chart.clear()

selected = INDEX_OPTIONS[index_name]
symbol = selected["symbol"]


# =========================================================
# Data loading
# =========================================================
try:
    price_df, summary = load_market_chart(symbol, range_value="1d", interval=interval)
    load_error = None
except Exception as exc:
    load_error = exc
    if use_demo_fallback:
        price_df, summary = build_demo_chart(symbol)
    else:
        st.error("Unable to load live Nasdaq market data.")
        st.exception(exc)
        st.stop()

inject_auto_refresh(auto_refresh, refresh_seconds)


# =========================================================
# Status and KPI cards
# =========================================================
if load_error is not None:
    st.warning(
        "Live data source is temporarily unavailable, so the page is showing local demo data. "
        f"Reason: {load_error}"
    )

latest_time = price_df["time"].iloc[-1] if not price_df.empty else None
price = summary.get("price")
change = summary.get("change")
change_pct = summary.get("change_pct")
delta_label = None
if change is not None and change_pct is not None:
    delta_label = f"{change:+,.2f} ({change_pct:+.2f}%)"

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.metric(index_name, format_market_number(price), delta=delta_label)
with kpi2:
    st.metric("Previous Close", format_market_number(summary.get("previous_close")))
with kpi3:
    st.metric("Day Range", f"{format_market_number(summary.get('day_low'))} - {format_market_number(summary.get('day_high'))}")
with kpi4:
    st.metric("Volume", format_market_number(summary.get("volume"), decimals=0))

meta_col1, meta_col2, meta_col3 = st.columns([1, 1, 1.2])
with meta_col1:
    st.write(f"**Symbol:** `{symbol}`")
with meta_col2:
    st.write(f"**Timezone:** {summary.get('timezone', 'N/A')}")
with meta_col3:
    st.write(f"**Last point:** {latest_time if latest_time is not None else 'N/A'}")


# =========================================================
# Charts
# =========================================================
st.markdown("---")
chart_col, side_col = st.columns([2.4, 1])

with chart_col:
    st.markdown("### Intraday Price")
    st.plotly_chart(build_intraday_chart(price_df, summary), use_container_width=True)

with side_col:
    st.markdown("### Market Pulse")
    st.metric("Change %", format_market_percent(change_pct))
    st.metric("Latest Tick", format_market_number(price))
    st.metric("Data Points", format_market_number(len(price_df), decimals=0))
    st.info(
        "Free public market feeds can be delayed or throttled. Treat this board as monitoring "
        "and analysis support, not as trading infrastructure."
    )

st.markdown("### Intraday Volume")
st.plotly_chart(build_volume_chart(price_df, summary), use_container_width=True)


# =========================================================
# Data transparency
# =========================================================
st.markdown("---")
with st.expander("Data source and raw ticks", expanded=False):
    st.markdown(
        f"""
        **Primary source:** {summary.get("data_source")}  
        **Reference page:** [{selected["label"]} on Sina Finance]({selected["sina_url"]})  
        **Symbol:** `{symbol}`  
        **Interval:** `{interval}`  
        **Auto refresh:** `{auto_refresh}` every `{refresh_seconds}` seconds
        """
    )
    st.dataframe(price_df.sort_values("time", ascending=False), use_container_width=True, hide_index=True)
