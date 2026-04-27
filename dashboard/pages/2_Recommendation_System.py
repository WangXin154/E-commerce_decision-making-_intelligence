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
        load_business_impact_estimation,
        load_evaluation_summary,
        load_matrix_sparsity_summary,
        load_recommendations_content,
        load_recommendations_hybrid,
        load_recommendations_item_based,
        load_recommendations_personalized,
        load_top_recommended_products,
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
        load_business_impact_estimation,
        load_evaluation_summary,
        load_matrix_sparsity_summary,
        load_recommendations_content,
        load_recommendations_hybrid,
        load_recommendations_item_based,
        load_recommendations_personalized,
        load_top_recommended_products,
        to_numeric,
    )


# =========================================================
# Page config
# =========================================================
st.set_page_config(
    page_title="Recommendation System",
    page_icon="🎯",
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
    st.success("Current page: Recommendation System")

    st.markdown(
        """
        **Dashboard focus**
        - User-level recommendations
        - Algorithm comparison
        - Offline evaluation
        - Business impact summary
        """
    )


# =========================================================
# Helpers
# =========================================================
def normalize_label(value) -> str:
    return str(value).strip().lower().replace("_", " ").replace("-", " ")


def prep_recommendation_df(df: pd.DataFrame, algorithm_name: str) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(
            columns=[
                "algorithm",
                "user_id",
                "product_id",
                "score",
                "category",
                "strategy",
                "source_count",
            ]
        )

    result = df.copy()

    user_col = find_first_existing(
        result,
        ["unique_user_id", "user_id", "customer_id", "customer_unique_id"]
    )
    product_col = find_first_existing(
        result,
        ["product_id", "item_id", "sku"]
    )
    score_col = find_first_existing(
        result,
        [
            "personalized_score",
            "hybrid_score",
            "predicted_rating",
            "similarity_score",
            "final_score",
            "score",
        ]
    )
    category_col = find_first_existing(
        result,
        ["category", "main_category", "product_category"]
    )
    strategy_col = find_first_existing(
        result,
        ["strategy", "score_source", "source", "recommendation_source"]
    )
    source_count_col = find_first_existing(
        result,
        ["source_count"]
    )

    if product_col is None:
        raise ValueError(f"Could not find product column for algorithm: {algorithm_name}")

    if user_col is None:
        result["user_id"] = "ALL_USERS"
        user_col = "user_id"

    if score_col is None:
        result["score"] = pd.NA
        score_col = "score"

    if category_col is None:
        result["category"] = "Unknown"
        category_col = "category"

    if strategy_col is None:
        result["strategy"] = algorithm_name
        strategy_col = "strategy"

    if source_count_col is None:
        result["source_count"] = pd.NA
        source_count_col = "source_count"

    result = result.rename(
        columns={
            user_col: "user_id",
            product_col: "product_id",
            score_col: "score",
            category_col: "category",
            strategy_col: "strategy",
            source_count_col: "source_count",
        }
    )

    result["score"] = to_numeric(result["score"])
    result["algorithm"] = algorithm_name

    keep_cols = [
        "algorithm",
        "user_id",
        "product_id",
        "score",
        "category",
        "strategy",
        "source_count",
    ]

    extra_cols = [c for c in result.columns if c not in keep_cols]
    result = result[keep_cols + extra_cols].copy()

    return result.reset_index(drop=True)


def prep_evaluation_summary(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(
            columns=[
                "algorithm", "k",
                "precision_mean", "recall_mean", "ndcg_mean",
                "hit_rate_mean", "coverage"
            ]
        )

    result = df.copy()

    rename_map = {}
    for old, new in [
        ("Precision", "precision_mean"),
        ("Recall", "recall_mean"),
        ("NDCG", "ndcg_mean"),
        ("Hit Rate", "hit_rate_mean"),
        ("Coverage", "coverage"),
    ]:
        if old in result.columns:
            rename_map[old] = new

    if rename_map:
        result = result.rename(columns=rename_map)

    required = ["algorithm", "k"]
    for col in required:
        if col not in result.columns:
            raise ValueError("evaluation_summary_leave_one_out.csv is missing required columns.")

    for col in ["precision_mean", "recall_mean", "ndcg_mean", "hit_rate_mean", "coverage"]:
        if col in result.columns:
            result[col] = to_numeric(result[col])

    result["algorithm"] = result["algorithm"].astype(str)
    result["k"] = to_numeric(result["k"])

    return result.reset_index(drop=True)


def prep_top_products(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(
            columns=[
                "product_id",
                "recommendation_count",
                "avg_score",
                "main_strategy",
                "main_category",
                "share",
            ]
        )

    result = df.copy()

    product_col = find_first_existing(result, ["product_id", "item_id", "sku"])
    count_col = find_first_existing(result, ["recommendation_count", "count"])
    score_col = find_first_existing(result, ["avg_personalized_score", "avg_score", "score"])
    strategy_col = find_first_existing(result, ["main_strategy", "strategy"])
    category_col = find_first_existing(result, ["main_category", "category"])
    share_col = find_first_existing(result, ["share"])

    if product_col is None or count_col is None:
        raise ValueError("top_recommended_products_debug.csv is missing core columns.")

    rename_map = {
        product_col: "product_id",
        count_col: "recommendation_count",
    }
    if score_col is not None:
        rename_map[score_col] = "avg_score"
    if strategy_col is not None:
        rename_map[strategy_col] = "main_strategy"
    if category_col is not None:
        rename_map[category_col] = "main_category"
    if share_col is not None:
        rename_map[share_col] = "share"

    result = result.rename(columns=rename_map)

    if "avg_score" not in result.columns:
        result["avg_score"] = pd.NA
    if "main_strategy" not in result.columns:
        result["main_strategy"] = pd.NA
    if "main_category" not in result.columns:
        result["main_category"] = pd.NA
    if "share" not in result.columns:
        result["share"] = pd.NA

    result["recommendation_count"] = to_numeric(result["recommendation_count"])
    result["avg_score"] = to_numeric(result["avg_score"])
    result["share"] = to_numeric(result["share"])

    return result[
        ["product_id", "recommendation_count", "avg_score", "main_strategy", "main_category", "share"]
    ].reset_index(drop=True)


def prep_metric_table(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["metric", "value"])

    result = df.copy()

    metric_col = find_first_existing(result, ["metric", "item", "name"])
    value_col = find_first_existing(result, ["value", "metric_value", "score"])

    if metric_col is None or value_col is None:
        return result

    result = result[[metric_col, value_col]].copy()
    result.columns = ["metric", "value"]
    result["metric"] = result["metric"].astype(str)
    result["value_numeric"] = pd.to_numeric(result["value"], errors="coerce")
    return result


def get_metric_value(df: pd.DataFrame, candidates: list[str]) -> float | None:
    if df.empty or "metric" not in df.columns or "value_numeric" not in df.columns:
        return None

    normalized = {normalize_label(x) for x in candidates}
    temp = df.copy()
    temp["_metric_norm"] = temp["metric"].map(normalize_label)

    matched = temp[temp["_metric_norm"].isin(normalized)]
    if matched.empty:
        return None

    value = matched["value_numeric"].iloc[0]
    return None if pd.isna(value) else float(value)


def get_best_metric(eval_df: pd.DataFrame, metric_col: str, k_value: int) -> float | None:
    if eval_df.empty or metric_col not in eval_df.columns:
        return None

    temp = eval_df[eval_df["k"] == k_value].copy()
    if temp.empty:
        return None

    temp = temp.dropna(subset=[metric_col])
    if temp.empty:
        return None

    return float(temp[metric_col].max())


def best_algorithm_at_k(eval_df: pd.DataFrame, metric_col: str, k_value: int) -> str:
    if eval_df.empty or metric_col not in eval_df.columns:
        return "N/A"

    temp = eval_df[eval_df["k"] == k_value].copy()
    temp = temp.dropna(subset=[metric_col])
    if temp.empty:
        return "N/A"

    best_row = temp.sort_values(metric_col, ascending=False).iloc[0]
    return str(best_row["algorithm"])


# =========================================================
# Title
# =========================================================
st.title("Recommendation System")
st.caption(
    "Interactive recommendation lookup, offline evaluation comparison, and business impact summary."
)


# =========================================================
# Data loading
# =========================================================
try:
    raw_content = load_recommendations_content()
    raw_item = load_recommendations_item_based()
    raw_hybrid = load_recommendations_hybrid()
    raw_personalized = load_recommendations_personalized()
    raw_eval = load_evaluation_summary()
    raw_sparsity = load_matrix_sparsity_summary()
    raw_top_products = load_top_recommended_products()
    raw_business_impact = load_business_impact_estimation()

    rec_content_df = prep_recommendation_df(raw_content, "content")
    rec_item_df = prep_recommendation_df(raw_item, "item_based")
    rec_hybrid_df = prep_recommendation_df(raw_hybrid, "hybrid")
    rec_personalized_df = prep_recommendation_df(raw_personalized, "personalized")

    eval_df = prep_evaluation_summary(raw_eval)
    sparsity_df = prep_metric_table(raw_sparsity)
    top_products_df = prep_top_products(raw_top_products)
    business_impact_df = prep_metric_table(raw_business_impact)

except Exception as e:
    st.error("Failed to load Recommendation System data.")
    st.exception(e)
    st.stop()


# =========================================================
# Algorithm map
# =========================================================
algorithm_map = {
    "personalized": rec_personalized_df,
    "hybrid": rec_hybrid_df,
    "content": rec_content_df,
    "item_based": rec_item_df,
}

available_algorithms = [k for k, v in algorithm_map.items() if not v.empty]
if not available_algorithms:
    st.warning("No recommendation result files contain usable data.")
    st.stop()


# =========================================================
# KPI row
# =========================================================
unique_users_personalized = (
    rec_personalized_df["user_id"].nunique() if not rec_personalized_df.empty else None
)
best_ndcg_10 = get_best_metric(eval_df, "ndcg_mean", 10)
best_coverage_10 = get_best_metric(eval_df, "coverage", 10)
sparsity_value = get_metric_value(sparsity_df, ["Sparsity"])

k1, k2, k3, k4 = st.columns(4)
k1.metric("Available Algorithms", format_number(len(available_algorithms), 0))
k2.metric("Users in Personalized Output", format_number(unique_users_personalized, 0))
k3.metric("Best NDCG@10", format_number(best_ndcg_10, 4))
k4.metric("Coverage@10 (Best)", format_number(best_coverage_10, 4))


# =========================================================
# Interactive recommender
# =========================================================
st.markdown("---")
st.markdown("## Interactive Recommendation Lookup")

control_col1, control_col2, control_col3 = st.columns([1, 1.2, 1])

with control_col1:
    selected_algorithm = st.selectbox(
        "Select algorithm",
        options=available_algorithms,
        index=0,
    )

current_df = algorithm_map[selected_algorithm].copy()
user_options = sorted(current_df["user_id"].dropna().astype(str).unique().tolist())

with control_col2:
    selected_user = st.selectbox(
        "Select user ID",
        options=user_options,
        index=0 if user_options else None,
    )

with control_col3:
    top_n = st.slider("Top N recommendations", min_value=5, max_value=20, value=10, step=5)

user_rec_df = current_df[current_df["user_id"].astype(str) == str(selected_user)].copy()
if "score" in user_rec_df.columns:
    user_rec_df = user_rec_df.sort_values("score", ascending=False)

st.markdown(
    f"""
    **Selected algorithm:** `{selected_algorithm}`  
    **Selected user:** `{selected_user}`  
    **User-level recommendations found:** `{len(user_rec_df)}`  
    """
)

left_col, right_col = st.columns([1.6, 1])

with left_col:
    st.markdown("### Recommendation Results")
    if user_rec_df.empty:
        st.info("No recommendations found for the selected user and algorithm.")
    else:
        display_cols = [c for c in [
            "product_id", "score", "category", "strategy", "source_count"
        ] if c in user_rec_df.columns]

        st.dataframe(
            user_rec_df[display_cols].head(top_n),
            use_container_width=True,
            hide_index=True,
        )

with right_col:
    st.markdown("### Category Mix")
    if user_rec_df.empty or "category" not in user_rec_df.columns:
        st.info("No category information available.")
    else:
        cat_df = (
            user_rec_df["category"]
            .fillna("Unknown")
            .value_counts()
            .reset_index()
        )
        cat_df.columns = ["category", "count"]

        fig_cat = px.pie(
            cat_df,
            names="category",
            values="count",
            hole=0.45,
        )
        fig_cat.update_layout(
            height=380,
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(fig_cat, use_container_width=True)


# =========================================================
# Evaluation summary
# =========================================================
st.markdown("---")
st.markdown("## Offline Evaluation Summary")

best_algo_ndcg = best_algorithm_at_k(eval_df, "ndcg_mean", 10)
best_algo_hit = best_algorithm_at_k(eval_df, "hit_rate_mean", 10)

summary_col1, summary_col2 = st.columns([1.5, 1])

with summary_col1:
    if eval_df.empty:
        st.info("No offline evaluation summary available.")
    else:
        metric_name = st.selectbox(
            "Select evaluation metric",
            options=["ndcg_mean", "hit_rate_mean", "precision_mean", "recall_mean", "coverage"],
            index=0,
        )

        fig_eval = px.line(
            eval_df,
            x="k",
            y=metric_name,
            color="algorithm",
            markers=True,
        )
        fig_eval.update_layout(
            height=420,
            xaxis_title="K",
            yaxis_title=metric_name,
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(fig_eval, use_container_width=True)

with summary_col2:
    st.markdown("### Evaluation Highlights")
    st.markdown(
        f"""
        - Best algorithm by **NDCG@10**: **{best_algo_ndcg}**
        - Best algorithm by **Hit Rate@10**: **{best_algo_hit}**
        - Best **Coverage@10**: **{format_number(best_coverage_10, 4)}**
        - Matrix sparsity: **{format_number(sparsity_value, 4)}**
        """
    )

    if not eval_df.empty:
        st.dataframe(eval_df, use_container_width=True, hide_index=True)


# =========================================================
# Top products and business impact
# =========================================================
st.markdown("---")
st.markdown("## Top Recommended Products and Business Impact")

bottom_col1, bottom_col2 = st.columns([1.3, 1])

with bottom_col1:
    st.markdown("### Top Recommended Products")
    if top_products_df.empty:
        st.info("No top recommended product summary available.")
    else:
        top_n_products = st.slider(
            "Top products to display",
            min_value=5,
            max_value=20,
            value=10,
            step=5,
            key="top_products_slider",
        )

        st.dataframe(
            top_products_df.head(top_n_products),
            use_container_width=True,
            hide_index=True,
        )

        fig_top = px.bar(
            top_products_df.head(top_n_products),
            x="product_id",
            y="recommendation_count",
            color="main_category" if "main_category" in top_products_df.columns else None,
            text="recommendation_count",
        )
        fig_top.update_layout(
            height=420,
            xaxis_title="Product ID",
            yaxis_title="Recommendation Count",
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(fig_top, use_container_width=True)

with bottom_col2:
    st.markdown("### Business Impact Summary")
    if business_impact_df.empty:
        st.info("No business impact summary available.")
    else:
        monthly_gmv_increase = get_metric_value(
            business_impact_df,
            ["Estimated monthly GMV increase"]
        )
        annual_gmv_increase = get_metric_value(
            business_impact_df,
            ["Estimated annual GMV increase"]
        )
        estimated_roi = get_metric_value(
            business_impact_df,
            ["Estimated ROI"]
        )

        m1, m2, m3 = st.columns(3)
        m1.metric("Monthly GMV Increase", format_currency(monthly_gmv_increase, 0, symbol="R$"))
        m2.metric("Annual GMV Increase", format_currency(annual_gmv_increase, 0, symbol="R$"))
        m3.metric("Estimated ROI", format_number(estimated_roi, 4))

        st.dataframe(
            business_impact_df[["metric", "value"]],
            use_container_width=True,
            hide_index=True,
        )

        # show sparsity summary below
        if not sparsity_df.empty:
            st.markdown("### Matrix Sparsity Summary")
            st.dataframe(
                sparsity_df[["metric", "value"]],
                use_container_width=True,
                hide_index=True,
            )


# =========================================================
# Raw preview
# =========================================================
st.markdown("---")
with st.expander("Preview loaded datasets", expanded=False):
    st.markdown("### Personalized recommendations")
    st.dataframe(rec_personalized_df.head(20), use_container_width=True, hide_index=True)

    st.markdown("### Hybrid recommendations")
    st.dataframe(rec_hybrid_df.head(20), use_container_width=True, hide_index=True)

    st.markdown("### Evaluation summary")
    st.dataframe(eval_df, use_container_width=True, hide_index=True)

    st.markdown("### Top recommended products")
    st.dataframe(top_products_df.head(20), use_container_width=True, hide_index=True)

    st.markdown("### Business impact")
    st.dataframe(business_impact_df, use_container_width=True, hide_index=True)
