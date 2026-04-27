from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional
import json

import pandas as pd
import streamlit as st


# =========================================================
# Path settings
# =========================================================
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DASHBOARD_DATA_DIR = PROJECT_ROOT / "output" / "dashboard"


# =========================================================
# Generic helpers
# =========================================================
def _ensure_file_exists(file_path: Path) -> None:
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")


@st.cache_data(show_spinner=False)
def load_csv(filename: str) -> pd.DataFrame:
    """
    Load a CSV file from output/dashboard with caching.
    """
    file_path = DASHBOARD_DATA_DIR / filename
    _ensure_file_exists(file_path)

    # utf-8-sig is safe for files exported from notebooks on Windows
    try:
        return pd.read_csv(file_path, encoding="utf-8-sig")
    except UnicodeDecodeError:
        return pd.read_csv(file_path)


@st.cache_data(show_spinner=False)
def load_json(filename: str) -> dict:
    """
    Load a JSON file from output/dashboard with caching.
    """
    file_path = DASHBOARD_DATA_DIR / filename
    _ensure_file_exists(file_path)

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def find_first_existing(df: pd.DataFrame, candidates: Iterable[str]) -> Optional[str]:
    """
    Return the first matching column name from candidates.
    Case-insensitive exact match first, then normalized match.
    """
    if df.empty:
        return None

    columns = list(df.columns)
    lower_map = {str(col).strip().lower(): col for col in columns}

    for candidate in candidates:
        key = str(candidate).strip().lower()
        if key in lower_map:
            return lower_map[key]

    # normalized fallback
    normalized_map = {
        str(col).strip().lower().replace(" ", "_").replace("-", "_"): col
        for col in columns
    }

    for candidate in candidates:
        key = str(candidate).strip().lower().replace(" ", "_").replace("-", "_")
        if key in normalized_map:
            return normalized_map[key]

    return None


def to_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def to_datetime(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, errors="coerce")


def format_number(value: float | int | None, decimals: int = 0) -> str:
    if value is None or pd.isna(value):
        return "N/A"

    if decimals == 0:
        return f"{value:,.0f}"
    return f"{value:,.{decimals}f}"


def format_currency(value: float | int | None, decimals: int = 0, symbol: str = "R$") -> str:
    if value is None or pd.isna(value):
        return "N/A"

    if decimals == 0:
        return f"{symbol} {value:,.0f}"
    return f"{symbol} {value:,.{decimals}f}"


# =========================================================
# Home page datasets
# =========================================================
def load_monthly_statistics() -> pd.DataFrame:
    return load_csv("monthly_statistics.csv")


def load_future_forecast() -> pd.DataFrame:
    return load_csv("future_30day_forecast.csv")


def load_anomalies() -> pd.DataFrame:
    return load_csv("anomalies.csv")


# =========================================================
# Other dashboard datasets
# =========================================================
def load_user_segments_rfm() -> pd.DataFrame:
    return load_csv("user_segments_rfm.csv")


def load_user_churn_scores() -> pd.DataFrame:
    return load_csv("user_churn_scores_latest_user_level.csv")


def load_high_value_high_risk_users() -> pd.DataFrame:
    return load_csv("high_value_high_risk_users.csv")


def load_customer_tier_statistics() -> pd.DataFrame:
    return load_csv("customer_tier_statistics.csv")


def load_customer_value_tiers() -> pd.DataFrame:
    return load_csv("customer_value_tiers.csv")


def load_value_risk_matrix_counts() -> pd.DataFrame:
    return load_csv("value_risk_matrix_counts.csv")


def load_roi_estimation() -> pd.DataFrame:
    return load_csv("roi_estimation.csv")


def load_final_metrics_summary() -> pd.DataFrame:
    return load_csv("final_metrics_summary.csv")


def load_recommendations_content() -> pd.DataFrame:
    return load_csv("recommendations_content.csv")


def load_recommendations_item_based() -> pd.DataFrame:
    return load_csv("recommendations_item_based.csv")


def load_recommendations_hybrid() -> pd.DataFrame:
    return load_csv("recommendations_hybrid.csv")


def load_recommendations_personalized() -> pd.DataFrame:
    return load_csv("recommendations_personalized.csv")


def load_evaluation_summary() -> pd.DataFrame:
    return load_csv("evaluation_summary_leave_one_out.csv")


def load_matrix_sparsity_summary() -> pd.DataFrame:
    return load_csv("matrix_sparsity_summary.csv")


def load_top_recommended_products() -> pd.DataFrame:
    return load_csv("top_recommended_products_debug.csv")


def load_business_impact_estimation() -> pd.DataFrame:
    return load_csv("business_impact_estimation_debug.csv")


def load_category_bcg_classification() -> pd.DataFrame:
    return load_csv("category_bcg_classification.csv")


def load_core_categories_pareto() -> pd.DataFrame:
    return load_csv("core_categories_pareto.csv")


def load_category_strategy_groups() -> dict:
    return load_json("category_strategy_groups.json")


def load_state_clustered_results() -> pd.DataFrame:
    return load_csv("state_clustered_results.csv")


def load_cluster_satisfaction_profile() -> pd.DataFrame:
    return load_csv("cluster_satisfaction_profile.csv")


def load_market_type_strategy() -> pd.DataFrame:
    return load_csv("market_type_strategy.csv")


def load_final_regional_conclusion() -> pd.DataFrame:
    return load_csv("final_regional_conclusion.csv")


def load_regional_key_findings() -> dict:
    return load_json("regional_key_findings.json")


