USE ecommerce_platform;

-- 1.User behavior analysis view
DROP VIEW IF EXISTS view_user_behavior;
CREATE VIEW view_user_behavior AS
SELECT 
	u.unique_user_id,
    u.city,
    u.state,
    -- frequency number of purchases
    COUNT(DISTINCT o.order_id) AS order_count,
   -- Monetary Total consumption and average customer price
    SUM(oi.gmv) AS total_spent,
    AVG(oi.gmv) AS avg_order_value,
    -- Recency Last purchase time and days since today
    MAX(o.purchase_ts) AS last_purchase_date,
    DATEDIFF('2018-09-01', MAX(o.purchase_ts)) AS days_since_last_purchase,
    -- Time to first purchase and lifecycle
    MIN(o.purchase_ts) AS first_purchase_date,
    DATEDIFF(MAX(o.purchase_ts), MIN(o.purchase_ts)) AS customer_lifetime_days
FROM dim_user u
LEFT JOIN fact_order o ON u.user_id = o.user_id
LEFT JOIN fact_order_item oi ON o.order_id = oi.order_id
GROUP BY u.unique_user_id, u.city, u.state;

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

USE ecommerce_platform;

DROP VIEW IF EXISTS view_category_analysis;
CREATE VIEW view_category_analysis AS
SELECT
    p.category,

    COUNT(DISTINCT oi.order_id) AS order_count,
    COUNT(DISTINCT o.user_id) AS customer_count,
    SUM(oi.price) AS total_revenue,
    SUM(oi.gmv) AS total_gmv,
    AVG(oi.price) AS avg_price,
    AVG(oi.freight_value) AS avg_freight,

    AVG(r.review_score) AS avg_review_score,
    SUM(CASE WHEN r.review_score <= 2 THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(r.review_id), 0) AS bad_review_rate,
    AVG(r.review_comment_len) AS avg_comment_len,

    COUNT(DISTINCT oi.order_id) * 1.0 / NULLIF(COUNT(DISTINCT o.user_id), 0) AS repeat_rate,

    MIN(o.purchase_ts) AS first_sale_date,
    MAX(o.purchase_ts) AS last_sale_date,
    DATEDIFF(MAX(o.purchase_ts), MIN(o.purchase_ts)) AS category_lifetime_days

FROM dim_product p
LEFT JOIN fact_order_item oi
    ON p.product_id = oi.product_id
LEFT JOIN fact_order o
    ON oi.order_id = o.order_id
LEFT JOIN fact_review r
    ON o.order_id = r.order_id
WHERE p.category IS NOT NULL
GROUP BY p.category;


--  Create State-level summary view
CREATE OR REPLACE VIEW view_geographic_state_summary AS
SELECT
    u.state AS customer_state,

    -- Number of users and order volume
    COUNT(DISTINCT o.order_id) AS order_count,
    COUNT(DISTINCT o.user_id) AS customer_count,

    -- Sales indicators
    SUM(order_item_summary.order_gmv) AS total_gmv,
    SUM(order_item_summary.order_revenue) AS total_revenue,
    SUM(order_item_summary.order_gmv) / NULLIF(COUNT(DISTINCT o.order_id), 0) AS avg_order_value,

    -- Logistics metrics (at the order level)
    AVG(o.delivered_days) AS avg_delivery_days,
    AVG(order_item_summary.order_freight) AS avg_freight_cost,
    SUM(
        CASE
            WHEN o.delivered_days > DATEDIFF(o.estimated_delivery_ts, o.purchase_ts)
            THEN 1 ELSE 0
        END
    ) * 100.0 / NULLIF(COUNT(DISTINCT o.order_id), 0) AS delay_rate,

    -- Satisfaction Metrics (Order Level)
    AVG(r.review_score) AS avg_review_score,
    SUM(CASE WHEN r.review_score <= 2 THEN 1 ELSE 0 END) * 100.0 /
        NULLIF(COUNT(r.review_id), 0) AS bad_review_rate,

    -- Re-purchase metrics
    COUNT(DISTINCT o.order_id) * 1.0 /
        NULLIF(COUNT(DISTINCT o.user_id), 0) AS repeat_rate

FROM dim_user u
JOIN fact_order o
    ON u.user_id = o.user_id
