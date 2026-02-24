DROP DATABASE IF EXISTS ecommerce_platform;
CREATE DATABASE ecommerce_platform
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_0900_ai_ci;
USE ecommerce_platform;
CREATE TABLE customers_raw(
	customer_id VARCHAR(50),
    customer_unique_id VARCHAR(50),
    customer_zip_code_prefix INT,
    customer_city VARCHAR(100),
    customer_state VARCHAR(10)
);

DROP TABLE IF EXISTS orders_raw;
CREATE TABLE orders_raw (
  order_id VARCHAR(50),
  customer_id VARCHAR(50),
  order_status VARCHAR(50),
  order_purchase_timestamp VARCHAR(32),
  order_approved_at VARCHAR(32),
  order_delivered_carrier_date VARCHAR(32),
  order_delivered_customer_date VARCHAR(32),
  order_estimated_delivery_date VARCHAR(32),
  PRIMARY KEY (order_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
	
DROP TABLE IF EXISTS products_raw;
CREATE TABLE products_raw (
  product_id VARCHAR(50) PRIMARY KEY,
  product_category_name VARCHAR(100),
  product_name_lenght INT,
  product_description_lenght INT,
  product_photos_qty INT,
  product_weight_g INT,
  product_length_cm INT,
  product_height_cm INT,
  product_width_cm INT
);   
DESCRIBE products_raw;

DROP TABLE IF EXISTS payments_raw;
CREATE TABLE payments_raw (
  order_id VARCHAR(50),
  payment_sequential INT,
  payment_type VARCHAR(50),
  payment_installments INT,
  payment_value DECIMAL(10,2),
  PRIMARY KEY (order_id, payment_sequential)
); 

DROP TABLE IF EXISTS reviews_raw;
CREATE TABLE reviews_raw (
  review_id VARCHAR(50), 
  order_id VARCHAR(50),
  review_score INT,
  review_comment_title TEXT,
  review_comment_message TEXT,
  review_creation_date DATETIME,
  review_answer_timestamp DATETIME,
  PRIMARY KEY (review_id, order_id)
);

CREATE TABLE order_items_raw(
	order_id VARCHAR(50),
	order_item_id INT,
    product_id VARCHAR(50),
    seller_id VARCHAR(50),
    shipping_limit_date VARCHAR(32),
    price DECIMAL(10, 2),
    freight_value DECIMAL(10, 2),
    PRIMARY KEY (order_id, order_item_id)
);
DESCRIBE order_items_raw;

DROP TABLE IF EXISTS fact_review;
DROP TABLE IF EXISTS fact_payment;
DROP TABLE IF EXISTS fact_order_item;
DROP TABLE IF EXISTS fact_order;
DROP TABLE IF EXISTS dim_product;
DROP TABLE IF EXISTS dim_user;

CREATE TABLE dim_user (
  user_id VARCHAR(50) PRIMARY KEY,          -- customer_id
  unique_user_id VARCHAR(50) NOT NULL,      -- customer_unique_id
  city VARCHAR(100),
  state VARCHAR(10)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE dim_product (
  product_id VARCHAR(50) PRIMARY KEY,
  category VARCHAR(100),
  weight_g INT,
  length_cm INT,
  height_cm INT,
  width_cm INT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE fact_order (
  order_id VARCHAR(50) PRIMARY KEY,
  user_id VARCHAR(50) NOT NULL,
  order_status VARCHAR(50),
  purchase_ts DATETIME,
  delivered_ts DATETIME,
  estimated_delivery_ts DATETIME,
  delivered_days INT,
  FOREIGN KEY (user_id) REFERENCES dim_user(user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX idx_order_user_purchase ON fact_order(user_id, purchase_ts);

CREATE TABLE fact_order_item (
  order_id VARCHAR(50) NOT NULL,
  order_item_id INT NOT NULL,
  product_id VARCHAR(50) NOT NULL,
  seller_id VARCHAR(50),
  shipping_limit_ts DATETIME,
  price DECIMAL(10,2),
  freight_value DECIMAL(10,2),
  gmv DECIMAL(10,2),
  PRIMARY KEY (order_id, order_item_id),
  FOREIGN KEY (order_id) REFERENCES fact_order(order_id),
  FOREIGN KEY (product_id) REFERENCES dim_product(product_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX idx_item_product ON fact_order_item(product_id);

DROP TABLE IF EXISTS fact_payment;
CREATE TABLE fact_payment (
  order_id VARCHAR(50) NOT NULL,
  payment_sequential INT NOT NULL,
  payment_type VARCHAR(50),
  payment_installments INT,
  payment_value DECIMAL(10,2),
  FOREIGN KEY (order_id) REFERENCES fact_order(order_id),
  PRIMARY KEY (order_id, payment_sequential)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS fact_review;
CREATE TABLE fact_review (
  review_id VARCHAR(50) PRIMARY KEY,
  order_id VARCHAR(50) NOT NULL,
  review_score INT,
  review_comment_len INT,
  review_creation_ts VARCHAR(32),
  review_answer_ts VARCHAR(32),
  FOREIGN KEY (order_id) REFERENCES fact_order(order_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE sellers_raw (
	seller_id VARCHAR(50) PRIMARY KEY,
    seller_zip_code_prefix varchar(5),
    seller_city VARCHAR(100),
    seller_state varchar(5)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX idx_review_order ON fact_review(order_id);

INSERT INTO dim_user (user_id, unique_user_id, city, state)
SELECT DISTINCT
  customer_id,
  customer_unique_id,
  customer_city,
  customer_state
FROM customers_raw;

INSERT INTO dim_product (product_id, category, weight_g, length_cm, height_cm, width_cm)
SELECT
  product_id,
  product_category_name,
  product_weight_g,
  product_length_cm,
  product_height_cm,
  product_width_cm
FROM products_raw;
DESCRIBE dim_product;

INSERT INTO fact_order (order_id, user_id, order_status, purchase_ts, delivered_ts, estimated_delivery_ts, delivered_days)
SELECT DISTINCT
  o.order_id,
  o.customer_id AS user_id,
  o.order_status,
  STR_TO_DATE(NULLIF(o.order_purchase_timestamp,''), '%Y-%m-%d %H:%i:%s') AS purchase_ts,
  STR_TO_DATE(NULLIF(o.order_delivered_customer_date,''), '%Y-%m-%d %H:%i:%s') AS delivered_ts,
  STR_TO_DATE(NULLIF(o.order_estimated_delivery_date,''), '%Y-%m-%d %H:%i:%s') AS estimated_delivery_ts,
  CASE
    WHEN order_delivered_customer_date IS NULL OR order_delivered_customer_date='' THEN NULL
    ELSE DATEDIFF(
      STR_TO_DATE(o.order_delivered_customer_date, '%Y-%m-%d %H:%i:%s'),
      STR_TO_DATE(o.order_purchase_timestamp, '%Y-%m-%d %H:%i:%s')
    )
  END AS delivered_days
FROM orders_raw o;


INSERT INTO fact_order_item (order_id, order_item_id, product_id, seller_id, shipping_limit_ts, price, freight_value, gmv)
SELECT
  oi.order_id,
  oi.order_item_id,
  oi.product_id,
  oi.seller_id,
  STR_TO_DATE(NULLIF(shipping_limit_date,''), '%Y-%m-%d %H:%i:%s') AS shipping_limit_ts,
  oi.price,
  oi.freight_value,
  (IFNULL(oi.price,0) + IFNULL(oi.freight_value,0)) AS gmv
FROM order_items_raw oi
JOIN fact_order o ON oi.order_id = o.order_id;

INSERT INTO fact_payment(order_id, payment_sequential, payment_type, payment_installments, payment_value)
SELECT
	p.order_id,
    p.payment_sequential,
    p.payment_type,
    p.payment_installments,
    p.payment_value
FROM payments_raw p
JOIN fact_order o ON p.order_id = o.order_id;

TRUNCATE TABLE fact_review;
INSERT INTO fact_review (
  review_id,
  order_id,
  review_score,
  review_comment_len,
  review_creation_ts,
  review_answer_ts
)
SELECT
  r.review_id,
  MAX(r.order_id) AS order_id,
  MAX(r.review_score) AS review_score,
  MAX(
  CASE
    WHEN r.review_comment_message IS NULL OR r.review_comment_message = '' THEN 0
    ELSE CHAR_LENGTH(r.review_comment_message)
  END) AS review_comment_len,
	MAX(DATE_FORMAT(review_creation_date, '%Y-%m-%d %H:%i:%s')) AS review_creation_ts,
	MAX(DATE_FORMAT(review_answer_timestamp, '%Y-%m-%d %H:%i:%s')) AS review_answer_ts
FROM reviews_raw r
JOIN fact_order o ON r.order_id = o.order_id
GROUP BY r.review_id;
-- Confirm whether the imported data is consistent with the number of data in the csv file
SELECT COUNT(*) FROM orders_raw;
SELECT * FROM orders_raw;

TRUNCATE TABLE orders_raw;
TRUNCATE TABLE order_items_raw;

SELECT COUNT(*) FROM order_items_raw;

TRUNCATE TABLE dim_product;

SELECT COUNT(*) FROM products_raw;

TRUNCATE TABLE customers_raw;
SELECT COUNT(*) FROM customers_raw;

SELECT COUNT(*) FROM payments_raw;
TRUNCATE TABLE payments_raw;

TRUNCATE TABLE reviews_raw;
SELECT COUNT(*) FROM reviews_raw;

SELECT COUNT(*) FROM sellers_raw;

-- Check whether all the checklists have been created.
SELECT 
	table_name,
    table_rows
FROM information_schema.tables
WHERE table_schema = 'ecommerce_platform'
ORDER BY table_name;

SELECT COUNT(*) FROM dim_user;
SELECT COUNT(*) FROM dim_product;
SELECT COUNT(*) FROM fact_order;
SELECT COUNT(*) FROM fact_order_item;
SELECT COUNT(*) FROM fact_payment;
SELECT COUNT(*) FROM fact_review;

-- These two numbers must be exactly the same, indicating that there is no duplicate order_id.
SELECT COUNT(*) FROM fact_order;
SELECT COUNT(*) AS total_rows,
       COUNT(DISTINCT order_id) AS distinct_orders
FROM fact_order;

-- Check if there are duplicate values ​​in the table
SELECT r.review_id, COUNT(*)
FROM reviews_raw r
JOIN fact_order o ON r.order_id = o.order_id
GROUP BY r.review_id
HAVING COUNT(*) > 1;

-- Solve the problem that two tables use a primary key at the same time
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE fact_review;
TRUNCATE TABLE fact_payment;
TRUNCATE TABLE fact_order_item;
TRUNCATE TABLE fact_order;
SET FOREIGN_KEY_CHECKS = 1;

-- General inspection
USE ecommerce_platform;

-- Look at the true number of rows per fact/dimension table
SELECT 
  'dim_user'       AS tbl, COUNT(*) AS cnt FROM dim_user
UNION ALL
SELECT 'dim_product',      COUNT(*) FROM dim_product
UNION ALL
SELECT 'fact_order',       COUNT(*) FROM fact_order
UNION ALL
SELECT 'fact_order_item',  COUNT(*) FROM fact_order_item
UNION ALL
SELECT 'fact_payment',     COUNT(*) FROM fact_payment
UNION ALL
SELECT 'fact_review',      COUNT(*) FROM fact_review;
