# Data Dictionary

This document provides a detailed description of all database tables and their fields in the E-Commerce Intelligence System.

## 📊 Database Schema

### 1. customers_raw

Customer information table.

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| customer_id | VARCHAR(50) | Unique customer identifier | 00012e2a6acb5febe7f2d34c15ca34b9 |
| customer_unique_id | VARCHAR(50) | Unique identifier for customer across all orders | 7b33db25497c3f0b754a2bd11956f8e7 |
| customer_zip_code_prefix | INT | Zip code prefix | 14409 |
| customer_city | VARCHAR(100) | Customer city | sao paulo |
| customer_state | VARCHAR(10) | Customer state (2-letter code) | SP |

**Constraints**: None
**Primary Key**: customer_id

---

### 2. orders_raw

Order information table.

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| order_id | VARCHAR(50) | Unique order identifier (PK) | 00010242fe6c5a6f1d23712d845882a8 |
| customer_id | VARCHAR(50) | Foreign key to customers_raw | 00012e2a6acb5febe7f2d34c15ca34b9 |
| order_status | VARCHAR(50) | Order status | delivered |
| order_purchase_timestamp | VARCHAR(32) | Purchase timestamp | 2017-09-14 11:27:45 |
| order_approved_at | VARCHAR(32) | Order approval timestamp | 2017-09-14 11:28:10 |
| order_delivered_carrier_date | VARCHAR(32) | Delivery to carrier timestamp | 2017-09-16 03:57:40 |
| order_delivered_customer_date | VARCHAR(32) | Delivery to customer timestamp | 2017-09-19 20:53:13 |
| order_estimated_delivery_date | VARCHAR(32) | Estimated delivery timestamp | 2017-10-09 23:59:59 |

**Constraints**: Primary Key (order_id)
**Foreign Key**: customer_id → customers_raw.customer_id

**Order Status Values**:
- created: Order created
- approved: Payment approved
- invoiced: Invoice issued
- processing: In processing
- shipped: Shipped
- delivered: Delivered
- unavailable: Unavailable
- canceled: Canceled

---

### 3. order_items_raw

Order items and product details.

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| order_id | VARCHAR(50) | Order identifier (FK) | 00010242fe6c5a6f1d23712d845882a8 |
| order_item_id | INT | Sequential item number in order | 1 |
| product_id | VARCHAR(50) | Product identifier | 4244733e06e7ecb4970a6e2683c13e61 |
| seller_id | VARCHAR(50) | Seller identifier | 48436dade18ac8b4b5d845f7b99d1c85 |
| shipping_limit_date | VARCHAR(32) | Shipping deadline | 2017-09-19 00:00:00 |
| price | DECIMAL(10,2) | Item price | 58.90 |
| freight_value | DECIMAL(10,2) | Freight value | 13.29 |

**Constraints**: Primary Key (order_id, order_item_id)
**Foreign Keys**:
- order_id → orders_raw.order_id
- product_id → products_raw.product_id
- seller_id → sellers_raw.seller_id

---

### 4. payments_raw

Payment information.

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| order_id | VARCHAR(50) | Order identifier (FK) | 00010242fe6c5a6f1d23712d845882a8 |
| payment_sequential | INT | Payment sequence number | 1 |
| payment_type | VARCHAR(50) | Payment method | credit_card |
| payment_installments | INT | Number of installments | 1 |
| payment_value | DECIMAL(10,2) | Payment amount | 58.90 |

**Constraints**: Primary Key (order_id, payment_sequential)
**Foreign Key**: order_id → orders_raw.order_id

**Payment Types**:
- credit_card: Credit card payment
- boleto: Brazilian boleto payment
- voucher: Voucher payment
- debit_card: Debit card payment
- not_defined: Undefined payment type

---

### 5. products_raw

Product catalog information.

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| product_id | VARCHAR(50) | Unique product identifier (PK) | 4244733e06e7ecb4970a6e2683c13e61 |
| product_category_name | VARCHAR(100) | Product category | moveis_escritorio |
| product_name_lenght | INT | Product name length | 62 |
| product_description_lenght | INT | Product description length | 321 |
| product_photos_qty | INT | Number of product photos | 4 |
| product_weight_g | INT | Product weight (grams) | 725 |
| product_length_cm | INT | Product length (cm) | 16 |
| product_height_cm | INT | Product height (cm) | 10 |
| product_width_cm | INT | Product width (cm) | 14 |

**Constraints**: Primary Key (product_id)

---

### 6. reviews_raw

Customer review information.

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| review_id | VARCHAR(50) | Unique review identifier | 7bc6e4b13d93680f39680626ef66e0cb |
| order_id | VARCHAR(50) | Order identifier (FK) | 00010242fe6c5a6f1d23712d845882a8 |
| review_score | INT | Review score (1-5) | 4 |
| review_comment_title | TEXT | Review comment title | omiti |
| review_comment_message | TEXT | Review comment message |omitiram... |
| review_creation_date | VARCHAR(32) | Review creation date | 2017-09-14 15:46:17 |
| review_answer_timestamp | VARCHAR(32) | Review response timestamp | 2017-09-15 14:27:44 |

**Constraints**: Primary Key (review_id)
**Foreign Key**: order_id → orders_raw.order_id

**Review Scores**:
- 1: Very dissatisfied
- 2: Dissatisfied
- 3: Neutral
- 4: Satisfied
- 5: Very satisfied

---

### 7. sellers_raw

Seller information.

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| seller_id | VARCHAR(50) | Unique seller identifier (PK) | 48436dade18ac8b4b5d845f7b99d1c85 |
| seller_zip_code_prefix | INT | Seller zip code prefix | 13023 |
| seller_city | VARCHAR(100) | Seller city | campinas |
| seller_state | VARCHAR(10) | Seller state | SP |

**Constraints**: Primary Key (seller_id)

---

### 8. geolocation_raw

Geographic location data.

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| geolocation_zip_code_prefix | INT | Zip code prefix | 1037 |
| geolocation_lat | DECIMAL(10,6) | Latitude | -23.550451 |
| geolocation_lng | DECIMAL(10,6) | Longitude | -46.633108 |
| geolocation_city | VARCHAR(100) | City name | sao paulo |
| geolocation_state | VARCHAR(10) | State code | SP |

**Constraints**: None

---

## 🔄 Entity Relationships

```
customers_raw (1) ──< (N) orders_raw (1) ──< (N) order_items_raw
                                                  │
                                                  │ (N)
                                                  │
                                              products_raw
                                                  │
                                                  │ (1)
                                                  │
                                              sellers_raw
                                                  │
                                                  │ (1)
                                                  │
orders_raw (1) ──< (N) payments_raw
orders_raw (1) ──< (N) reviews_raw
```

## 📈 Data Statistics

- **Total Customers**: ~100,000
- **Total Orders**: ~100,000
- **Total Products**: ~30,000
- **Total Sellers**: ~3,000
- **Date Range**: September 2016 - October 2018

## 🔍 Notes

1. All timestamps are in UTC-3 (Brazil time)
2. Currency is in Brazilian Real (BRL)
3. Zip codes are Brazilian format (5-digit + 3-digit)
4. Product categories are in Portuguese (see `product_category_name_translation.csv` for English translations)

## 📚 Related Documentation

- [ETL Pipeline](etl_pipeline.md) - How data is loaded into the database
- [Database Design](database_design.md) - ER diagrams and relationships
- [API Reference](api_reference.md) - How to query this data