LEFT JOIN (
    SELECT
        order_id,
        SUM(gmv) AS order_gmv,
        SUM(price) AS order_revenue,
        SUM(freight_value) AS order_freight
    FROM fact_order_item
    GROUP BY order_id
) AS order_item_summary
    ON o.order_id = order_item_summary.order_id
LEFT JOIN fact_review r
    ON o.order_id = r.order_id
WHERE u.state IS NOT NULL
GROUP BY u.state;



-- Create City-level summary view
CREATE OR REPLACE VIEW view_geographic_city_summary AS
SELECT
    u.state AS customer_state,
    u.city AS customer_city,

    COUNT(DISTINCT o.order_id) AS order_count,
    COUNT(DISTINCT o.user_id) AS customer_count,

    SUM(order_item_summary.order_gmv) AS total_gmv,
    SUM(order_item_summary.order_revenue) AS total_revenue,
    SUM(order_item_summary.order_gmv) / NULLIF(COUNT(DISTINCT o.order_id), 0) AS avg_order_value,

    AVG(o.delivered_days) AS avg_delivery_days,
    AVG(order_item_summary.order_freight) AS avg_freight_cost,

    AVG(r.review_score) AS avg_review_score,
    SUM(CASE WHEN r.review_score <= 2 THEN 1 ELSE 0 END) * 100.0 /
        NULLIF(COUNT(r.review_id), 0) AS bad_review_rate

FROM dim_user u
JOIN fact_order o
    ON u.user_id = o.user_id
LEFT JOIN (
    SELECT
        order_id,
        SUM(gmv) AS order_gmv,
        SUM(price) AS order_revenue,
        SUM(freight_value) AS order_freight
    FROM fact_order_item
    GROUP BY order_id
) AS order_item_summary
    ON o.order_id = order_item_summary.order_id
LEFT JOIN fact_review r
    ON o.order_id = r.order_id
WHERE u.state IS NOT NULL
  AND u.city IS NOT NULL
GROUP BY u.state, u.city;


DROP VIEW IF EXISTS view_buyer_seller_distance;
CREATE VIEW view_buyer_seller_distance AS
SELECT
    o.order_id,
    u.state AS buyer_state,
    u.city AS buyer_city,
    s.seller_state,
    s.seller_city,
    CASE
        WHEN u.state = s.seller_state THEN 'Same State'
        ELSE 'Cross State'
    END AS trade_type,
    o.delivered_days,
    oi.freight_value,
    oi.gmv,
    r.review_score
FROM fact_order o
JOIN dim_user u
    ON o.user_id = u.user_id
JOIN fact_order_item oi
    ON o.order_id = oi.order_id
LEFT JOIN sellers_raw s
    ON oi.seller_id = s.seller_id
LEFT JOIN fact_review r
    ON o.order_id = r.order_id
WHERE u.state IS NOT NULL
  AND s.seller_state IS NOT NULL;
  
  
  -- Create view_user_clv_features for 07_Customer_Lifetime_Value_Prediction
DROP VIEW IF EXISTS view_user_clv_features;
  CREATE OR REPLACE VIEW view_user_clv_features AS
WITH delivered_orders AS (
    SELECT
        c.customer_unique_id,
        o.order_id,
        o.order_purchase_timestamp,
        o.order_delivered_customer_date,
        o.order_estimated_delivery_date
    FROM customers_raw c
    JOIN orders_raw o
        ON c.customer_id = o.customer_id
    WHERE o.order_status = 'delivered'
     AND o.order_purchase_timestamp < '2017-07-01'
),

order_value AS (
    SELECT
        oi.order_id,
        SUM(oi.price + oi.freight_value) AS order_gmv
    FROM order_items_raw oi
    GROUP BY oi.order_id
),

payment_agg AS (
    SELECT
        p.order_id,
        SUM(p.payment_value) AS order_payment_value,
        MAX(p.payment_installments) AS max_installments_used
    FROM payments_raw p
    GROUP BY p.order_id
),

review_agg AS (
    SELECT
        r.order_id,
        AVG(r.review_score) AS review_score
    FROM reviews_raw r
    GROUP BY r.order_id
),

product_diversity AS (
    SELECT
        c.customer_unique_id,
        COUNT(DISTINCT oi.product_id) AS unique_products_purchased,
        COUNT(DISTINCT pr.product_category_name) AS unique_categories_purchased
    FROM customers_raw c
    JOIN orders_raw o
        ON c.customer_id = o.customer_id
    JOIN order_items_raw oi
        ON o.order_id = oi.order_id
    LEFT JOIN products_raw pr
        ON oi.product_id = pr.product_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id
),