# =========================================================
# Home page preparation logic
# =========================================================
def prepare_monthly_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize monthly statistics to:
    - period
    - order_count
    - gmv
    - avg_order_value
    """
    if df.empty:
        return pd.DataFrame(columns=["period", "order_count", "gmv", "avg_order_value"])

    result = df.copy()

    period_col = find_first_existing(
        result,
        ["year_month", "month", "period", "date", "ds"]
    )
    order_col = find_first_existing(
        result,
        ["order_count", "orders", "total_orders", "n_orders"]
    )
    gmv_col = find_first_existing(
        result,
        ["gmv", "total_gmv", "revenue", "sales", "total_revenue"]
    )
    aov_col = find_first_existing(
        result,
        ["avg_order_value", "aov", "average_order_value", "avg_gmv_per_order"]
    )

    if period_col is None:
        raise ValueError(
            "Could not find a period column in monthly_statistics.csv. "
            "Expected something like year_month / month / period / date."
        )

    result["period"] = to_datetime(result[period_col])

    if order_col is not None:
        result["order_count"] = to_numeric(result[order_col])
    else:
        result["order_count"] = pd.NA

    if gmv_col is not None:
        result["gmv"] = to_numeric(result[gmv_col])
    else:
        result["gmv"] = pd.NA

    if aov_col is not None:
        result["avg_order_value"] = to_numeric(result[aov_col])
    else:
        # fallback: derive from gmv / orders when possible
        if order_col is not None and gmv_col is not None:
            result["avg_order_value"] = result["gmv"] / result["order_count"].replace(0, pd.NA)
        else:
            result["avg_order_value"] = pd.NA

    result = result.sort_values("period").reset_index(drop=True)
    return result[["period", "order_count", "gmv", "avg_order_value"]]


def prepare_future_forecast(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize forecast data to:
    - forecast_date
    - forecast_value
    - lower_bound (optional)
    - upper_bound (optional)
    """
    if df.empty:
        return pd.DataFrame(columns=["forecast_date", "forecast_value", "lower_bound", "upper_bound"])

    result = df.copy()

    date_col = find_first_existing(result, ["date", "ds", "forecast_date"])
    value_col = find_first_existing(result, ["forecast", "yhat", "predicted_gmv", "prediction", "forecast_value"])
    lower_col = find_first_existing(result, ["yhat_lower", "lower_bound", "forecast_lower"])
    upper_col = find_first_existing(result, ["yhat_upper", "upper_bound", "forecast_upper"])

    if date_col is None or value_col is None:
        raise ValueError(
            "Could not find required columns in future_30day_forecast.csv. "
            "Expected date/ds and forecast/yhat."
        )

    result["forecast_date"] = to_datetime(result[date_col])
    result["forecast_value"] = to_numeric(result[value_col])
    result["lower_bound"] = to_numeric(result[lower_col]) if lower_col else pd.NA
    result["upper_bound"] = to_numeric(result[upper_col]) if upper_col else pd.NA

    result = result.sort_values("forecast_date").reset_index(drop=True)
    return result[["forecast_date", "forecast_value", "lower_bound", "upper_bound"]]


def prepare_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize anomalies to:
    - date
    - residual
    """
    if df.empty:
        return pd.DataFrame(columns=["date", "residual"])

    result = df.copy()

    date_col = find_first_existing(result, ["date", "ds"])
    residual_col = find_first_existing(result, ["residual", "anomaly_score", "score"])

    if date_col is None or residual_col is None:
        raise ValueError(
            "Could not find required columns in anomalies.csv. "
            "Expected date and residual."
        )

    result["date"] = to_datetime(result[date_col])
    result["residual"] = to_numeric(result[residual_col])

    result = result.sort_values("date").reset_index(drop=True)
    return result[["date", "residual"]]


def calculate_home_kpis(monthly_df: pd.DataFrame, forecast_df: pd.DataFrame) -> dict:
    """
    Calculate KPI dictionary for Home page.
    """
    total_orders = monthly_df["order_count"].sum(min_count=1)
    total_gmv = monthly_df["gmv"].sum(min_count=1)

    avg_order_value = None
    if pd.notna(total_orders) and total_orders not in [0, None] and pd.notna(total_gmv):
        avg_order_value = total_gmv / total_orders

    latest_month_gmv = None
    previous_month_gmv = None
    latest_month_orders = None

    valid_gmv = monthly_df["gmv"].dropna()
    valid_orders = monthly_df["order_count"].dropna()

    if len(valid_gmv) >= 1:
        latest_month_gmv = monthly_df["gmv"].iloc[-1]
    if len(valid_gmv) >= 2:
        previous_month_gmv = monthly_df["gmv"].iloc[-2]
    if len(valid_orders) >= 1:
        latest_month_orders = monthly_df["order_count"].iloc[-1]

    forecast_30d_gmv = forecast_df["forecast_value"].sum(min_count=1) if not forecast_df.empty else None

    gmv_change_pct = None
    if previous_month_gmv not in [None, 0] and pd.notna(previous_month_gmv) and pd.notna(latest_month_gmv):
        gmv_change_pct = ((latest_month_gmv - previous_month_gmv) / previous_month_gmv) * 100

    return {
        "total_orders": total_orders,
        "total_gmv": total_gmv,
        "avg_order_value": avg_order_value,
        "latest_month_orders": latest_month_orders,
        "latest_month_gmv": latest_month_gmv,
        "forecast_30d_gmv": forecast_30d_gmv,
        "gmv_change_pct": gmv_change_pct,
    }


def get_available_dashboard_files() -> list[str]:
    if not DASHBOARD_DATA_DIR.exists():
        return []
    return sorted([p.name for p in DASHBOARD_DATA_DIR.iterdir() if p.is_file()])