# Data Dictionary

## Overview

This project uses a layered data design built on top of the Olist Brazilian e-commerce dataset. The database starts with raw ingestion tables, then transforms them into a simple star-schema-style warehouse with dimension and fact tables, and finally exposes reusable SQL views for downstream analysis modules such as satisfaction, RFM segmentation, category analysis, geography, churn, and CLV. :contentReference[oaicite:0]{index=0} :contentReference[oaicite:1]{index=1}

---

## Database

- **Database name:** `ecommerce_platform`
- **Character set:** `utf8mb4`
- **Collation:** `utf8mb4_0900_ai_ci` :contentReference[oaicite:2]{index=2}

---

## Layer 1 — Raw Tables

These tables store ingested source data before warehouse modeling. They preserve the original transactional structure of customers, orders, products, payments, reviews, order items, and sellers. :contentReference[oaicite:3]{index=3}

### 1. `customers_raw`

| Column | Type | Description |
|---|---|---|
| `customer_id` | `VARCHAR(50)` | Order-level customer identifier from source data |
| `customer_unique_id` | `VARCHAR(50)` | Persistent user identifier across multiple orders |
| `customer_zip_code_prefix` | `INT` | Zip prefix |
| `customer_city` | `VARCHAR(100)` | Customer city |
| `customer_state` | `VARCHAR(10)` | Customer state |

**Used in:** user dimension, geography, churn, CLV, recommendation. :contentReference[oaicite:4]{index=4}

### 2. `orders_raw`

| Column | Type | Description |
|---|---|---|
| `order_id` | `VARCHAR(50)` | Unique order ID, primary key |
| `customer_id` | `VARCHAR(50)` | Links to source customer |
| `order_status` | `VARCHAR(50)` | Order status |
| `order_purchase_timestamp` | `VARCHAR(32)` | Purchase timestamp from raw source |
| `order_approved_at` | `VARCHAR(32)` | Approval timestamp |
| `order_delivered_carrier_date` | `VARCHAR(32)` | Carrier handoff timestamp |
| `order_delivered_customer_date` | `VARCHAR(32)` | Final delivery timestamp |
| `order_estimated_delivery_date` | `VARCHAR(32)` | Estimated delivery date |

**Primary key:** `order_id` :contentReference[oaicite:5]{index=5}

### 3. `products_raw`

| Column | Type | Description |
|---|---|---|
| `product_id` | `VARCHAR(50)` | Product ID, primary key |
| `product_category_name` | `VARCHAR(100)` | Product category |
| `product_name_lenght` | `INT` | Product name length |
| `product_description_lenght` | `INT` | Product description length |
| `product_photos_qty` | `INT` | Number of product photos |
| `product_weight_g` | `INT` | Product weight in grams |
| `product_length_cm` | `INT` | Product length |
| `product_height_cm` | `INT` | Product height |
| `product_width_cm` | `INT` | Product width |

**Primary key:** `product_id` :contentReference[oaicite:6]{index=6}

### 4. `payments_raw`

| Column | Type | Description |
|---|---|---|
| `order_id` | `VARCHAR(50)` | Order ID |
| `payment_sequential` | `INT` | Payment sequence within order |
| `payment_type` | `VARCHAR(50)` | Payment method |
| `payment_installments` | `INT` | Installment count |
| `payment_value` | `DECIMAL(10,2)` | Payment amount |

**Primary key:** (`order_id`, `payment_sequential`) :contentReference[oaicite:7]{index=7}

### 5. `reviews_raw`

| Column | Type | Description |
|---|---|---|
| `review_id` | `VARCHAR(50)` | Review ID |
| `order_id` | `VARCHAR(50)` | Order ID |
| `review_score` | `INT` | Review rating score |
| `review_comment_title` | `TEXT` | Review title |
| `review_comment_message` | `TEXT` | Review message |
| `review_creation_date` | `DATETIME` | Review creation timestamp |
| `review_answer_timestamp` | `DATETIME` | Review answer timestamp |

