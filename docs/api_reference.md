# API Reference

This document provides detailed information about the Python APIs available in the E-Commerce Intelligence System.

## 📋 Table of Contents

- [Database Utilities](#database-utilities)
- [Analysis Modules](#analysis-modules)
- [ETL Modules](#etl-modules)
- [Usage Examples](#usage-examples)

---

## 🔌 Database Utilities

### Module: `src/utils/db.py`

Provides database connection and SQL execution utilities.

#### Functions

##### `get_connection()`

Returns a raw PyMySQL connection to the database.

**Signature**:
```python
def get_connection() -> pymysql.connections.Connection
```

**Returns**: PyMySQL connection object

**Example**:
```python
from src.utils.db import get_connection

conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT * FROM customers_raw LIMIT 10")
results = cursor.fetchall()
conn.close()
```

**Raises**:
- `Exception`: If database connection fails

---

##### `get_engine()`

Returns a SQLAlchemy engine for use with Pandas.

**Signature**:
```python
def get_engine() -> sqlalchemy.engine.Engine
```

**Returns**: SQLAlchemy Engine object

**Example**:
```python
from src.utils.db import get_engine
import pandas as pd

engine = get_engine()
df = pd.read_sql("SELECT * FROM orders_raw", engine)
```

**Note**: Ideal for `pd.read_sql()` and `df.to_sql()` operations

---

##### `execute_sql(conn, sql, params=None)`

Executes a single SQL query with optional parameters.

**Signature**:
```python
def execute_sql(
    conn: pymysql.connections.Connection,
    sql: str,
    params: tuple = None
) -> int
```

**Parameters**:
- `conn`: Database connection
- `sql`: SQL query string
- `params`: Optional parameters for parameterized queries

**Returns**: Number of affected rows

**Example**:
```python
from src.utils.db import get_connection, execute_sql

conn = get_connection()

# Simple query
result = execute_sql(conn, "DELETE FROM orders_raw WHERE order_status = 'canceled'")

# Parameterized query
sql = "SELECT * FROM orders_raw WHERE customer_id = %s"
result = execute_sql(conn, sql, params=('00012e2a6acb5febe7f2d34c15ca34b9',))
```

---

##### `execute_many(conn, sql, params_list)`

Executes a batch SQL operation for multiple records.

**Signature**:
```python
def execute_many(
    conn: pymysql.connections.Connection,
    sql: str,
    params_list: List[tuple]
) -> int
```

**Parameters**:
- `conn`: Database connection
- `sql`: SQL query string
- `params_list`: List of parameter tuples

**Returns**: Number of affected rows

**Example**:
```python
from src.utils.db import get_connection, execute_many

conn = get_connection()

sql = """
INSERT INTO customers_raw (
    customer_id, customer_unique_id, customer_zip_code_prefix,
    customer_city, customer_state
) VALUES (%s, %s, %s, %s, %s)
"""

data = [
    ('id1', 'unique1', 12345, 'São Paulo', 'SP'),
    ('id2', 'unique2', 12346, 'Rio de Janeiro', 'RJ'),
]

execute_many(conn, sql, data)
```

---

##### `close_connection(conn)`

Closes the database connection.

**Signature**:
```python
def close_connection(conn: pymysql.connections.Connection) -> None
```

**Parameters**:
- `conn`: Database connection to close

**Example**:
```python
from src.utils.db import get_connection, close_connection

conn = get_connection()
# ... perform operations ...
close_connection(conn)
```

---

## 📊 Analysis Modules

### Module: `src/analysis/user_behavior_analysis.py`

Provides customer behavior analysis and segmentation capabilities.

#### Class: `UserBehaviorAnalyzer`

##### `__init__(self, engine)`

Initialize the analyzer with a database engine.

**Parameters**:
- `engine`: SQLAlchemy engine (from `get_engine()`)

**Example**:
```python
from src.analysis.user_behavior_analysis import UserBehaviorAnalyzer
from src.utils.db import get_engine

engine = get_engine()
analyzer = UserBehaviorAnalyzer(engine)
```

---

##### `rfm_analysis(self)`

Performs RFM (Recency, Frequency, Monetary) analysis on customers.

**Signature**:
```python
def rfm_analysis(self) -> pd.DataFrame
```

**Returns**: DataFrame with RFM metrics

**Columns**:
- `customer_id`: Customer identifier
- `recency`: Days since last purchase
- `frequency`: Number of purchases
- `monetary`: Total spend amount
- `R_score`: Recency score (1-5)
- `F_score`: Frequency score (1-5)
- `M_score`: Monetary score (1-5)
- `RFM_segment`: Combined segment identifier

**Example**:
```python
rfm_df = analyzer.rfm_analysis()
print(rfm_df.head())

# Get top customers
top_customers = rfm_df[rfm_df['RFM_segment'] == '555']  # Best customers
```

---

##### `customer_segmentation(self, n_clusters=4)`

Performs K-Means clustering on customers.

**Signature**:
```python
def customer_segmentation(self, n_clusters: int = 4) -> pd.DataFrame
```

**Parameters**:
- `n_clusters`: Number of clusters to create (default: 4)

**Returns**: DataFrame with customer segments

**Columns**:
- `customer_id`: Customer identifier
- `cluster`: Cluster assignment (0 to n_clusters-1)
- `recency`: Days since last purchase
- `frequency`: Number of purchases
- `monetary`: Total spend amount

**Example**:
```python
segments = analyzer.customer_segmentation(n_clusters=4)

# Analyze each segment
for cluster_id in range(4):
    cluster_customers = segments[segments['cluster'] == cluster_id]
    print(f"Cluster {cluster_id}:")
    print(f"  Customers: {len(cluster_customers)}")
    print(f"  Avg Monetary: {cluster_customers['monetary'].mean():.2f}")
```

---

### Module: `src/analysis/satisfaction_model.py`

Customer satisfaction analysis and prediction.

#### Class: `SatisfactionModel`

##### `predict_satisfaction(self, order_features)`

Predicts customer satisfaction score based on order features.

**Signature**:
```python
def predict_satisfaction(self, order_features: pd.DataFrame) -> np.ndarray
```

**Parameters**:
- `order_features`: DataFrame with order features

**Required Columns**:
- `delay_days`: Delivery delay in days
- `delivery_duration`: Total delivery duration in days
- `price`: Order value
- `freight_value`: Shipping cost

**Returns**: Array of predicted satisfaction scores (1-5)

**Example**:
```python
from src.analysis.satisfaction_model import SatisfactionModel

model = SatisfactionModel()

# Prepare features
features = pd.DataFrame({
    'delay_days': [2, -1, 5],
    'delivery_duration': [7, 5, 15],
    'price': [100.0, 250.0, 50.0],
    'freight_value': [15.0, 20.0, 10.0]
})

predictions = model.predict_satisfaction(features)
print(predictions)  # e.g., [4, 5, 2]
```

---

## 🔄 ETL Modules

### Module: `src/etl/`

Data loading modules for importing CSV files into the database.

#### Available Loaders

Each loader follows the same pattern:

##### `load_*.py` Functions

**Common Signature**:
```python
def load_*_raw(csv_path: str, batch_size: int = 1000) -> None
```

**Parameters**:
- `csv_path`: Path to CSV file
- `batch_size`: Number of records per batch (default: 1000)

**Available Loaders**:
- `load_customers.py`: Load customer data
- `load_orders.py`: Load order data
- `load_order_items.py`: Load order item data
- `load_payments.py`: Load payment data
- `load_products.py`: Load product data
- `load_reviews.py`: Load review data
- `load_sellers.py`: Load seller data

**Example**:
```python
from src.etl.load_customers import load_customers_raw
from src.etl.load_orders import load_orders_raw

# Load customer data
load_customers_raw('data/olist_customers_dataset.csv', batch_size=1000)

# Load order data
load_orders_raw('data/olist_orders_dataset.csv', batch_size=1000)
```

---

## 💡 Complete Usage Examples

### Example 1: Complete Analysis Workflow

```python
from src.utils.db import get_engine, get_connection, execute_sql
from src.analysis.user_behavior_analysis import UserBehaviorAnalyzer
import pandas as pd

# Initialize
engine = get_engine()
analyzer = UserBehaviorAnalyzer(engine)

# 1. RFM Analysis
print("Performing RFM Analysis...")
rfm = analyzer.rfm_analysis()
print(rfm.describe())

# 2. Customer Segmentation
print("\nPerforming Customer Segmentation...")
segments = analyzer.customer_segmentation(n_clusters=4)

# 3. Analyze segments
for cluster_id in range(4):
    cluster_data = segments[segments['cluster'] == cluster_id]
    print(f"\nCluster {cluster_id}:")
    print(f"  Size: {len(cluster_data)}")
    print(f"  Avg Recency: {cluster_data['recency'].mean():.1f} days")
    print(f"  Avg Frequency: {cluster_data['frequency'].mean():.1f} orders")
    print(f"  Avg Monetary: ${cluster_data['monetary'].mean():.2f}")

# 4. Export results
segments.to_csv('customer_segments.csv', index=False)
print("\nResults exported to customer_segments.csv")
```

### Example 2: Custom Data Query

```python
from src.utils.db import get_engine
import pandas as pd

engine = get_engine()

# Complex multi-table query
sql = """
SELECT
    c.customer_id,
    c.customer_city,
    c.customer_state,
    COUNT(DISTINCT o.order_id) as total_orders,
    SUM(o.order_id) as order_count,
    AVG(r.review_score) as avg_review_score
FROM customers_raw c
LEFT JOIN orders_raw o ON c.customer_id = o.customer_id
LEFT JOIN reviews_raw r ON o.order_id = r.order_id
GROUP BY c.customer_id
HAVING total_orders > 5
ORDER BY avg_review_score DESC
LIMIT 10
"""

top_customers = pd.read_sql(sql, engine)
print(top_customers)
```

### Example 3: Batch Data Processing

```python
from src.utils.db import get_connection, execute_many
import pandas as pd

# Read and transform data
df = pd.read_csv('new_orders.csv')

# Prepare data for insertion
conn = get_connection()

sql = """
INSERT INTO orders_raw (
    order_id, customer_id, order_status,
    order_purchase_timestamp, order_estimated_delivery_date
) VALUES (%s, %s, %s, %s, %s)
"""

# Transform and batch insert
batch_data = []
for _, row in df.iterrows():
    batch_data.append((
        row['order_id'],
        row['customer_id'],
        'created',
        row['timestamp'],
        row['estimated_delivery']
    ))

# Insert in batches
execute_many(conn, sql, batch_data)
print(f"Inserted {len(batch_data)} orders")
```

---

## 🔐 Error Handling

### Connection Errors

```python
from src.utils.db import get_connection
import pymysql

try:
    conn = get_connection()
    # ... operations ...
except pymysql.Error as e:
    print(f"Database error: {e}")
    # Handle error appropriately
finally:
    if 'conn' in locals():
        conn.close()
```

### Query Errors

```python
from src.utils.db import get_connection, execute_sql

conn = get_connection()

try:
    result = execute_sql(conn, "SELECT * FROM non_existent_table")
except Exception as e:
    print(f"Query failed: {e}")
    # Log error, notify user, etc.
finally:
    conn.close()
```

---

## 📝 Best Practices

1. **Always close connections**: Use `close_connection()` or context managers
2. **Use parameterized queries**: Prevent SQL injection
3. **Batch operations**: Use `execute_many()` for multiple inserts
4. **Handle errors**: Always wrap database operations in try-except blocks
5. **Use SQLAlchemy engine**: For Pandas operations, prefer `get_engine()`

---

## 📚 Related Documentation

- [Data Dictionary](data_dictionary.md) - Database schema
- [ETL Pipeline](etl_pipeline.md) - Data loading workflow
- [Quick Start Guide](quickstart.md) - Getting started

---

## 🔗 References

- [PyMySQL Documentation](https://pymysql.readthedocs.io/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pandas Database IO](https://pandas.pydata.org/docs/user_guide/io.html#sql)
