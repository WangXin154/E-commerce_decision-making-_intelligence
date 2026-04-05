CREATE TABLE churn_labels_tmp AS
WITH params AS (
    SELECT
        MAX(purchase_ts) AS data_end_date
    FROM fact_order
    WHERE order_status = 'delivered'
),
snapshot_dates AS (
    SELECT 1 AS snapshot_id, DATE_SUB(data_end_date, INTERVAL 450 DAY) AS obs_date FROM params
    UNION ALL
SELECT 2 AS snapshot_id, DATE_SUB(data_end_date, INTERVAL 420 DAY) AS obs_date FROM params
    UNION ALL
SELECT 3 AS snapshot_id, DATE_SUB(data_end_date, INTERVAL 390 DAY) AS obs_date FROM params
    UNION ALL
SELECT 4 AS snapshot_id, DATE_SUB(data_end_date, INTERVAL 360 DAY) AS obs_date FROM params
    UNION ALL
SELECT 5 AS snapshot_id, DATE_SUB(data_end_date, INTERVAL 330 DAY) AS obs_date FROM params
    UNION ALL
SELECT 6 AS snapshot_id, DATE_SUB(data_end_date, INTERVAL 300 DAY) AS obs_date FROM params
    UNION ALL
SELECT 7 AS snapshot_id, DATE_SUB(data_end_date, INTERVAL 270 DAY) AS obs_date FROM params
),
order_gmv AS (
    SELECT
        order_id,
        SUM(gmv) AS order_gmv
    FROM fact_order_item
    GROUP BY order_id
),
history_orders AS (
    SELECT
        CONCAT(du.unique_user_id, '__', DATE_FORMAT(sd.obs_date, '%Y%m%d')) AS snapshot_key,
        sd.snapshot_id,
        sd.obs_date,
        du.unique_user_id,
        fo.order_id,
        fo.purchase_ts,
        COALESCE(og.order_gmv, 0) AS order_gmv
    FROM snapshot_dates sd
    JOIN fact_order fo
        ON fo.order_status = 'delivered'
       AND fo.purchase_ts <= sd.obs_date
    JOIN dim_user du
        ON fo.user_id = du.user_id
    LEFT JOIN order_gmv og
        ON fo.order_id = og.order_id
    WHERE du.unique_user_id IS NOT NULL
),
user_history AS (
    SELECT
        snapshot_key,
        snapshot_id,
        obs_date,
        unique_user_id,
        MIN(purchase_ts) AS first_purchase_date,
        MAX(purchase_ts) AS last_purchase_date,
        COUNT(DISTINCT order_id) AS total_orders,
        SUM(order_gmv) AS total_gmv,
        DATEDIFF(obs_date, MAX(purchase_ts)) AS days_since_last_order,
        DATEDIFF(obs_date, MIN(purchase_ts)) AS customer_age_days
    FROM history_orders
    GROUP BY snapshot_key, snapshot_id, obs_date, unique_user_id
),
eligible_users AS (
    SELECT *
    FROM user_history
    WHERE total_orders >= 2
      AND customer_age_days >= 30
      AND days_since_last_order <= 60
),
future_activity AS (
    SELECT
        eu.snapshot_key,
        MAX(CASE WHEN fo.purchase_ts <= DATE_ADD(eu.obs_date, INTERVAL 30 DAY) THEN 1 ELSE 0 END) AS purchased_within_30d,
        MAX(CASE WHEN fo.purchase_ts <= DATE_ADD(eu.obs_date, INTERVAL 60 DAY) THEN 1 ELSE 0 END) AS purchased_within_60d,
        MAX(CASE WHEN fo.purchase_ts <= DATE_ADD(eu.obs_date, INTERVAL 90 DAY) THEN 1 ELSE 0 END) AS purchased_within_90d,
        MAX(CASE WHEN fo.purchase_ts <= DATE_ADD(eu.obs_date, INTERVAL 180 DAY) THEN 1 ELSE 0 END) AS purchased_within_180d,
        MAX(CASE WHEN fo.purchase_ts <= DATE_ADD(eu.obs_date, INTERVAL 270 DAY) THEN 1 ELSE 0 END) AS purchased_within_270d
    FROM eligible_users eu
    JOIN dim_user du
        ON eu.unique_user_id = du.unique_user_id
    JOIN fact_order fo
        ON du.user_id = fo.user_id
    WHERE fo.order_status = 'delivered'
      AND fo.purchase_ts > eu.obs_date
      AND fo.purchase_ts <= DATE_ADD(eu.obs_date, INTERVAL 270 DAY)
    GROUP BY eu.snapshot_key
)
SELECT
    eu.snapshot_key,
    eu.snapshot_id,
    eu.unique_user_id,
    eu.first_purchase_date,
    eu.last_purchase_date,
    eu.obs_date,
    CASE WHEN COALESCE(fa.purchased_within_30d, 0) = 1 THEN 0 ELSE 1 END AS is_churned_30d,
    CASE WHEN COALESCE(fa.purchased_within_60d, 0) = 1 THEN 0 ELSE 1 END AS is_churned_60d,
    CASE WHEN COALESCE(fa.purchased_within_90d, 0) = 1 THEN 0 ELSE 1 END AS is_churned_90d,
    CASE WHEN COALESCE(fa.purchased_within_180d, 0) = 1 THEN 0 ELSE 1 END AS is_churned_180d,
    CASE WHEN COALESCE(fa.purchased_within_270d, 0) = 1 THEN 0 ELSE 1 END AS is_churned_270d,
    eu.total_orders,
    eu.total_gmv,
    eu.days_since_last_order,
    eu.customer_age_days
FROM eligible_users eu
LEFT JOIN future_activity fa
    ON eu.snapshot_key = fa.snapshot_key