**Primary key:** (`review_id`, `order_id`) :contentReference[oaicite:8]{index=8}

### 6. `order_items_raw`

| Column | Type | Description |
|---|---|---|
| `order_id` | `VARCHAR(50)` | Order ID |
| `order_item_id` | `INT` | Item sequence in order |
| `product_id` | `VARCHAR(50)` | Product ID |
| `seller_id` | `VARCHAR(50)` | Seller ID |
| `shipping_limit_date` | `VARCHAR(32)` | Shipping limit timestamp |
| `price` | `DECIMAL(10,2)` | Item price |
| `freight_value` | `DECIMAL(10,2)` | Freight cost |

**Primary key:** (`order_id`, `order_item_id`) :contentReference[oaicite:9]{index=9}

### 7. `sellers_raw`

| Column | Type | Description |
|---|---|---|
| `seller_id` | `VARCHAR(50)` | Seller ID, primary key |
| `seller_zip_code_prefix` | `VARCHAR(5)` | Seller zip prefix |
| `seller_city` | `VARCHAR(100)` | Seller city |
| `seller_state` | `VARCHAR(5)` | Seller state |

**Primary key:** `seller_id` :contentReference[oaicite:10]{index=10}

---

## Layer 2 — Warehouse Tables

The warehouse organizes data into dimensions and facts. This is the main analytical layer used by notebooks and SQL views. :contentReference[oaicite:11]{index=11}

### 1. `dim_user`

| Column | Type | Description |
|---|---|---|
| `user_id` | `VARCHAR(50)` | Warehouse user key, sourced from `customer_id` |
| `unique_user_id` | `VARCHAR(50)` | Persistent user identifier |
| `city` | `VARCHAR(100)` | User city |
| `state` | `VARCHAR(10)` | User state |

**Primary key:** `user_id`  
**Business role:** user dimension for customer-level analysis. :contentReference[oaicite:12]{index=12}

### 2. `dim_product`

| Column | Type | Description |
|---|---|---|
| `product_id` | `VARCHAR(50)` | Product ID |
| `category` | `VARCHAR(100)` | Product category |
| `weight_g` | `INT` | Product weight |
| `length_cm` | `INT` | Product length |
| `height_cm` | `INT` | Product height |
| `width_cm` | `INT` | Product width |

**Primary key:** `product_id` :contentReference[oaicite:13]{index=13}

### 3. `fact_order`

| Column | Type | Description |
|---|---|---|
| `order_id` | `VARCHAR(50)` | Order ID |
| `user_id` | `VARCHAR(50)` | Links to `dim_user.user_id` |
| `order_status` | `VARCHAR(50)` | Order status |
| `purchase_ts` | `DATETIME` | Purchase timestamp |
| `delivered_ts` | `DATETIME` | Delivered timestamp |
| `estimated_delivery_ts` | `DATETIME` | Estimated delivery timestamp |
| `delivered_days` | `INT` | Days from purchase to delivery |

**Primary key:** `order_id`  
**Foreign key:** `user_id -> dim_user(user_id)`  
**Index:** `idx_order_user_purchase(user_id, purchase_ts)` :contentReference[oaicite:14]{index=14}

### 4. `fact_order_item`

| Column | Type | Description |
|---|---|---|
| `order_id` | `VARCHAR(50)` | Order ID |
| `order_item_id` | `INT` | Item sequence |
| `product_id` | `VARCHAR(50)` | Product ID |
| `seller_id` | `VARCHAR(50)` | Seller ID |
| `shipping_limit_ts` | `DATETIME` | Shipping limit timestamp |
| `price` | `DECIMAL(10,2)` | Item price |
| `freight_value` | `DECIMAL(10,2)` | Freight cost |
| `gmv` | `DECIMAL(10,2)` | Gross merchandise value, defined as `price + freight_value` |

