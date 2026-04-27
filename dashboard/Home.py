from __future__ import annotations

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.data_loader import (
    DASHBOARD_DATA_DIR,
    calculate_home_kpis,
    format_currency,
    format_number,
    get_available_dashboard_files,
    load_anomalies,
    load_future_forecast,
    load_monthly_statistics,
    prepare_anomalies,
    prepare_future_forecast,
    prepare_monthly_statistics,
)


# =========================================================
# Page config
# =========================================================
st.set_page_config(
    page_title="E-commerce Intelligent Decision Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# Local helpers
# =========================================================
def safe_delta_text(delta_value: float | None) -> str:
    if delta_value is None or pd.isna(delta_value):
        return None
    return f"{delta_value:+.1f}% vs previous month"


def show_data_status() -> None:
    with st.expander("Data source status", expanded=False):
        st.write(f"Dashboard data folder: `{DASHBOARD_DATA_DIR}`")
        files = get_available_dashboard_files()

        if not files:
            st.warning("No files found in output/dashboard.")
            return

        st.dataframe(
            pd.DataFrame({"filename": files}),
            use_container_width=True,
            hide_index=True
        )


def build_forecast_chart(forecast_df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()

    has_bounds = (
        "lower_bound" in forecast_df.columns and
        "upper_bound" in forecast_df.columns and
        forecast_df["lower_bound"].notna().any() and
        forecast_df["upper_bound"].notna().any()
    )

    if has_bounds:
        fig.add_trace(
            go.Scatter(
                x=forecast_df["forecast_date"],
                y=forecast_df["upper_bound"],
                mode="lines",
                line=dict(width=0),
                name="Upper Bound",
                showlegend=False,
                hoverinfo="skip",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=forecast_df["forecast_date"],
                y=forecast_df["lower_bound"],
                mode="lines",
                fill="tonexty",
                line=dict(width=0),
                name="Forecast Range",
                hoverinfo="skip",
            )
        )

    fig.add_trace(
        go.Scatter(
            x=forecast_df["forecast_date"],
            y=forecast_df["forecast_value"],
            mode="lines+markers",
            name="Forecasted GMV",
        )
    )

    fig.update_layout(
        height=420,
        xaxis_title="Forecast Date",
        yaxis_title="Forecasted GMV",
        margin=dict(l=20, r=20, t=40, b=20),
        legend_title_text="Series",
    )
    return fig


def build_anomaly_chart(anomalies_df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=anomalies_df["date"],
            y=anomalies_df["residual"],
            name="Residual",
        )
    )

    fig.add_hline(y=0, line_dash="dash")

    fig.update_layout(
        height=420,
        xaxis_title="Date",
        yaxis_title="Residual",
        margin=dict(l=20, r=20, t=40, b=20),
    )
    return fig


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
    st.success("Current page: Home")

    st.markdown(
        """
        **Dashboard focus**
        - Business overview
        - Trend monitoring
        - Forecast tracking
        - Anomaly review
        """
    )


# =========================================================
# Header
# =========================================================
st.title("E-commerce Intelligent Decision Dashboard")
st.caption(
    "Integrated business overview for order trends, GMV performance, forecast monitoring, "
    "and anomaly detection."
)


# =========================================================
# Data loading
# =========================================================
try:
    raw_monthly = load_monthly_statistics()
    raw_forecast = load_future_forecast()
    raw_anomalies = load_anomalies()

    monthly_df = prepare_monthly_statistics(raw_monthly)
    forecast_df = prepare_future_forecast(raw_forecast)
    anomalies_df = prepare_anomalies(raw_anomalies)

    kpis = calculate_home_kpis(monthly_df, forecast_df)

except Exception as e:
    st.error("Failed to load dashboard data.")
    st.exception(e)
    show_data_status()
    st.stop()


# =========================================================
# Top summary block
# =========================================================
st.markdown("## Business Overview")

summary_col1, summary_col2 = st.columns([2.2, 1])

with summary_col1:
    st.info(
        "This dashboard summarizes the current e-commerce performance from time-series outputs, "
        "including monthly business trends, short-term sales forecast, and anomaly monitoring."
    )

with summary_col2:
    latest_month_label = (
        monthly_df["period"].max().strftime("%Y-%m")
        if not monthly_df.empty and monthly_df["period"].notna().any()
        else "N/A"
    )
    st.markdown(
        f"""
        **Latest month:** {latest_month_label}  
        **Observed periods:** {len(monthly_df)}  
        **Forecast horizon:** {len(forecast_df)} days  
        **Anomaly records:** {len(anomalies_df)}
        """
    )


# =========================================================
# KPI row
# =========================================================
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        label="Total Orders",
        value=format_number(kpis["total_orders"], 0),
    )

