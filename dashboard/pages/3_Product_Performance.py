from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# =========================================================
# Import fallback
# =========================================================
try:
    from utils.data_loader import (
        find_first_existing,
        format_currency,
        format_number,
        load_category_bcg_classification,
        load_category_strategy_groups,
        load_core_categories_pareto,
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
        load_category_bcg_classification,
        load_category_strategy_groups,
        load_core_categories_pareto,
        to_numeric,
    )


# =========================================================
# Page config
# =========================================================
st.set_page_config(
    page_title="Product Performance",
    page_icon="📦",
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
    st.success("Current page: Product Performance")

    st.markdown(
        """
        **Dashboard focus**
        - Category performance
        - BCG classification
        - Pareto concentration
        - Strategy grouping
        """
    )


# =========================================================
# Helpers
# =========================================================
def normalize_label(value) -> str:
    return str(value).strip().lower().replace("_", " ").replace("-", " ")


def prep_bcg(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(
            columns=["category", "bcg_group", "gmv", "order_count", "review_score"]
        )

    result = df.copy()

    category_col = find_first_existing(
        result,
        [
            "category",
            "product_category_name_english",
            "product_category_name",
            "main_category",
            "category_name",
        ],
    )

    bcg_col = find_first_existing(
        result,
        [
            "bcg_group",
            "bcg_class",
            "quadrant",
            "group",
            "strategy_group",
        ],
    )

    gmv_col = find_first_existing(
        result,
        [
            "gmv",
            "total_gmv",
            "revenue",
            "total_revenue",
            "sales",
        ],
    )

    order_col = find_first_existing(
        result,
        [
            "order_count",
            "orders",
            "total_orders",
            "purchase_count",
        ],
    )

    review_col = find_first_existing(
        result,
        [
            "avg_review_score",
            "review_score",
            "score",
            "avg_score",
        ],
    )

    if category_col is None:
        raise ValueError("Could not find category column in category_bcg_classification.csv.")

    if bcg_col is None:
        result["bcg_group"] = "Unclassified"
        bcg_col = "bcg_group"

    if gmv_col is None:
        result["gmv"] = pd.NA
        gmv_col = "gmv"

    if order_col is None:
        result["order_count"] = pd.NA
        order_col = "order_count"

    if review_col is None:
        result["review_score"] = pd.NA
        review_col = "review_score"

    result = result.rename(
        columns={
            category_col: "category",
            bcg_col: "bcg_group",
            gmv_col: "gmv",
            order_col: "order_count",
            review_col: "review_score",
        }
    )

    result["gmv"] = to_numeric(result["gmv"])
    result["order_count"] = to_numeric(result["order_count"])
    result["review_score"] = to_numeric(result["review_score"])

    keep_cols = ["category", "bcg_group", "gmv", "order_count", "review_score"]
    extra_cols = [c for c in result.columns if c not in keep_cols]
    return result[keep_cols + extra_cols].reset_index(drop=True)


def prep_pareto(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["category", "gmv", "cumulative_share"])

    result = df.copy()

    category_col = find_first_existing(
        result,
        [
            "category",
            "product_category_name_english",
            "product_category_name",
            "main_category",
            "category_name",
        ],
    )

    gmv_col = find_first_existing(
        result,
        [
            "gmv",
            "total_gmv",
            "revenue",
            "total_revenue",
            "sales",
        ],
    )

    cumulative_col = find_first_existing(
        result,
        [
            "cumulative_share",
            "cum_share",
            "cumulative_pct",
            "cumulative_percentage",
            "cum_pct",
            "pareto_share",
        ],
    )

    if category_col is None or gmv_col is None:
        raise ValueError("Could not find category / GMV columns in core_categories_pareto.csv.")

    result = result.rename(
        columns={
            category_col: "category",
            gmv_col: "gmv",
        }
    )

    result["gmv"] = to_numeric(result["gmv"]).fillna(0)
    result = result.sort_values("gmv", ascending=False).reset_index(drop=True)

    if cumulative_col is not None:
        result = result.rename(columns={cumulative_col: "cumulative_share"})
        result["cumulative_share"] = to_numeric(result["cumulative_share"])
        # convert likely percentages to 0-1 scale
        if result["cumulative_share"].dropna().max() is not None:
            max_val = result["cumulative_share"].dropna().max()
            if pd.notna(max_val) and max_val > 1.5:
                result["cumulative_share"] = result["cumulative_share"] / 100
    else:
        total = result["gmv"].sum()
        if total > 0:
            result["cumulative_share"] = result["gmv"].cumsum() / total
        else:
            result["cumulative_share"] = pd.NA

    return result[["category", "gmv", "cumulative_share"]].reset_index(drop=True)


def prep_strategy_groups(strategy_obj) -> pd.DataFrame:
    if not strategy_obj:
        return pd.DataFrame(columns=["strategy_group", "category"])

    rows = []

    if isinstance(strategy_obj, dict):
        for key, value in strategy_obj.items():
            if isinstance(value, list):
                for item in value:
                    rows.append(
                        {
                            "strategy_group": str(key),
                            "category": str(item),
                        }
                    )
            elif isinstance(value, dict):
                for sub_key, sub_val in value.items():
                    if isinstance(sub_val, list):
                        for item in sub_val:
                            rows.append(
                                {
                                    "strategy_group": f"{key} | {sub_key}",
                                    "category": str(item),
                                }
                            )
                    else:
                        rows.append(
                            {
                                "strategy_group": f"{key} | {sub_key}",
                                "category": str(sub_val),
                            }
                        )
            else:
                rows.append(
                    {
                        "strategy_group": str(key),
                        "category": str(value),
                    }
                )

    if not rows:
        return pd.DataFrame(columns=["strategy_group", "category"])

    return pd.DataFrame(rows)


def top_category_value(df: pd.DataFrame) -> tuple[str, float | None]:
    if df.empty or "gmv" not in df.columns:
        return "N/A", None

    temp = df.dropna(subset=["gmv"]).copy()
    if temp.empty:
        return "N/A", None

    best = temp.sort_values("gmv", ascending=False).iloc[0]
    return str(best["category"]), float(best["gmv"])


def build_pareto_chart(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df["category"],
            y=df["gmv"],
            name="GMV",
            yaxis="y1",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["category"],
            y=df["cumulative_share"],
            name="Cumulative Share",
            mode="lines+markers",
            yaxis="y2",
        )
    )

    fig.add_hline(
        y=0.8,
        line_dash="dash",
        yref="y2",
    )

    fig.update_layout(
        height=450,
        xaxis=dict(title="Category"),
        yaxis=dict(title="GMV"),
        yaxis2=dict(
            title="Cumulative Share",
            overlaying="y",
            side="right",
            tickformat=".0%",
            range=[0, 1.05],
        ),
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(orientation="h"),
    )
    return fig


# =========================================================
# Title
# =========================================================
st.title("Product Performance")
st.caption(
    "Category-level performance, BCG portfolio structure, Pareto concentration, and strategy grouping."
)


# =========================================================
# Data loading
# =========================================================
try:
    raw_bcg = load_category_bcg_classification()
    raw_pareto = load_core_categories_pareto()

    try:
        raw_strategy_groups = load_category_strategy_groups()
    except Exception:
        raw_strategy_groups = {}

    bcg_df = prep_bcg(raw_bcg)
    pareto_df = prep_pareto(raw_pareto)
    strategy_df = prep_strategy_groups(raw_strategy_groups)

except Exception as e:
    st.error("Failed to load Product Performance data.")
    st.exception(e)
    st.stop()


# =========================================================
# KPIs
# =========================================================
total_categories = bcg_df["category"].nunique() if not bcg_df.empty else None
bcg_groups_count = bcg_df["bcg_group"].nunique() if not bcg_df.empty else None

core_categories = None
if not pareto_df.empty and "cumulative_share" in pareto_df.columns:
    core_categories = pareto_df[pareto_df["cumulative_share"] <= 0.8]["category"].nunique()

top_category_name, top_category_gmv = top_category_value(bcg_df)

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Categories", format_number(total_categories, 0))
k2.metric("BCG Groups", format_number(bcg_groups_count, 0))
k3.metric("Core Categories (80%)", format_number(core_categories, 0))
k4.metric("Top Category GMV", format_currency(top_category_gmv, 0, symbol="R$"))


# =========================================================
# Filters
# =========================================================
st.markdown("---")
st.markdown("## Filtered View")

filter_col1, filter_col2 = st.columns(2)

selected_bcg_groups = None
if not bcg_df.empty:
    with filter_col1:
        bcg_options = sorted(bcg_df["bcg_group"].dropna().astype(str).unique().tolist())
        selected_bcg_groups = st.multiselect(
            "Select BCG groups",
            options=bcg_options,
            default=bcg_options,
        )

selected_top_n = None
with filter_col2:
    selected_top_n = st.slider("Top N categories", min_value=5, max_value=20, value=10, step=5)


# =========================================================
# Chart row 1
# =========================================================
st.markdown("---")
st.markdown("## Category Portfolio Structure")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown("### BCG Group Distribution")
    if bcg_df.empty:
        st.info("No BCG classification data available.")
    else:
        bcg_plot_df = bcg_df.copy()
        if selected_bcg_groups is not None:
            bcg_plot_df = bcg_plot_df[bcg_plot_df["bcg_group"].astype(str).isin(selected_bcg_groups)]

        dist_df = (
            bcg_plot_df["bcg_group"]
            .fillna("Unknown")
            .value_counts()
            .reset_index()
        )
        dist_df.columns = ["bcg_group", "category_count"]

        fig_bcg = px.pie(
            dist_df,
            names="bcg_group",
            values="category_count",
            hole=0.45,
        )
        fig_bcg.update_layout(
            height=420,
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(fig_bcg, use_container_width=True)

with chart_col2:
    st.markdown("### Top Categories by GMV")
    if bcg_df.empty or "gmv" not in bcg_df.columns:
        st.info("No GMV data available.")
    else:
        top_df = bcg_df.copy()
        if selected_bcg_groups is not None:
            top_df = top_df[top_df["bcg_group"].astype(str).isin(selected_bcg_groups)]

        top_df = top_df.dropna(subset=["gmv"]).sort_values("gmv", ascending=False).head(selected_top_n)

        fig_top = px.bar(
            top_df,
            x="category",
            y="gmv",
            color="bcg_group",
            text="gmv",
        )
        fig_top.update_layout(
            height=420,
            xaxis_title="Category",
            yaxis_title="GMV",
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(fig_top, use_container_width=True)


# =========================================================
# Chart row 2
# =========================================================
st.markdown("---")
st.markdown("## Category Performance and Pareto Analysis")

chart_col3, chart_col4 = st.columns(2)

with chart_col3:
    st.markdown("### Revenue vs Order Count")
    if bcg_df.empty or "gmv" not in bcg_df.columns or "order_count" not in bcg_df.columns:
        st.info("Scatter plot requires GMV and order count.")
    else:
        scatter_df = bcg_df.copy()
        if selected_bcg_groups is not None:
            scatter_df = scatter_df[scatter_df["bcg_group"].astype(str).isin(selected_bcg_groups)]

        scatter_df = scatter_df.dropna(subset=["gmv", "order_count"])

        if scatter_df.empty:
            st.info("No usable records for scatter chart.")
        else:
            fig_scatter = px.scatter(
                scatter_df,
                x="order_count",
                y="gmv",
                color="bcg_group",
                hover_name="category",
                size="gmv" if scatter_df["gmv"].notna().any() else None,
            )
            fig_scatter.update_layout(
                height=420,
                xaxis_title="Order Count",
                yaxis_title="GMV",
                margin=dict(l=20, r=20, t=40, b=20),
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

with chart_col4:
    st.markdown("### Pareto Concentration")
    if pareto_df.empty:
        st.info("No Pareto summary available.")
    else:
        st.plotly_chart(
            build_pareto_chart(pareto_df.head(max(selected_top_n, 10))),
            use_container_width=True,
        )


# =========================================================
# Strategy section
# =========================================================
st.markdown("---")
st.markdown("## Strategy Groups")

left_col, right_col = st.columns([1.4, 1])

with left_col:
    st.markdown("### Strategy Group Table")
    if strategy_df.empty:
        st.info("No category strategy group JSON was loaded.")
    else:
        summary_df = (
            strategy_df.groupby("strategy_group", as_index=False)["category"]
            .count()
            .rename(columns={"category": "category_count"})
            .sort_values("category_count", ascending=False)
        )
        st.dataframe(summary_df, use_container_width=True, hide_index=True)

with right_col:
    st.markdown("### Strategy Group Distribution")
    if strategy_df.empty:
        st.info("No strategy distribution available.")
    else:
        summary_df = (
            strategy_df.groupby("strategy_group", as_index=False)["category"]
            .count()
            .rename(columns={"category": "category_count"})
            .sort_values("category_count", ascending=False)
        )

        fig_strategy = px.bar(
            summary_df,
            x="strategy_group",
            y="category_count",
            text="category_count",
        )
        fig_strategy.update_layout(
            height=380,
            xaxis_title="Strategy Group",
            yaxis_title="Category Count",
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(fig_strategy, use_container_width=True)


# =========================================================
# Detailed tables
# =========================================================
st.markdown("---")
st.markdown("## Detailed Category Tables")

table_col1, table_col2 = st.columns(2)

with table_col1:
    st.markdown("### BCG Classification Table")
    if bcg_df.empty:
        st.info("No BCG data available.")
    else:
        display_df = bcg_df.copy()
        if selected_bcg_groups is not None:
            display_df = display_df[display_df["bcg_group"].astype(str).isin(selected_bcg_groups)]
        st.dataframe(display_df.head(30), use_container_width=True, hide_index=True)

with table_col2:
    st.markdown("### Core Categories Pareto Table")
    if pareto_df.empty:
        st.info("No Pareto data available.")
    else:
        display_pareto_df = pareto_df.copy()
        st.dataframe(display_pareto_df.head(30), use_container_width=True, hide_index=True)


# =========================================================
# Raw preview
# =========================================================
st.markdown("---")
with st.expander("Preview loaded datasets", expanded=False):
    st.markdown("### BCG classification")
    st.dataframe(bcg_df.head(20), use_container_width=True, hide_index=True)

    st.markdown("### Pareto summary")
    st.dataframe(pareto_df.head(20), use_container_width=True, hide_index=True)

    st.markdown("### Strategy groups")
    st.dataframe(strategy_df.head(20), use_container_width=True, hide_index=True)