**Primary key:** (`order_id`, `order_item_id`)  
**Foreign keys:** `order_id -> fact_order(order_id)`, `product_id -> dim_product(product_id)`  
**Index:** `idx_item_product(product_id)` :contentReference[oaicite:15]{index=15}

### 5. `fact_payment`

| Column | Type | Description |
|---|---|---|
| `order_id` | `VARCHAR(50)` | Order ID |
| `payment_sequential` | `INT` | Payment sequence |
| `payment_type` | `VARCHAR(50)` | Payment method |
| `payment_installments` | `INT` | Installment count |
| `payment_value` | `DECIMAL(10,2)` | Payment value |

**Primary key:** (`order_id`, `payment_sequential`)  
**Foreign key:** `order_id -> fact_order(order_id)` :contentReference[oaicite:16]{index=16}

### 6. `fact_review`

| Column | Type | Description |
|---|---|---|
| `review_id` | `VARCHAR(50)` | Review ID |
| `order_id` | `VARCHAR(50)` | Order ID |
| `review_score` | `INT` | Review rating |
| `review_comment_len` | `INT` | Review text length |
| `review_creation_ts` | `VARCHAR(32)` | Review creation timestamp |
| `review_answer_ts` | `VARCHAR(32)` | Review answer timestamp |

**Primary key:** `review_id`  
**Foreign key:** `order_id -> fact_order(order_id)`  
**Index:** `idx_review_order(order_id)` :contentReference[oaicite:17]{index=17}

---

## ETL and Transformation Notes

The ETL process loads raw tables first, then populates warehouse tables with cleaned and typed fields. Important transformations include:

- raw customer data → `dim_user`
- raw product data → `dim_product`
- raw order timestamps → parsed into `DATETIME` fields in `fact_order`
- `delivered_days` computed from purchase and delivery timestamps
- `gmv` computed in `fact_order_item` as `price + freight_value`
- `fact_review.review_comment_len` computed from review text length. :contentReference[oaicite:18]{index=18}

---

## Layer 3 — Analytical Views

These views are the reusable semantic layer for notebooks and business modules. They are defined in `create_views.sql`. :contentReference[oaicite:19]{index=19}

### 1. `view_user_behavior`
User-level behavior summary for RFM and customer analysis.

**Main fields**
- `unique_user_id`
- `city`
- `state`
- `order_count`
- `total_spent`
- `avg_order_value`
- `last_purchase_date`
- `days_since_last_purchase`
- `first_purchase_date`
- `customer_lifetime_days`

**Used in**
- Module 02 RFM segmentation
- customer value analysis
- later personalization logic. :contentReference[oaicite:20]{index=20}

### 2. `view_product_sales`
Product-level sales and review summary.

**Main fields**
- `product_id`
- `category`
- `sales_count`
- `total_revenue`
- `total_gmv`
- `avg_price`
- `avg_review_score`
- `review_count`
- `first_sale_date`
- `last_sale_date`

**Used in**
- product ranking
- category rollups
- recommendation feature engineering. :contentReference[oaicite:21]{index=21}

### 3. `view_category_sales`
Category-level summary based on `view_product_sales`.

**Main fields**
- `category`
- `product_count`
- `total_sales`
- `category_total_revenue`
- `avg_product_price`
- `avg_review_score`

**Used in**
- category portfolio analysis
- Pareto / BCG-style categorization. :contentReference[oaicite:22]{index=22}

### 4. `view_delivery_analysis`
Order-level logistics and review performance view.

**Main fields**
- `order_id`
- `customer_state`
- `order_status`
- `delivered_days`
- `estimated_days`
- `is_delayed`
- `delay_days`
- `order_value`
- `review_score`

**Used in**
- Module 01 satisfaction vs delivery
- regional logistics analysis. :contentReference[oaicite:23]{index=23}

### 5. `view_order_satisfaction`
Order-level satisfaction labeling view.

