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
        format_currency,
        format_number,
        load_cluster_satisfaction_profile,
        load_final_regional_conclusion,
        load_market_type_strategy,
        load_regional_key_findings,
        load_state_clustered_results,
        to_numeric,
    )
except ModuleNotFoundError:
    DASHBOARD_ROOT = Path(__file__).resolve().parents[1]
    if str(DASHBOARD_ROOT) not in sys.path:
        sys.path.append(str(DASHBOARD_ROOT))

    from utils.data_loader import (
        find_first_existing,
        format_currency,
        format_number,
        load_cluster_satisfaction_profile,
        load_final_regional_conclusion,
        load_market_type_strategy,
        load_regional_key_findings,
        load_state_clustered_results,
        to_numeric,
    )


# =========================================================
# Page config
# =========================================================
st.set_page_config(
    page_title="Geographic Analysis",
    page_icon="🌍",
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
    st.success("Current page: Geographic Analysis")

    st.markdown(
        """
        **Dashboard focus**
        - Regional performance
        - State clustering
        - Satisfaction profile
        - Market strategy
        """
    )


# =========================================================
# Helpers
# =========================================================
def normalize_label(value) -> str:
    return str(value).strip().lower().replace("_", " ").replace("-", " ")


def prep_state_clusters(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(
            columns=[
                "state",
                "cluster",
                "gmv",
                "avg_order_value",
                "avg_delivery_days",
                "delay_rate",
                "avg_review_score",
                "bad_review_rate",
                "repeat_rate",
            ]
        )

    result = df.copy()

    state_col = find_first_existing(
        result,
        ["customer_state", "state", "buyer_state", "region_state"]
    )
    cluster_col = find_first_existing(
        result,
        ["cluster", "state_cluster", "cluster_label", "market_cluster"]
    )
    gmv_col = find_first_existing(
        result,
        ["total_gmv", "gmv", "revenue", "total_revenue", "sales"]
    )
    aov_col = find_first_existing(
        result,
        ["avg_order_value", "aov", "average_order_value"]
    )
    delivery_col = find_first_existing(
        result,
        ["avg_delivery_days", "delivery_days", "mean_delivery_days"]
    )
    delay_col = find_first_existing(
        result,
        ["delay_rate", "late_rate", "is_delayed_rate"]
    )
    review_col = find_first_existing(
        result,
        ["avg_review_score", "review_score", "avg_score"]
    )
    bad_review_col = find_first_existing(
        result,
        ["bad_review_rate", "negative_review_rate"]
    )
    repeat_col = find_first_existing(
        result,
        ["repeat_rate", "repeat_purchase_rate", "repurchase_rate"]
    )

    if state_col is None:
        raise ValueError("Could not find state column in state_clustered_results.csv.")

    if cluster_col is None:
        result["cluster"] = "Unclassified"
        cluster_col = "cluster"

    rename_map = {
        state_col: "state",
        cluster_col: "cluster",
    }

    optional_map = {
        gmv_col: "gmv",
        aov_col: "avg_order_value",
        delivery_col: "avg_delivery_days",
        delay_col: "delay_rate",
        review_col: "avg_review_score",
        bad_review_col: "bad_review_rate",
        repeat_col: "repeat_rate",
    }

    for old, new in optional_map.items():
        if old is not None:
            rename_map[old] = new

    result = result.rename(columns=rename_map)

    for col in [
        "gmv",
        "avg_order_value",
        "avg_delivery_days",
        "delay_rate",
        "avg_review_score",
        "bad_review_rate",
        "repeat_rate",
    ]:
        if col not in result.columns:
            result[col] = pd.NA
        result[col] = to_numeric(result[col])

    keep_cols = [
        "state",
        "cluster",
        "gmv",
        "avg_order_value",
        "avg_delivery_days",
        "delay_rate",
        "avg_review_score",
        "bad_review_rate",
        "repeat_rate",
    ]
    extra_cols = [c for c in result.columns if c not in keep_cols]
    return result[keep_cols + extra_cols].reset_index(drop=True)


def prep_market_strategy(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()

    result = df.copy()

    market_col = find_first_existing(
        result,
        ["market_type", "market_segment", "market_group", "type"]
    )
    strategy_col = find_first_existing(
        result,
        ["strategy", "recommended_strategy", "action_plan"]
    )

    if market_col is not None:
        result = result.rename(columns={market_col: "market_type"})
    if strategy_col is not None:
        result = result.rename(columns={strategy_col: "strategy"})

    return result.reset_index(drop=True)


def prep_final_conclusion(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()

    return df.copy().reset_index(drop=True)


def summarize_key_findings(obj) -> pd.DataFrame:
    if not obj:
        return pd.DataFrame(columns=["section", "finding"])

    rows = []

    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, list):
                for item in value:
                    rows.append({"section": str(key), "finding": str(item)})
            elif isinstance(value, dict):
                for sub_key, sub_val in value.items():
                    if isinstance(sub_val, list):
                        for item in sub_val:
                            rows.append({"section": f"{key} | {sub_key}", "finding": str(item)})
                    else:
                        rows.append({"section": f"{key} | {sub_key}", "finding": str(sub_val)})
            else:
                rows.append({"section": str(key), "finding": str(value)})

    return pd.DataFrame(rows)


def metric_mean(df: pd.DataFrame, col: str) -> float | None:
    if df.empty or col not in df.columns:
        return None
    temp = pd.to_numeric(df[col], errors="coerce").dropna()
    if temp.empty:
        return None
    return float(temp.mean())

def prep_cluster_profile(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize cluster satisfaction profile into row-wise format:
    - cluster
    - avg_review_score
    - delay_rate
    - avg_delivery_days
    - bad_review_rate

    Supported input shapes:
    1. Normal row-wise table:
       cluster | avg_review_score | delay_rate | ...
    2. Index-export table:
       Unnamed: 0 | avg_review_score | delay_rate | ...
    3. Transposed table:
       metric | Cluster 0 | Cluster 1 | Cluster 2
    """
    if df.empty:
        return pd.DataFrame(
            columns=[
                "cluster",
                "avg_review_score",
                "delay_rate",
                "avg_delivery_days",
                "bad_review_rate",
            ]
        )

    result = df.copy()

    cluster_col = find_first_existing(
        result,
        [
            "cluster",
            "state_cluster",
            "cluster_label",
            "market_cluster",
            "cluster_name",
            "unnamed: 0",
            "Unnamed: 0",
            "index",
        ]
    )

    if cluster_col is not None:
        result = result.rename(columns={cluster_col: "cluster"})

        review_col = find_first_existing(
            result,
            ["avg_review_score", "review_score", "avg_score"]
        )
        delay_col = find_first_existing(
            result,
            ["delay_rate", "late_rate", "is_delayed_rate"]
        )
        delivery_col = find_first_existing(
            result,
            ["avg_delivery_days", "delivery_days", "mean_delivery_days"]
        )
        bad_review_col = find_first_existing(
            result,
            ["bad_review_rate", "negative_review_rate"]
        )

        mapping = {
            review_col: "avg_review_score",
            delay_col: "delay_rate",
            delivery_col: "avg_delivery_days",
            bad_review_col: "bad_review_rate",
        }

        for old, new in mapping.items():
            if old is not None:
                result = result.rename(columns={old: new})

        for col in ["avg_review_score", "delay_rate", "avg_delivery_days", "bad_review_rate"]:
            if col not in result.columns:
                result[col] = pd.NA
            result[col] = to_numeric(result[col])

        keep_cols = ["cluster", "avg_review_score", "delay_rate", "avg_delivery_days", "bad_review_rate"]
        extra_cols = [c for c in result.columns if c not in keep_cols]
        return result[keep_cols + extra_cols].reset_index(drop=True)

    first_col = result.columns[0]
    first_col_values = result[first_col].astype(str).str.strip().str.lower()

    metric_alias_map = {
        "avg_review_score": "avg_review_score",
        "review_score": "avg_review_score",
        "avg_score": "avg_review_score",
        "delay_rate": "delay_rate",
        "late_rate": "delay_rate",
        "is_delayed_rate": "delay_rate",
        "avg_delivery_days": "avg_delivery_days",
        "delivery_days": "avg_delivery_days",
        "mean_delivery_days": "avg_delivery_days",
        "bad_review_rate": "bad_review_rate",
        "negative_review_rate": "bad_review_rate",
    }

    recognized_metric_count = sum(v in metric_alias_map for v in first_col_values.tolist())

    if recognized_metric_count >= 2:
        temp = result.copy()
        temp[first_col] = temp[first_col].astype(str).str.strip().str.lower()
        temp[first_col] = temp[first_col].map(lambda x: metric_alias_map.get(x, x))

        temp = temp.set_index(first_col).T.reset_index()
        temp = temp.rename(columns={"index": "cluster"})

        for col in ["avg_review_score", "delay_rate", "avg_delivery_days", "bad_review_rate"]:
            if col not in temp.columns:
                temp[col] = pd.NA
            temp[col] = to_numeric(temp[col])

        keep_cols = ["cluster", "avg_review_score", "delay_rate", "avg_delivery_days", "bad_review_rate"]
        extra_cols = [c for c in temp.columns if c not in keep_cols]
        return temp[keep_cols + extra_cols].reset_index(drop=True)

    result = result.rename(columns={first_col: "cluster"})

    review_col = find_first_existing(
        result,
        ["avg_review_score", "review_score", "avg_score"]
    )
    delay_col = find_first_existing(
        result,
        ["delay_rate", "late_rate", "is_delayed_rate"]
    )
    delivery_col = find_first_existing(
        result,
        ["avg_delivery_days", "delivery_days", "mean_delivery_days"]
    )
    bad_review_col = find_first_existing(
        result,
        ["bad_review_rate", "negative_review_rate"]
    )

    mapping = {
        review_col: "avg_review_score",
        delay_col: "delay_rate",
        delivery_col: "avg_delivery_days",
        bad_review_col: "bad_review_rate",
    }

    for old, new in mapping.items():
        if old is not None:
            result = result.rename(columns={old: new})

    for col in ["avg_review_score", "delay_rate", "avg_delivery_days", "bad_review_rate"]:
        if col not in result.columns:
            result[col] = pd.NA
        result[col] = to_numeric(result[col])

    keep_cols = ["cluster", "avg_review_score", "delay_rate", "avg_delivery_days", "bad_review_rate"]
    extra_cols = [c for c in result.columns if c not in keep_cols]
    return result[keep_cols + extra_cols].reset_index(drop=True)
# =========================================================
# Title
# =========================================================
st.title("Geographic Analysis")
st.caption(
    "Regional performance analysis, state clustering, satisfaction profile comparison, and market strategy summary."
)


# =========================================================
# Data loading
# =========================================================
try:
    raw_state_clusters = load_state_clustered_results()
    raw_cluster_profile = load_cluster_satisfaction_profile()
    raw_market_strategy = load_market_type_strategy()
    raw_final_conclusion = load_final_regional_conclusion()

    try:
        raw_key_findings = load_regional_key_findings()
    except Exception:
        raw_key_findings = {}

    state_df = prep_state_clusters(raw_state_clusters)
    cluster_profile_df = prep_cluster_profile(raw_cluster_profile)
    market_strategy_df = prep_market_strategy(raw_market_strategy)
    final_conclusion_df = prep_final_conclusion(raw_final_conclusion)
    key_findings_df = summarize_key_findings(raw_key_findings)

except Exception as e:
    st.error("Failed to load Geographic Analysis data.")
    st.exception(e)
    st.stop()


# =========================================================
# KPIs
# =========================================================
total_states = state_df["state"].nunique() if not state_df.empty else None
cluster_count = state_df["cluster"].nunique() if not state_df.empty else None
avg_review = metric_mean(state_df, "avg_review_score")
avg_delay = metric_mean(state_df, "delay_rate")

k1, k2, k3, k4 = st.columns(4)
k1.metric("States Covered", format_number(total_states, 0))
k2.metric("Clusters", format_number(cluster_count, 0))
k3.metric("Average Review Score", format_number(avg_review, 3))
k4.metric("Average Delay Rate", format_number(avg_delay, 3))


# =========================================================
# Filters
# =========================================================
st.markdown("---")
st.markdown("## Filtered View")

filter_col1, filter_col2 = st.columns(2)

selected_clusters = None
if not state_df.empty:
    with filter_col1:
        cluster_options = sorted(state_df["cluster"].dropna().astype(str).unique().tolist())
        selected_clusters = st.multiselect(
            "Select clusters",
            options=cluster_options,
            default=cluster_options,
        )

with filter_col2:
    top_n_states = st.slider("Top N states", min_value=5, max_value=27, value=10, step=1)


filtered_state_df = state_df.copy()
if selected_clusters is not None:
    filtered_state_df = filtered_state_df[filtered_state_df["cluster"].astype(str).isin(selected_clusters)]


# =========================================================
# Chart row 1
# =========================================================
st.markdown("---")
st.markdown("## Regional Cluster Structure")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown("### Cluster Distribution")
    if filtered_state_df.empty:
        st.info("No state cluster data available.")
    else:
        cluster_dist_df = (
            filtered_state_df["cluster"]
            .fillna("Unknown")
            .value_counts()
            .reset_index()
        )
        cluster_dist_df.columns = ["cluster", "state_count"]

        fig_cluster = px.pie(
            cluster_dist_df,
            names="cluster",
            values="state_count",
            hole=0.45,
        )
        fig_cluster.update_layout(
            height=420,
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(fig_cluster, use_container_width=True)

with chart_col2:
    st.markdown("### Top States by GMV")
    if filtered_state_df.empty or "gmv" not in filtered_state_df.columns:
        st.info("No GMV data available.")
    else:
        top_gmv_df = (
            filtered_state_df
            .dropna(subset=["gmv"])
            .sort_values("gmv", ascending=False)
            .head(top_n_states)
        )

        if top_gmv_df.empty:
            st.info("No usable GMV values available.")
        else:
            fig_gmv = px.bar(
                top_gmv_df,
                x="state",
                y="gmv",
                color="cluster",
                text="gmv",
            )
            fig_gmv.update_layout(
                height=420,
                xaxis_title="State",
                yaxis_title="GMV",
                margin=dict(l=20, r=20, t=40, b=20),
            )
            st.plotly_chart(fig_gmv, use_container_width=True)


# =========================================================
# Chart row 2
# =========================================================
st.markdown("---")
st.markdown("## Performance Comparison by State")

chart_col3, chart_col4 = st.columns(2)

with chart_col3:
    st.markdown("### Review Score vs Delay Rate")
    scatter_df = filtered_state_df.dropna(subset=["avg_review_score", "delay_rate"], how="any").copy()
    if scatter_df.empty:
        st.info("Scatter plot requires both review score and delay rate.")
    else:
        fig_scatter = px.scatter(
            scatter_df,
            x="delay_rate",
            y="avg_review_score",
            color="cluster",
            hover_name="state",
            size="gmv" if scatter_df["gmv"].notna().any() else None,
        )
        fig_scatter.update_layout(
            height=420,
            xaxis_title="Delay Rate",
            yaxis_title="Average Review Score",
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

with chart_col4:
    st.markdown("### Delivery Days by State")
    delivery_df = filtered_state_df.dropna(subset=["avg_delivery_days"]).copy()
    if delivery_df.empty:
        st.info("No average delivery-day data available.")
    else:
        delivery_df = delivery_df.sort_values("avg_delivery_days", ascending=False).head(top_n_states)
        fig_delivery = px.bar(
            delivery_df,
            x="state",
            y="avg_delivery_days",
            color="cluster",
            text="avg_delivery_days",
        )
        fig_delivery.update_layout(
            height=420,
            xaxis_title="State",
            yaxis_title="Average Delivery Days",
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(fig_delivery, use_container_width=True)


# =========================================================
# Cluster profile section
# =========================================================
st.markdown("---")
st.markdown("## Cluster Satisfaction Profile")

left_col, right_col = st.columns([1.2, 1])

with left_col:
    if cluster_profile_df.empty:
        st.info("No cluster satisfaction profile data available.")
    else:
        profile_plot_df = cluster_profile_df.copy()
        if selected_clusters is not None:
            profile_plot_df = profile_plot_df[
                profile_plot_df["cluster"].astype(str).isin(selected_clusters)
            ]

        plot_candidates = []
        for col in ["avg_review_score", "delay_rate", "avg_delivery_days", "bad_review_rate"]:
            if col in profile_plot_df.columns and profile_plot_df[col].notna().any():
                plot_candidates.append(col)

        if not plot_candidates:
            st.info("No numeric cluster profile metrics available.")
        else:
            melted = profile_plot_df.melt(
                id_vars="cluster",
                value_vars=plot_candidates,
                var_name="metric",
                value_name="value",
            )

            fig_profile = px.bar(
                melted,
                x="cluster",
                y="value",
                color="metric",
                barmode="group",
            )
            fig_profile.update_layout(
                height=420,
                xaxis_title="Cluster",
                yaxis_title="Metric Value",
                margin=dict(l=20, r=20, t=40, b=20),
            )
            st.plotly_chart(fig_profile, use_container_width=True)

with right_col:
    st.markdown("### Cluster Profile Table")
    if cluster_profile_df.empty:
        st.info("No cluster profile table available.")
    else:
        profile_table_df = cluster_profile_df.copy()
        if selected_clusters is not None:
            profile_table_df = profile_table_df[
                profile_table_df["cluster"].astype(str).isin(selected_clusters)
            ]
        st.dataframe(profile_table_df, use_container_width=True, hide_index=True)


# =========================================================
# Strategy and conclusion section
# =========================================================
st.markdown("---")
st.markdown("## Market Strategy and Conclusions")

bottom_col1, bottom_col2 = st.columns(2)

with bottom_col1:
    st.markdown("### Market Type Strategy")
    if market_strategy_df.empty:
        st.info("No market strategy table available.")
    else:
        st.dataframe(market_strategy_df, use_container_width=True, hide_index=True)

    st.markdown("### Key Findings")
    if key_findings_df.empty:
        st.info("No regional key findings JSON was loaded.")
    else:
        st.dataframe(key_findings_df, use_container_width=True, hide_index=True)

with bottom_col2:
    st.markdown("### Final Regional Conclusion")
    if final_conclusion_df.empty:
        st.info("No final regional conclusion data available.")
    else:
        st.dataframe(final_conclusion_df, use_container_width=True, hide_index=True)

    st.markdown("### State Cluster Table")
    if filtered_state_df.empty:
        st.info("No state cluster table available.")
    else:
        st.dataframe(
            filtered_state_df.sort_values(["cluster", "gmv"], ascending=[True, False]).head(30),
            use_container_width=True,
            hide_index=True,
        )


# =========================================================
# Raw preview
# =========================================================
st.markdown("---")
with st.expander("Preview loaded datasets", expanded=False):
    st.markdown("### State clustered results")
    st.dataframe(state_df.head(20), use_container_width=True, hide_index=True)

    st.markdown("### Cluster satisfaction profile")
    st.dataframe(cluster_profile_df.head(20), use_container_width=True, hide_index=True)

    st.markdown("### Market type strategy")
    st.dataframe(market_strategy_df.head(20), use_container_width=True, hide_index=True)

    st.markdown("### Final regional conclusion")
    st.dataframe(final_conclusion_df.head(20), use_container_width=True, hide_index=True)

    st.markdown("### Regional key findings")
    st.dataframe(key_findings_df.head(20), use_container_width=True, hide_index=True)
