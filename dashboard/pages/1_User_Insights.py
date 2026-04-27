from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# =========================================================
# Import fallback
# =========================================================
try:
    from utils.data_loader import (
        find_first_existing,
        format_number,
        load_customer_tier_statistics,
        load_customer_value_tiers,
        load_final_metrics_summary,
        load_high_value_high_risk_users,
        load_roi_estimation,
        load_user_churn_scores,
        load_user_segments_rfm,
        load_value_risk_matrix_counts,
        to_numeric,
    )
except ModuleNotFoundError:
    DASHBOARD_ROOT = Path(__file__).resolve().parents[1]
    if str(DASHBOARD_ROOT) not in sys.path:
        sys.path.append(str(DASHBOARD_ROOT))

    from utils.data_loader import (
        find_first_existing,
        format_number,
        load_customer_tier_statistics,
        load_customer_value_tiers,
        load_final_metrics_summary,
        load_high_value_high_risk_users,
        load_roi_estimation,
        load_user_churn_scores,
        load_user_segments_rfm,
        load_value_risk_matrix_counts,
        to_numeric,
    )


# =========================================================
# Page config
# =========================================================
st.set_page_config(
    page_title="User Insights",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded",
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
    st.success("Current page: User Insights")

    st.markdown(
        """
        **Dashboard focus**
        - Customer segmentation
        - Churn monitoring
        - CLV tiers
        - Value-risk prioritization
        """
    )


# =========================================================
# Helpers
# =========================================================
def normalize_label(value) -> str:
    return str(value).strip().lower().replace("_", " ").replace("-", " ")


def prep_rfm(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["segment", "user_count"])

    result = df.copy()

    segment_col = find_first_existing(
        result,
        [
            "segment",
            "rfm_segment",
            "customer_segment",
            "user_segment",
            "segment_name",
            "rfm_label",
        ],
    )

    user_col = find_first_existing(
        result,
        [
            "unique_user_id",
            "user_id",
            "customer_id",
            "customer_unique_id",
        ],
    )

    count_col = find_first_existing(
        result,
        [
            "user_count",
            "customer_count",
            "count",
            "n_users",
        ],
    )

    if segment_col is None:
        raise ValueError("Could not find segment column in user_segments_rfm.csv.")

    if count_col is not None:
        grouped = result[[segment_col, count_col]].copy()
        grouped.columns = ["segment", "user_count"]
        grouped["user_count"] = to_numeric(grouped["user_count"])
        grouped = grouped.groupby("segment", as_index=False)["user_count"].sum()
        return grouped.sort_values("user_count", ascending=False).reset_index(drop=True)

    if user_col is not None:
        grouped = (
            result.groupby(segment_col)[user_col]
            .nunique()
            .reset_index(name="user_count")
        )
        grouped.columns = ["segment", "user_count"]
        return grouped.sort_values("user_count", ascending=False).reset_index(drop=True)

    grouped = result[segment_col].value_counts(dropna=False).reset_index()
    grouped.columns = ["segment", "user_count"]
    return grouped.sort_values("user_count", ascending=False).reset_index(drop=True)


def prep_churn(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    if df.empty:
        empty_dist = pd.DataFrame(columns=["risk_level", "user_count"])
        empty_score = pd.DataFrame(columns=["risk_level", "avg_churn_probability"])
        return empty_dist, empty_score

    result = df.copy()

    risk_col = find_first_existing(
        result,
        ["risk_level", "risk_segment", "churn_risk", "risk_label"]
    )
    prob_col = find_first_existing(
        result,
        ["churn_probability", "probability", "score", "risk_score"]
    )
    user_col = find_first_existing(
        result,
        ["unique_user_id", "user_id", "customer_id", "customer_unique_id"]
    )

    if risk_col is None:
        raise ValueError("Could not find risk level column in user_churn_scores_latest_user_level.csv.")

    if user_col is not None:
        dist_df = (
            result.groupby(risk_col)[user_col]
            .nunique()
            .reset_index(name="user_count")
        )
    else:
        dist_df = result[risk_col].value_counts(dropna=False).reset_index()
        dist_df.columns = [risk_col, "user_count"]

    dist_df.columns = ["risk_level", "user_count"]

    if prob_col is not None:
        result[prob_col] = to_numeric(result[prob_col])
        score_df = (
            result.groupby(risk_col)[prob_col]
            .mean()
            .reset_index(name="avg_churn_probability")
        )
        score_df.columns = ["risk_level", "avg_churn_probability"]
    else:
        score_df = pd.DataFrame(columns=["risk_level", "avg_churn_probability"])

    return (
        dist_df.sort_values("user_count", ascending=False).reset_index(drop=True),
        score_df.reset_index(drop=True),
    )


def prep_clv_tiers(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["tier", "user_count"])

    result = df.copy()

    tier_col = find_first_existing(
        result,
        [
            "tier",
            "customer_tier",
            "value_tier",
            "clv_tier",
            "tier_name",
            "clv_group",
            "value_group",
            "segment",
        ]
    )

    count_col = find_first_existing(
        result,
        ["user_count", "customer_count", "count", "n_users"]
    )

    user_col = find_first_existing(
        result,
        ["unique_user_id", "user_id", "customer_id", "customer_unique_id"]
    )

    if tier_col is None:
        raise ValueError("Could not find tier column in customer_value_tiers.csv or customer_tier_statistics.csv.")

    if count_col is not None:
        grouped = result[[tier_col, count_col]].copy()
        grouped.columns = ["tier", "user_count"]
        grouped["user_count"] = to_numeric(grouped["user_count"])
        grouped = grouped.groupby("tier", as_index=False)["user_count"].sum()
        return grouped.sort_values("user_count", ascending=False).reset_index(drop=True)

    if user_col is not None:
        grouped = (
            result.groupby(tier_col)[user_col]
            .nunique()
            .reset_index(name="user_count")
        )
        grouped.columns = ["tier", "user_count"]
        return grouped.sort_values("user_count", ascending=False).reset_index(drop=True)

    grouped = result[tier_col].value_counts(dropna=False).reset_index()
    grouped.columns = ["tier", "user_count"]
    return grouped.sort_values("user_count", ascending=False).reset_index(drop=True)


def prep_value_risk_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize value-risk matrix into long format:
    - value_tier
    - risk_level
    - count

    Supports both:
    1. long format:
       value_tier | risk_level | count
    2. wide crosstab format:
       clv_group  | Low Risk | High Risk | ...
    """
    if df.empty:
        return pd.DataFrame(columns=["value_tier", "risk_level", "count"])

    result = df.copy()

    # Case 1: already long format
    value_col = find_first_existing(
        result,
        ["value_tier", "tier", "customer_tier", "clv_tier", "value_segment", "clv_group"]
    )
    risk_col = find_first_existing(
        result,
        ["risk_level", "risk_segment", "churn_risk", "risk_label", "risk_group"]
    )
    count_col = find_first_existing(
        result,
        ["count", "user_count", "customer_count", "n_users"]
    )

    if value_col is not None and risk_col is not None and count_col is not None:
        matrix_df = result[[value_col, risk_col, count_col]].copy()
        matrix_df.columns = ["value_tier", "risk_level", "count"]
        matrix_df["count"] = to_numeric(matrix_df["count"]).fillna(0)
        return matrix_df

    # Case 2: wide crosstab format
    possible_index_col = find_first_existing(
        result,
        ["clv_group", "value_tier", "tier", "customer_tier", "Unnamed: 0", "index"]
    )

    if possible_index_col is None:
        possible_index_col = result.columns[0]

    wide_df = result.copy()
    wide_df = wide_df.rename(columns={possible_index_col: "value_tier"})

    risk_cols = [col for col in wide_df.columns if col != "value_tier"]

    if not risk_cols:
        raise ValueError(
            "Could not parse value_risk_matrix_counts.csv. "
            "No risk-level columns were found."
        )

    long_df = wide_df.melt(
        id_vars="value_tier",
        var_name="risk_level",
        value_name="count"
    )

    long_df["value_tier"] = long_df["value_tier"].astype(str).str.strip()
    long_df["risk_level"] = long_df["risk_level"].astype(str).str.strip()
    long_df["count"] = to_numeric(long_df["count"]).fillna(0)

    long_df = long_df[
        long_df["value_tier"].notna() &
        long_df["risk_level"].notna()
    ].reset_index(drop=True)

    return long_df


def prep_high_value_high_risk(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()

    result = df.copy()

    preferred_cols = []
    for candidates in [
        ["unique_user_id", "user_id", "customer_id", "customer_unique_id"],
        ["risk_level"],
        ["churn_probability", "probability", "risk_score"],
        ["predicted_clv", "clv", "customer_lifetime_value", "pred_clv"],
        ["tier", "value_tier", "customer_tier", "clv_tier", "clv_group"],
        ["strategy", "retention_strategy", "action_plan"],
    ]:
        col = find_first_existing(result, candidates)
        if col is not None:
            preferred_cols.append(col)

    if preferred_cols:
        result = result[preferred_cols].copy()

    rename_map = {}
    for col in result.columns:
        lower = str(col).strip().lower()
        if lower in ["unique_user_id", "user_id", "customer_id", "customer_unique_id"]:
            rename_map[col] = "user_id"
        elif lower == "risk_level":
            rename_map[col] = "risk_level"
        elif lower in ["churn_probability", "probability", "risk_score"]:
            rename_map[col] = "churn_probability"
        elif lower in ["predicted_clv", "clv", "customer_lifetime_value", "pred_clv"]:
            rename_map[col] = "predicted_clv"
        elif lower in ["tier", "value_tier", "customer_tier", "clv_tier", "clv_group"]:
            rename_map[col] = "value_tier"
        elif lower in ["strategy", "retention_strategy", "action_plan"]:
            rename_map[col] = "strategy"

    result = result.rename(columns=rename_map)

    if "churn_probability" in result.columns:
        result["churn_probability"] = to_numeric(result["churn_probability"])

    if "predicted_clv" in result.columns:
        result["predicted_clv"] = to_numeric(result["predicted_clv"])

    sort_cols = [c for c in ["predicted_clv", "churn_probability"] if c in result.columns]
    if sort_cols:
        result = result.sort_values(sort_cols, ascending=[False] * len(sort_cols))

    return result.reset_index(drop=True)


def prep_roi(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    return df.copy()


def prep_final_metrics(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    return df.copy()


def safe_metric_value(df: pd.DataFrame, candidates: list[str]) -> float | None:
    if df.empty:
        return None

    metric_col = find_first_existing(df, ["metric", "metric_name", "name"])
    value_col = find_first_existing(df, ["value", "metric_value", "score"])

    if metric_col is None or value_col is None:
        return None

    temp = df.copy()
    temp[metric_col] = temp[metric_col].astype(str).str.strip().str.lower()
    temp[value_col] = to_numeric(temp[value_col])

    candidate_set = {c.strip().lower() for c in candidates}
    matched = temp[temp[metric_col].isin(candidate_set)]

    if matched.empty:
        return None

    return matched[value_col].iloc[0]


# =========================================================
# Title
# =========================================================
st.title("User Insights")
st.caption(
    "Customer segmentation, churn monitoring, CLV tier analysis, and value-risk prioritization."
)


# =========================================================
# Data loading
# =========================================================
try:
    raw_rfm = load_user_segments_rfm()
    raw_churn = load_user_churn_scores()
    raw_hvhr = load_high_value_high_risk_users()
    raw_tier_stats = load_customer_tier_statistics()
    raw_value_tiers = load_customer_value_tiers()
    raw_value_risk = load_value_risk_matrix_counts()
    raw_roi = load_roi_estimation()
    raw_metrics = load_final_metrics_summary()

    rfm_df = prep_rfm(raw_rfm)
    churn_dist_df, churn_score_df = prep_churn(raw_churn)

    try:
        clv_from_value_tiers = prep_clv_tiers(raw_value_tiers)
    except Exception:
        clv_from_value_tiers = pd.DataFrame(columns=["tier", "user_count"])

    try:
        clv_from_tier_stats = prep_clv_tiers(raw_tier_stats)
    except Exception:
        clv_from_tier_stats = pd.DataFrame(columns=["tier", "user_count"])

    if clv_from_tier_stats["tier"].nunique() > clv_from_value_tiers["tier"].nunique():
        clv_tier_df = clv_from_tier_stats
    else:
        clv_tier_df = clv_from_value_tiers

    value_risk_df = prep_value_risk_matrix(raw_value_risk)
    hvhr_df = prep_high_value_high_risk(raw_hvhr)
    roi_df = prep_roi(raw_roi)
    final_metrics_df = prep_final_metrics(raw_metrics)

except Exception as e:
    st.error("Failed to load User Insights data.")
    st.exception(e)
    st.stop()


# =========================================================
# KPI row
# =========================================================
total_segmented_users = rfm_df["user_count"].sum() if not rfm_df.empty else None

high_risk_users = None
if not churn_dist_df.empty:
    high_risk_mask = churn_dist_df["risk_level"].astype(str).str.lower().str.contains("high")
    if high_risk_mask.any():
        high_risk_users = churn_dist_df.loc[high_risk_mask, "user_count"].sum()

high_value_high_risk_users = len(hvhr_df) if not hvhr_df.empty else None

avg_churn_prob = None
if not churn_score_df.empty and "avg_churn_probability" in churn_score_df.columns:
    avg_churn_prob = churn_score_df["avg_churn_probability"].mean()

k1, k2, k3, k4 = st.columns(4)
k1.metric("Segmented Users", format_number(total_segmented_users, 0))
k2.metric("High Risk Users", format_number(high_risk_users, 0))
k3.metric("High-Value High-Risk Users", format_number(high_value_high_risk_users, 0))
k4.metric("Average Churn Probability", format_number(avg_churn_prob, 3))


# =========================================================
# Filters
# =========================================================
st.markdown("---")
st.markdown("## Filtered View")

filter_col1, filter_col2 = st.columns(2)

selected_risk_levels = None
if not churn_dist_df.empty:
    with filter_col1:
        risk_options = sorted(churn_dist_df["risk_level"].dropna().astype(str).unique().tolist())
        selected_risk_levels = st.multiselect(
            "Select risk levels",
            options=risk_options,
            default=risk_options,
        )

selected_value_tiers = None
if not clv_tier_df.empty:
    with filter_col2:
        tier_options = sorted(clv_tier_df["tier"].dropna().astype(str).unique().tolist())
        selected_value_tiers = st.multiselect(
            "Select CLV tiers",
            options=tier_options,
            default=tier_options,
        )


# =========================================================
# Charts row 1
# =========================================================
st.markdown("---")
st.markdown("## Customer Segmentation and Risk")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown("### RFM Segment Distribution")
    if rfm_df.empty:
        st.info("No RFM data available.")
    else:
        fig_rfm = px.bar(
            rfm_df,
            x="segment",
            y="user_count",
            text="user_count",
        )
        fig_rfm.update_layout(
            height=420,
            xaxis_title="Segment",
            yaxis_title="User Count",
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(fig_rfm, use_container_width=True)

with chart_col2:
    st.markdown("### Churn Risk Distribution")
    if churn_dist_df.empty:
        st.info("No churn risk data available.")
    else:
        churn_plot_df = churn_dist_df.copy()
        if selected_risk_levels is not None:
            churn_plot_df = churn_plot_df[churn_plot_df["risk_level"].astype(str).isin(selected_risk_levels)]

        fig_churn = px.pie(
            churn_plot_df,
            names="risk_level",
            values="user_count",
            hole=0.45,
        )
        fig_churn.update_layout(
            height=420,
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(fig_churn, use_container_width=True)


# =========================================================
# Charts row 2
# =========================================================
st.markdown("---")
st.markdown("## CLV and Value-Risk Structure")

chart_col3, chart_col4 = st.columns(2)

with chart_col3:
    st.markdown("### CLV Tier Distribution")
    if clv_tier_df.empty:
        st.info("No CLV tier data available.")
    else:
        clv_plot_df = clv_tier_df.copy()
        if selected_value_tiers is not None:
            clv_plot_df = clv_plot_df[clv_plot_df["tier"].astype(str).isin(selected_value_tiers)]

        fig_clv = px.bar(
            clv_plot_df,
            x="tier",
            y="user_count",
            text="user_count",
        )
        fig_clv.update_layout(
            height=420,
            xaxis_title="CLV Tier",
            yaxis_title="User Count",
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(fig_clv, use_container_width=True)

with chart_col4:
    st.markdown("### Value-Risk Matrix")
    if value_risk_df.empty:
        st.info("No value-risk matrix data available.")
    else:
        matrix_plot_df = value_risk_df.copy()

        if selected_risk_levels is not None:
            selected_risk_norm = {normalize_label(x) for x in selected_risk_levels}
            matrix_plot_df["_risk_norm"] = matrix_plot_df["risk_level"].astype(str).map(normalize_label)

            if matrix_plot_df["_risk_norm"].isin(selected_risk_norm).any():
                matrix_plot_df = matrix_plot_df[matrix_plot_df["_risk_norm"].isin(selected_risk_norm)]

        if selected_value_tiers is not None:
            selected_tier_norm = {normalize_label(x) for x in selected_value_tiers}
            matrix_plot_df["_tier_norm"] = matrix_plot_df["value_tier"].astype(str).map(normalize_label)

            if matrix_plot_df["_tier_norm"].isin(selected_tier_norm).any():
                matrix_plot_df = matrix_plot_df[matrix_plot_df["_tier_norm"].isin(selected_tier_norm)]

        for col in ["_risk_norm", "_tier_norm"]:
            if col in matrix_plot_df.columns:
                matrix_plot_df = matrix_plot_df.drop(columns=[col])

        if matrix_plot_df.empty:
            st.warning("No records remain after filtering.")
        else:
            pivot_df = (
                matrix_plot_df.pivot_table(
                    index="value_tier",
                    columns="risk_level",
                    values="count",
                    aggfunc="sum",
                    fill_value=0,
                )
            )

            heatmap_df = pivot_df.reset_index().melt(
                id_vars="value_tier",
                var_name="risk_level",
                value_name="count",
            )

            fig_matrix = px.density_heatmap(
                heatmap_df,
                x="risk_level",
                y="value_tier",
                z="count",
                text_auto=True,
            )
            fig_matrix.update_layout(
                height=420,
                xaxis_title="Risk Level",
                yaxis_title="Value Tier",
                margin=dict(l=20, r=20, t=40, b=20),
            )
            st.plotly_chart(fig_matrix, use_container_width=True)


# =========================================================
# Priority customer list
# =========================================================
st.markdown("---")
st.markdown("## Priority Customer List")

left_col, right_col = st.columns([1.7, 1])

with left_col:
    st.markdown("### High-Value High-Risk Users")
    if hvhr_df.empty:
        st.info("No high-value high-risk user data available.")
    else:
        display_df = hvhr_df.copy()

        if selected_risk_levels is not None and "risk_level" in display_df.columns:
            display_df = display_df[display_df["risk_level"].astype(str).isin(selected_risk_levels)]

        if selected_value_tiers is not None and "value_tier" in display_df.columns:
            selected_tier_norm = {normalize_label(x) for x in selected_value_tiers}
            temp_tier_norm = display_df["value_tier"].astype(str).map(normalize_label)
            if temp_tier_norm.isin(selected_tier_norm).any():
                display_df = display_df[temp_tier_norm.isin(selected_tier_norm)]

        top_n = st.slider("Rows to display", min_value=5, max_value=30, value=10, step=5)

        st.dataframe(
            display_df.head(top_n),
            use_container_width=True,
            hide_index=True,
        )

with right_col:
    st.markdown("### ROI Summary")
    if roi_df.empty:
        st.info("No ROI estimation data available.")
    else:
        st.dataframe(roi_df, use_container_width=True, hide_index=True)


# =========================================================
# Final metrics summary
# =========================================================
st.markdown("---")
st.markdown("## Final Metrics Summary")

if final_metrics_df.empty:
    st.info("No final metrics summary data available.")
else:
    metric_candidates = {
        "Retention Rate": ["retention_rate", "expected_retention_rate"],
        "ROI": ["roi", "estimated_roi"],
        "Lift": ["lift", "uplift"],
        "Revenue Impact": ["revenue_impact", "estimated_revenue_impact"],
    }

    metric_cols = st.columns(len(metric_candidates))
    for i, (label, candidates) in enumerate(metric_candidates.items()):
        value = safe_metric_value(final_metrics_df, candidates)
        metric_cols[i].metric(label, format_number(value, 3) if value is not None else "N/A")

    st.dataframe(final_metrics_df, use_container_width=True, hide_index=True)


# =========================================================
# Raw preview
# =========================================================
st.markdown("---")
with st.expander("Preview loaded datasets", expanded=False):
    st.markdown("### RFM")
    st.dataframe(rfm_df, use_container_width=True, hide_index=True)

    st.markdown("### Churn Distribution")
    st.dataframe(churn_dist_df, use_container_width=True, hide_index=True)

    st.markdown("### CLV Tiers")
    st.dataframe(clv_tier_df, use_container_width=True, hide_index=True)

    st.markdown("### Value-Risk Matrix")
    st.dataframe(value_risk_df, use_container_width=True, hide_index=True)

    st.markdown("### High-Value High-Risk Users")
    st.dataframe(hvhr_df.head(20), use_container_width=True, hide_index=True)