**Main fields**
- `order_id`
- `user_id`
- `state`
- `purchase_ts`
- `delivered_days`
- `order_value`
- `review_score`
- `review_comment_len`
- `satisfaction_level`
- `delivery_period`

**Used in**
- satisfaction segmentation
- delivery-period comparison
- statistical testing. :contentReference[oaicite:24]{index=24}

### 6. `view_order_complete`
Wide order-level analysis view joining facts and dimensions.

**Main fields**
- order-level: `order_id`, `order_status`, `purchase_ts`, `delivered_ts`, `estimated_delivery_ts`, `delivered_days`
- user-level: `user_id`, `user_city`, `user_state`
- product-level: `product_category`, `product_id`
- item-level: `order_item_id`, `price`, `freight_value`, `gmv`, `seller_id`
- seller-level: `seller_city`, `seller_state`
- payment-level: `payment_type`, `payment_installments`, `payment_value`
- review-level: `review_score`, `review_comment_len`
- derived flags: `is_delayed`, `is_satisfied`

**Used in**
- integrated analysis
- downstream module feature extraction. :contentReference[oaicite:25]{index=25}

### 7. `view_category_analysis`
Category-level business strategy view.

**Main fields**
- `category`
- `order_count`
- `customer_count`
- `total_revenue`
- `total_gmv`
- `avg_price`
- `avg_freight`
- `avg_review_score`
- `bad_review_rate`
- `avg_comment_len`
- `repeat_rate`
- `first_sale_date`
- `last_sale_date`
- `category_lifetime_days`

**Used in**
- Module 03 product category analysis. :contentReference[oaicite:26]{index=26}

### 8. `view_geographic_state_summary`
State-level KPI summary.

**Main fields**
- `customer_state`
- `order_count`
- `customer_count`
- `total_gmv`
- `total_revenue`
- `avg_order_value`
- `avg_delivery_days`
- `avg_freight_cost`
- `delay_rate`
- `avg_review_score`
- `bad_review_rate`
- `repeat_rate`

**Used in**
- Module 04 geographic analysis
- state clustering
- logistics and satisfaction comparison. :contentReference[oaicite:27]{index=27}

### 9. `view_geographic_city_summary`
City-level KPI summary.

**Main fields**
- `customer_state`
- `customer_city`
- `order_count`
- `customer_count`
- `total_gmv`
- `total_revenue`
- `avg_order_value`
- `avg_delivery_days`
- `avg_freight_cost`
- `avg_review_score`
- `bad_review_rate`

**Used in**
- Module 04 city concentration analysis. :contentReference[oaicite:28]{index=28}

### 10. `view_buyer_seller_distance`
Buyer–seller geographic relationship view.

**Main fields**
- `order_id`
- `buyer_state`
- `buyer_city`
- `seller_state`
- `seller_city`
- `trade_type` (`Same State` / `Cross State`)
- `delivered_days`
- `freight_value`
- `gmv`
- `review_score`

**Used in**
- cross-state vs same-state logistics analysis
- route pressure analysis. :contentReference[oaicite:29]{index=29}

### 11. `view_user_clv_features`
Customer-level CLV feature view.

**Main fields**
- `customer_unique_id`
- `total_orders`
- `total_gmv`
- `avg_order_value`
- `first_order_date`
- `last_order_date`
- `customer_lifetime_days`
- `days_since_last_order`
- `monthly_frequency`
- `unique_products_purchased`
- `unique_categories_purchased`
- `avg_payment_value`
- `max_installments_used`
- `avg_review_score`
- `satisfaction_rate`
- `bad_review_count`
- `avg_delivery_delay`
- `delay_rate`

**Used in**
- Module 07 CLV prediction. :contentReference[oaicite:30]{index=30}

### 12. `view_user_future_gmv`
Future-value target view for CLV modeling.

**Main fields**
- `customer_unique_id`
- `future_6m_gmv`
- `future_6m_orders`
- `is_active_future`

