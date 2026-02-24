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

-- 1)See the distribution of totalspent(A small number of users contribute a lot of revenue)
SELECT
  MIN(total_spent),
  AVG(total_spent),
  MAX(total_spent)
FROM view_user_behavior;

-- 2)View the distribution of ordercount(Almost all users have only bought it once)
SELECT
  order_count,
  COUNT(*) AS user_cnt
FROM view_user_behavior
GROUP BY order_count
ORDER BY order_count;
-- 3)View the distribution of dayssincelast_purchase
SELECT
  MIN(days_since_last_purchase),
  AVG(days_since_last_purchase),
  MAX(days_since_last_purchase)
FROM view_user_behavior
ORDER BY order_count;


-- 2.Product sales analysis view
DROP VIEW IF EXISTS view_product_sales;
CREATE VIEW view_product_sales AS 
SELECT 
	p.product_id,
    p.category,
  -- Sales metrics
    COUNT(oi.order_id) AS sales_count, -- How many times this item has been sold (once in an order)
    SUM(oi.price) AS total_revenue,
    SUM(oi.gmv) AS total_gmv,
    AVG(oi.price) AS avg_price,
    -- Evaluation indicators
    AVG(r.review_score) AS avg_review_score,
    COUNT(r.review_id) AS review_count,
   -- Time indicators
    MIN(o.purchase_ts) AS first_sale_date,
    MAX(o.purchase_ts) AS last_sale_date
FROM dim_product p
LEFT JOIN fact_order_item oi ON p.product_id = oi.product_id
LEFT JOIN fact_order o ON oi.order_id = o.order_id
LEFT JOIN fact_review r ON o.order_id = r.order_id
GROUP BY p.product_id, p.category;

-- 1)Check out the top popular products
SELECT * FROM view_product_sales
ORDER BY total_gmv DESC
LIMIT 10;


-- 3.Category sales analysis view
DROP VIEW IF EXISTS view_category_sales;
CREATE VIEW view_category_sales AS
SELECT
	v.category,
    -- How many products are there in this category
    COUNT(DISTINCT v.product_id) AS product_count,
    -- Total sales (sum of all product sales)
    SUM(v.sales_count) AS total_sales,
    -- Total sales of categories
    SUM(v.total_revenue) AS category_total_revenue,
    -- The average price of goods under the category
    AVG(v.avg_price) AS avg_product_price,
    -- Category average rating
    AVG(v.avg_review_score) AS avg_review_score
FROM view_product_sales v
GROUP BY v.category;
    
SELECT *
FROM view_category_sales
ORDER BY category_total_revenue DESC
limit 10;    
	
-- 4.Delivert analysis view
DROP VIEW IF EXISTS view_delivery_analysis;
CREATE VIEW view_delivery_analysis AS 
SELECT
	o.order_id,
    u.state AS customer_state,
	o.order_status,
    o.delivered_days,
    -- Estimated delivery days
    DATEDIFF(o.estimated_delivery_ts, o.purchase_ts) AS estimated_days,
    -- if is delay
    CASE
		WHEN o.delivered_days IS NULL
			THEN NULL
		WHEN o.delivered_days > DATEDIFF(o.estimated_delivery_ts, o.purchase_ts)
			THEN 1
		ELSE 0
	END AS is_delayed,
    -- delay_days
    CASE 
		WHEN o.delivered_days IS NULL
			THEN NULL
		ELSE o.delivered_days - DATEDIFF(o.estimated_delivery_ts, o.purchase_ts)
	END AS delay_days,
    -- order_value
    (
	SELECT SUM(gmv)
    FROM fact_order_item
    WHERE order_id = o.order_id
    ) AS order_value,
    r.review_score
FROM fact_order o
LEFT JOIN dim_user u ON u.user_id = o.user_id
LEFT JOIN fact_review r ON r.order_id = o.order_id
WHERE o.delivered_ts IS NOT NULL; -- Just look at the delivery of the order first
    
SELECT *
FROM view_delivery_analysis
LIMIT 10;    
    
