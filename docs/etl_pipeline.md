# ETL Pipeline Documentation

This document describes the Extract, Transform, Load (ETL) pipeline used to populate the E-Commerce Intelligence System database.

## 📋 Overview

The ETL pipeline processes raw CSV files from the Brazilian E-Commerce dataset and loads them into a MySQL database. The pipeline is designed to handle large datasets efficiently using batch processing.

## 🔄 Pipeline Architecture

```
┌─────────────────┐
│   Raw CSV Files │
│   (data/)       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Extract & Read │
│   (Pandas)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Transform &    │
│  Clean Data     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Batch Load to  │
│   MySQL DB      │
└─────────────────┘
```

## 📁 Data Files

### Input Files
Located in `data/` directory:

| File | Records | Size | Description |
|------|---------|------|-------------|
| olist_customers_dataset.csv | ~99,441 | 9.1 MB | Customer information |
| olist_orders_dataset.csv | ~99,441 | 17.8 MB | Order details |
| olist_order_items_dataset.csv | ~112,650 | 15.6 MB | Order items |
| olist_order_payments_dataset.csv | ~103,886 | 5.9 MB | Payment information |
| olist_order_reviews_dataset.csv | ~99,224 | 14.5 MB | Customer reviews |
| olist_products_dataset.csv | ~32,952 | 2.4 MB | Product catalog |
| olist_sellers_dataset.csv | ~3,095 | 177 KB | Seller information |
| olist_geolocation_dataset.csv | ~1,000,000 | 62.3 MB | Geographic data |

## 🔧 ETL Scripts

### Script Location
All ETL scripts are located in `src/etl/` directory.

### Load Scripts

#### 1. load_customers.py
**Purpose**: Load customer data into `customers_raw` table

**Features**:
- Batch processing (1000 records per batch)
- NULL value handling
- Duplicate detection using `INSERT IGNORE`

**Usage**:
```bash
python src/etl/load_customers.py
```

**Table Schema**:
```sql
CREATE TABLE customers_raw (
    customer_id VARCHAR(50),
    customer_unique_id VARCHAR(50),
    customer_zip_code_prefix INT,
    customer_city VARCHAR(100),
    customer_state VARCHAR(10)
);
```

---

#### 2. load_orders.py
**Purpose**: Load order data into `orders_raw` table

**Features**:
- Batch processing
- Date/time parsing
- Foreign key validation

**Usage**:
```bash
python src/etl/load_orders.py
```

**Important Notes**:
- `order_id` is the primary key
- `customer_id` references `customers_raw.customer_id`
- All timestamp fields are stored as VARCHAR(32)

---

#### 3. load_order_items.py
**Purpose**: Load order item data

**Features**:
- Composite key handling (order_id, order_item_id)
- Decimal precision handling
- Sequential item numbering

**Usage**:
```bash
python src/etl/load_order_items.py
```

---

#### 4. load_payments.py
**Purpose**: Load payment information

**Features**:
- Sequential payment tracking
- Payment type validation
- Installment data handling

**Usage**:
```bash
python src/etl/load_payments.py
```

**Payment Types**:
- credit_card
- boleto
- voucher
- debit_card

---

#### 5. load_products.py
**Purpose**: Load product catalog

**Features**:
- Product dimension data
- Category handling
- NULL value management

**Usage**:
```bash
python src/etl/load_products.py
```

---

#### 6. load_reviews.py
**Purpose**: Load customer reviews

**Features**:
- Text data handling (UTF-8)
- Score validation (1-5)
- Timestamp tracking

**Usage**:
```bash
python src/etl/load_reviews.py
```

---

#### 7. load_sellers.py
**Purpose**: Load seller information

**Features**:
- Geographical data
- State code validation

**Usage**:
```bash
python src/etl/load_sellers.py
```

---

## 🔐 Database Configuration

### Configuration File
Location: `src/utils/db.py`

```python
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "your_password",
    "database": "ecommerce_platform",
    "charset": "utf8mb4"
}
```

### Connection Utilities

**get_connection()**: Returns a raw PyMySQL connection
```python
from src.utils.db import get_connection

conn = get_connection()
```

**get_engine()**: Returns a SQLAlchemy engine (for Pandas)
```python
from src.utils.db import get_engine

engine = get_engine()
df = pd.read_sql("SELECT * FROM customers_raw", engine)
```

---

## 🚀 Execution Options

### Option 1: Run Individual Scripts

Execute scripts sequentially to respect foreign key dependencies:

```bash
# 1. Load customers (no dependencies)
python src/etl/load_customers.py

# 2. Load sellers (no dependencies)
python src/etl/load_sellers.py

# 3. Load products (no dependencies)
python src/etl/load_products.py

# 4. Load orders (depends on customers)
python src/etl/load_orders.py

# 5. Load order items (depends on orders, products, sellers)
python src/etl/load_order_items.py

# 6. Load payments (depends on orders)
python src/etl/load_payments.py

# 7. Load reviews (depends on orders)
python src/etl/load_reviews.py
```