**Used in**
- CLV target construction
- future-value modeling. :contentReference[oaicite:31]{index=31}

---

## Additional SQL Assets

These SQL files extend the warehouse and support feature engineering for specialized modules.

### 1. `create_view_user_churn_labels.sql`
Creates a snapshot-based churn labeling table `churn_labels_tmp`.

**Main concepts**
- `snapshot_id`
- `obs_date`
- `snapshot_key`
- `unique_user_id`
- `first_purchase_date`
- `last_purchase_date`
- `total_orders`
- `total_gmv`
- `days_since_last_order`
- `customer_age_days`
- churn labels for multiple windows:
  - `is_churned_30d`
  - `is_churned_60d`
  - `is_churned_90d`
  - `is_churned_180d`
  - `is_churned_270d`

**Used in**
- Module 06 churn prediction
- snapshot-based retention modeling. :contentReference[oaicite:32]{index=32}

### 2. `user_category_preference.sql`
Creates user–category preference aggregates.

| Column | Meaning |
|---|---|
| `unique_user_id` | User ID |
| `category` | Product category |
| `category_purchases` | Purchase count in category |
| `category_gmv` | GMV in category |

**Used in**
- recommendation personalization
- preference profiling. :contentReference[oaicite:33]{index=33}

### 3. `user_satisfaction_features.sql`
Creates user-level satisfaction and delivery features.

| Column | Meaning |
|---|---|
| `unique_user_id` | User ID |
| `avg_rating` | Average review score |
| `rating_std` | Rating variability |
| `bad_review_count` | Count of low ratings |
| `avg_delivery_days` | Average delivery days |
| `delayed_orders` | Count of delayed orders |

**Used in**
- churn features
- CLV / satisfaction enrichment
- recommendation user profiling. :contentReference[oaicite:34]{index=34}

---

## Table Relationship Summary

### Core relationship flow

```text
customers_raw ──> dim_user ──┐
                             ├── fact_order ──┬── fact_order_item ──> dim_product
orders_raw ──────────────────┘                ├── fact_payment
                                              └── fact_review

products_raw ──> dim_product
payments_raw ──> fact_payment
reviews_raw  ──> fact_review
order_items_raw ──> fact_order_item
sellers_raw ──> seller attributes used in wide views
This warehouse structure supports a reusable SQL-view layer and feeds all 8 analytical modules in the project.
```

## Module Mapping

| Module                       | Main Data Assets                                                                                                  |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| 01 Satisfaction vs Delivery  | `view_delivery_analysis`, `view_order_satisfaction`, `fact_order`, `fact_review`                                  |
| 02 RFM Segmentation          | `view_user_behavior`                                                                                              |
| 03 Product Category Analysis | `view_category_analysis`, `view_category_sales`, `view_product_sales`                                             |
| 04 Geographic Analysis       | `view_geographic_state_summary`, `view_geographic_city_summary`, `view_buyer_seller_distance`                     |
| 05 Time Series Analysis      | `fact_order`, `fact_order_item`, `dim_product`, wide order-derived notebook tables                                |
| 06 Churn Prediction          | `churn_labels_tmp`, `view_user_behavior`, user-level engineered features                                          |
| 07 CLV Prediction            | `view_user_clv_features`, `view_user_future_gmv`                                                                  |
| 08 Recommendation System     | user–item interaction data built from `fact_order_item`, `fact_review`, `dim_product`, plus user-level enrichment |

This mapping is consistent with the overall project architecture described in the portfolio deck: raw data → ETL → MySQL warehouse → analysis and modeling modules → business insights.

## Notes
- The warehouse uses a pragmatic star-schema-style layout rather than a fully normalized enterprise warehouse.
- Many module-specific analytical datasets are built in notebooks from the warehouse views rather than stored as permanent database tables.
- Churn and CLV modeling both rely on derived time-window logic rather than only static user summaries.