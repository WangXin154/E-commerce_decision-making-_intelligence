USE ecommerce_platform;

-- 1.User behavior analysis view
DROP VIEW IF EXISTS view_user_behavior;
CREATE VIEW view_user_behavior AS
SELECT 
	u.user_id,
    u.city,
    u.state,
    
    -- frequency number of purchases
    COUNT(DISTINCT o.order_id) AS order_count,
    
    -- Monetary Total consumption and average customer price
    SUM(oi.gmv) AS total_spent,
    AVG(oi.gmv) AS avg_order_value,
    
    -- Recency Last purchase time and days since today
    MAX(o.purchase_ts) AS last_purchase_date,
    DATEDIFF(NOW(), MAX(o.purchase_ts)) AS days_since_last_purchase,
    
    -- Time to first purchase and lifecycle
    MIN(o.purchase_ts) AS first_purchase_date,
    DATEDIFF(MAX(o.purchase_ts), MIN(o.purchase_ts)) AS customer_lifetime_days

FROM dim_user u
LEFT JOIN fact_order o ON u.user_id = o.user_id
LEFT JOIN fact_order_item oi ON o.order_id = oi.order_id
GROUP BY u.user_id, u.city, u.state;

-- See the distribution of totalspent(A small number of users contribute a lot of revenue)
SELECT
  MIN(total_spent),
  AVG(total_spent),
  MAX(total_spent)
FROM view_user_behavior;

-- View the distribution of ordercount(Almost all users have only bought it once)
SELECT
  order_count,
  COUNT(*) AS user_cnt
FROM view_user_behavior
GROUP BY order_count
ORDER BY order_count;
-- View the distribution of dayssincelast_purchase
SELECT
  MIN(days_since_last_purchase),
  AVG(days_since_last_purchase),
  MAX(days_since_last_purchase)
FROM view_user_behavior
ORDER BY order_count;