### Option 2: Use Jupyter Notebook

Interactive data import with progress tracking:

```bash
jupyter notebook Import_data_into_sql.ipynb
```

Advantages:
- Visual progress tracking
- Cell-by-cell execution
- Error inspection
- Data preview

### Option 3: Automated Script

Create a master script `load_all_data.sh`:

```bash
#!/bin/bash

echo "Starting ETL Pipeline..."

python src/etl/load_customers.py && \
python src/etl/load_sellers.py && \
python src/etl/load_products.py && \
python src/etl/load_orders.py && \
python src/etl/load_order_items.py && \
python src/etl/load_payments.py && \
python src/etl/load_reviews.py && \

echo "ETL Pipeline Completed Successfully!"
```

Make executable and run:
```bash
chmod +x load_all_data.sh
./load_all_data.sh
```

---

## ⚡ Performance Optimization

### Batch Processing
All scripts use batch processing with configurable batch size:

```python
def load_orders_raw(csv_path, batch_size=1000):
    df = pd.read_csv(csv_path)

    for start in range(0, len(df), batch_size):
        end = start + batch_size
        chunk = df.iloc[start:end]
        # Process batch...
```

**Recommended Batch Sizes**:
- Small tables (< 10K records): 1000
- Medium tables (10K-100K): 1000-5000
- Large tables (> 100K): 5000-10000

### Transaction Management
- Each batch is committed independently
- Failed batches roll back automatically
- Use `INSERT IGNORE` to skip duplicates

### Memory Management
For large datasets, use chunked reading:

```python
# Read in chunks
chunk_size = 10000
for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
    process_chunk(chunk)
```

---

## ✅ Data Validation

### Pre-Load Validation
Check CSV files before loading:

```python
import pandas as pd

def validate_csv(csv_path, required_columns):
    df = pd.read_csv(csv_path)
    missing_cols = set(required_columns) - set(df.columns)

    if missing_cols:
        raise ValueError(f"Missing columns: {missing_cols}")

    print(f"✓ {csv_path}: {len(df)} rows, {len(df.columns)} columns")
```

### Post-Load Validation
Verify data after loading:

```sql
-- Check row counts
SELECT
    'customers' as table_name, COUNT(*) as row_count FROM customers_raw
UNION ALL
SELECT 'orders', COUNT(*) FROM orders_raw
UNION ALL
SELECT 'products', COUNT(*) FROM products_raw;

-- Check for NULL values in critical fields
SELECT
    COUNT(*) as null_orders
FROM orders_raw
WHERE customer_id IS NULL;

-- Check referential integrity
SELECT
    COUNT(*) as orphaned_orders
FROM orders_raw o
LEFT JOIN customers_raw c ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. Connection Errors
**Error**: `Can't connect to MySQL server`

**Solution**:
- Verify MySQL is running: `mysql -u root -p`
- Check credentials in `src/utils/db.py`
- Ensure database exists: `SHOW DATABASES;`

#### 2. Character Encoding Issues
**Error**: `UnicodeDecodeError`

**Solution**:
- Ensure CSV files are UTF-8 encoded
- Add encoding parameter: `pd.read_csv(path, encoding='utf-8')`

#### 3. Memory Errors
**Error**: `MemoryError` or out of memory

**Solution**:
- Reduce batch size
- Use chunked reading
- Close connections after use

#### 4. Foreign Key Violations
**Error**: `Cannot add or update a child row`

**Solution**:
- Ensure parent tables are loaded first
- Check for missing foreign key values
- Use `INSERT IGNORE` to skip invalid records

---

## 📊 Monitoring & Logging

### Progress Tracking
Each script prints progress:

```
Inserted 1000 rows
Inserted 2000 rows
...
```

### Logging
Enable detailed logging in `src/utils/log.py`:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('etl.log'),
        logging.StreamHandler()
    ]
)
```

---

## 🔄 Refresh & Update Strategies

### Full Reload
Drop and recreate tables:
```bash
mysql -u root -p < sql/ecommerce_platform.sql
```

### Incremental Update
For incremental updates, use:
```sql
INSERT IGNORE INTO orders_raw
VALUES (...);

-- Or use REPLACE INTO for upserts
REPLACE INTO orders_raw
VALUES (...);
```

---

## 📚 Related Documentation

- [Data Dictionary](data_dictionary.md) - Table structures and definitions
- [Database Design](database_design.md) - ER diagrams
- [Quick Start Guide](quickstart.md) - Setup instructions

---

## 🔗 References

- [Brazilian E-Commerce Dataset](https://www.kaggle.com/olistbr/brazilian-ecommerce)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [PyMySQL Documentation](https://pymysql.readthedocs.io/)