with kpi2:
    st.metric(
        label="Total GMV",
        value=format_currency(kpis["total_gmv"], 0, symbol="R$"),
        delta=safe_delta_text(kpis["gmv_change_pct"]),
    )

with kpi3:
    st.metric(
        label="Average Order Value",
        value=format_currency(kpis["avg_order_value"], 2, symbol="R$"),
    )

with kpi4:
    st.metric(
        label="Next 30-Day Forecast",
        value=format_currency(kpis["forecast_30d_gmv"], 0, symbol="R$"),
    )


# =========================================================
# Main trend charts
# =========================================================
st.markdown("---")
st.markdown("## Performance Trends")

trend_col1, trend_col2 = st.columns(2)

with trend_col1:
    st.markdown("### Monthly GMV Trend")
    fig_gmv = px.line(
        monthly_df,
        x="period",
        y="gmv",
        markers=True,
    )
    fig_gmv.update_layout(
        height=420,
        xaxis_title="Month",
        yaxis_title="GMV",
        margin=dict(l=20, r=20, t=40, b=20),
    )
    st.plotly_chart(fig_gmv, use_container_width=True)

with trend_col2:
    st.markdown("### Monthly Order Trend")
    fig_orders = px.bar(
        monthly_df,
        x="period",
        y="order_count",
    )
    fig_orders.update_layout(
        height=420,
        xaxis_title="Month",
        yaxis_title="Order Count",
        margin=dict(l=20, r=20, t=40, b=20),
    )
    st.plotly_chart(fig_orders, use_container_width=True)


# =========================================================
# Forecast and anomalies
# =========================================================
st.markdown("---")
st.markdown("## Forecast and Monitoring")

monitor_col1, monitor_col2 = st.columns(2)

with monitor_col1:
    st.markdown("### 30-Day Forecast")
    if forecast_df.empty:
        st.warning("No forecast data available.")
    else:
        st.plotly_chart(build_forecast_chart(forecast_df), use_container_width=True)

with monitor_col2:
    st.markdown("### Detected Anomalies")
    if anomalies_df.empty:
        st.info("No anomaly records found.")
    else:
        st.plotly_chart(build_anomaly_chart(anomalies_df), use_container_width=True)


# =========================================================
# Bottom insight section
# =========================================================
st.markdown("---")
st.markdown("## Key Insights")

insight_col1, insight_col2 = st.columns([1.4, 1])

with insight_col1:
    latest_month_gmv = kpis.get("latest_month_gmv")
    latest_month_orders = kpis.get("latest_month_orders")
    forecast_30d_gmv = kpis.get("forecast_30d_gmv")
    gmv_change_pct = kpis.get("gmv_change_pct")

    st.markdown(
        f"""
        - The dashboard currently covers **{len(monthly_df)} observed monthly periods**.
        - Total observed GMV is **{format_currency(kpis["total_gmv"], 0, symbol="R$")}**, based on **{format_number(kpis["total_orders"], 0)} orders**.
        - The latest monthly GMV is **{format_currency(latest_month_gmv, 0, symbol="R$")}**, with **{format_number(latest_month_orders, 0)} orders**.
        - The next 30-day forecast suggests a projected GMV of **{format_currency(forecast_30d_gmv, 0, symbol="R$")}**.
        - Month-over-month GMV change is **{safe_delta_text(gmv_change_pct) or 'N/A'}**.
        """
    )

with insight_col2:
    st.markdown("### Recent anomaly preview")
    if anomalies_df.empty:
        st.info("No anomaly data available.")
    else:
        preview_df = anomalies_df.sort_values("date", ascending=False).head(10).copy()
        st.dataframe(preview_df, use_container_width=True, hide_index=True)


# =========================================================
# Raw data preview
# =========================================================
st.markdown("---")
with st.expander("Preview loaded datasets", expanded=False):
    st.markdown("### Monthly statistics")
    st.dataframe(monthly_df, use_container_width=True, hide_index=True)

    st.markdown("### Forecast")
    st.dataframe(forecast_df, use_container_width=True, hide_index=True)

    st.markdown("### Anomalies")
    st.dataframe(anomalies_df, use_container_width=True, hide_index=True)


show_data_status()