user_order_base AS (
    SELECT
        d.customer_unique_id,
        d.order_id,
        d.order_purchase_timestamp,
        d.order_delivered_customer_date,
        d.order_estimated_delivery_date,
        ov.order_gmv,
        pa.order_payment_value,
        pa.max_installments_used,
        ra.review_score
    FROM delivered_orders d
    LEFT JOIN order_value ov
        ON d.order_id = ov.order_id
    LEFT JOIN payment_agg pa
        ON d.order_id = pa.order_id
    LEFT JOIN review_agg ra
        ON d.order_id = ra.order_id
)

SELECT
    u.customer_unique_id,

    COUNT(DISTINCT u.order_id) AS total_orders,
    SUM(u.order_gmv) AS total_gmv,
    AVG(u.order_gmv) AS avg_order_value,

    MIN(u.order_purchase_timestamp) AS first_order_date,
    MAX(u.order_purchase_timestamp) AS last_order_date,
    DATEDIFF(MAX(u.order_purchase_timestamp), MIN(u.order_purchase_timestamp)) AS customer_lifetime_days,
    DATEDIFF('2017-07-01', MAX(u.order_purchase_timestamp)) AS days_since_last_order,

    COUNT(DISTINCT u.order_id) * 30.0 /
        NULLIF(GREATEST(DATEDIFF(MAX(u.order_purchase_timestamp), MIN(u.order_purchase_timestamp)), 1), 0)
        AS monthly_frequency,

    pd.unique_products_purchased,
    pd.unique_categories_purchased,

    AVG(u.order_payment_value) AS avg_payment_value,
    MAX(u.max_installments_used) AS max_installments_used,

    AVG(u.review_score) AS avg_review_score,
    AVG(CASE WHEN u.review_score >= 4 THEN 1 ELSE 0 END) AS satisfaction_rate,
    SUM(CASE WHEN u.review_score <= 2 THEN 1 ELSE 0 END) AS bad_review_count,

    AVG(
        DATEDIFF(
            u.order_delivered_customer_date,
            u.order_estimated_delivery_date
        )
    ) AS avg_delivery_delay,

    AVG(
        CASE
            WHEN u.order_delivered_customer_date > u.order_estimated_delivery_date THEN 1
            ELSE 0
        END
    ) AS delay_rate

FROM user_order_base u
LEFT JOIN product_diversity pd
    ON u.customer_unique_id = pd.customer_unique_id
GROUP BY
    u.customer_unique_id,
    pd.unique_products_purchased,
    pd.unique_categories_purchased;

-- Validate the repaired view
SELECT
    MIN(days_since_last_order) AS min_dslo,
    MAX(days_since_last_order) AS max_dslo,
    AVG(days_since_last_order) AS avg_dslo,
    COUNT(*) AS total_customers
FROM view_user_clv_features;
    
-- view_user_future_gmv for 07_Customer_Lifetime_Value_Prediction
CREATE OR REPLACE VIEW view_user_future_gmv AS
SELECT
    c.customer_unique_id,

    SUM(
        CASE
            WHEN o.order_purchase_timestamp >= '2017-07-01'
             AND o.order_purchase_timestamp < '2018-01-01'
            THEN oi.price + oi.freight_value
            ELSE 0
        END
    ) AS future_6m_gmv,

    COUNT(
        DISTINCT CASE
            WHEN o.order_purchase_timestamp >= '2017-07-01'
             AND o.order_purchase_timestamp < '2018-01-01'
            THEN o.order_id
            ELSE NULL
        END
    ) AS future_6m_orders,

    CASE
        WHEN COUNT(
            DISTINCT CASE
                WHEN o.order_purchase_timestamp >= '2017-07-01'
                 AND o.order_purchase_timestamp < '2018-01-01'
                THEN o.order_id
                ELSE NULL
            END
        ) > 0 THEN 1
        ELSE 0
    END AS is_active_future

FROM customers_raw c
LEFT JOIN orders_raw o
    ON c.customer_id = o.customer_id
LEFT JOIN order_items_raw oi
    ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
GROUP BY c.customer_unique_id;

SELECT * FROM view_user_clv_features LIMIT 5;
SELECT * FROM view_user_future_gmv LIMIT 5;