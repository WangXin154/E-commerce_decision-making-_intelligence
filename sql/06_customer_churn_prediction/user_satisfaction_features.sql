SELECT
    u.unique_user_id,
    AVG(r.review_score) AS avg_rating,
    STDDEV(r.review_score) AS rating_std,
    SUM(CASE WHEN r.review_score <= 2 THEN 1 ELSE 0 END) AS bad_review_count,
    AVG(o.delivered_days) AS avg_delivery_days,
    SUM(
        CASE
            WHEN o.delivered_ts > o.estimated_delivery_ts THEN 1
            ELSE 0
        END
    ) AS delayed_orders
FROM fact_order o
JOIN dim_user u
    ON o.user_id = u.user_id
LEFT JOIN fact_review r
    ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
GROUP BY u.unique_user_id