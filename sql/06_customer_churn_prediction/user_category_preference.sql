SELECT
    u.unique_user_id,
    p.category,
    COUNT(*) AS category_purchases,
    SUM(oi.gmv) AS category_gmv
FROM fact_order o
JOIN dim_user u
    ON o.user_id = u.user_id
JOIN fact_order_item oi
    ON o.order_id = oi.order_id
LEFT JOIN dim_product p
    ON oi.product_id = p.product_id
WHERE p.category IS NOT NULL
  AND o.order_status = 'delivered'
GROUP BY u.unique_user_id, p.category