SELECT
    customer_state,
    COUNT(*) AS order_count,
    AVG(delivered_days) AS avg_delivered_days,
    SUM(is_delayed) * 100.0 / COUNT(*) AS delay_rate,
    AVG(review_score) AS avg_review_score
FROM view_delivery_analysis
GROUP BY customer_state
ORDER BY delay_rate DESC; 

-- 5.order satifaction view
DROP VIEW IF EXISTS view_order_satisfaction;
CREATE VIEW view_order_satisfaction AS 
SELECT 
	o.order_id,
    u.user_id,
    u.state,
    o.purchase_ts,
    o.delivered_days,
     (
		SELECT SUM(gmv)
        FROM fact_order_item
        WHERE order_id = o.order_id
	) AS order_value,
    r.review_score,
    r.review_comment_len,
    -- satisfaction level
    CASE
		WHEN r.review_score >= 4 
			THEN 'Satisfied'
		WHEN r.review_score = 3
			THEN 'Average'
		WHEN r.review_score <= 2
			THEN 'Dissatisfied'
		ELSE 'Not Rated'
	END AS satisfaction_level,
    -- delivery period
    CASE
		WHEN o.delivered_days IS NULL
			THEN 'Not delivered'
        WHEN o.delivered_days <= 7
			THEN 'Within 1 week'
		WHEN o.delivered_days <= 14
			THEN '1-2 weeks'
		WHEN o.delivered_days <=21 
			THEN '2-3 weeks'
		ELSE 'More than 3 weeks'
	END AS delivery_period
FROM fact_order o
LEFT JOIN dim_user u ON o.user_id = u.user_id
LEFT JOIN fact_review r ON o.order_id = r.order_id;

-- 1)Analysis of satisfaction and delivery time
SELECT 
	delivery_period,
    COUNT(*) AS order_count,
    AVG(review_score) AS avg_score,
    SUM(CASE WHEN review_score >= 4 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS satisfaction_rate
FROM view_order_satisfaction
WHERE review_score IS NOT NULL
GROUP BY delivery_period
ORDER BY
	CASE delivery_period
		WHEN 'Within 1 week'     THEN 1
        WHEN '1-2 weeks'         THEN 2
        WHEN '2-3 weeks'	     THEN 3
        WHEN 'More than 3 weeks' THEN 4
        ELSE 5
	END;
    
-- 6.order complete vew
DROP VIEW IF EXISTS view_order_complete;
CREATE VIEW view_order_complete AS 
SELECT
	o.order_id,
    o.order_status,
    o.purchase_ts,
    o.delivered_ts,
    o.delivered_days,
    o.estimated_delivery_ts,
    u.user_id,
    u.city AS user_city,
    u.state AS user_state,
    p.category AS product_category,
    oi.product_id,
    oi.order_item_id,
    oi.price,
    oi.freight_value,
    oi.gmv,
    oi.seller_id,
    s.seller_city,
    s.seller_state,
    pay.payment_type,
    pay.payment_installments,
    pay.payment_value,
    r.review_score,
    r.review_comment_len,
    CASE
		WHEN o.delivered_days IS NULL
			THEN NULL
		WHEN o.delivered_days > DATEDIFF(o.estimated_delivery_ts, o.purchase_ts) 
			THEN 1
		ELSE 0
	END AS is_delayed,
    CASE
		WHEN r.review_score >= 4 THEN 1
		ELSE 0
	END AS is_satisfied
FROM fact_order_item oi
LEFT JOIN fact_order o 		ON oi.order_id = o.order_id
LEFT JOIN dim_user u 		ON o.user_id = u.user_id
LEFT JOIN dim_product p		ON oi.product_id = p.product_id
LEFT JOIN sellers_raw s 	ON oi.seller_id = s.seller_id
LEFT JOIN fact_payment pay  ON o.order_id = pay.order_id
LEFT JOIN fact_review r 	ON o.order_id = r.order_id;

-- Quickly sample to check structures
SELECT *
FROM view_order_complete
LIMIT 10;
