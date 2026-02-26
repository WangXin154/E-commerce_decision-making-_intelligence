from src.utils.db import get_connection, execute_many, close_connection
import pandas as pd

def safe_value(v):
    if pd.isna(v):
        return None
    return v

def row_to_params(row, columns):
    return tuple(
        safe_value(row[col])
        for col in columns
    )

def load_customers_raw(csv_path, batch_size=1000):
    df = pd.read_csv(csv_path)

    column_order = [
    "customer_id",
    "customer_unique_id",
    "customer_zip_code_prefix",
    "customer_city",
    "customer_state"
]

    sql = """
    INSERT  IGNORE INTO customers_raw (
        customer_id,
        customer_unique_id,
        customer_zip_code_prefix,
        customer_city,
        customer_state
    ) VALUES (%s, %s, %s, %s, %s)
    """

    conn = get_connection()
    try:
        for start in range(0, len(df), batch_size):
            end = start + batch_size
            chunk = df.iloc[start:end]

            batch = [
                row_to_params(row, column_order)
                for _, row in chunk.iterrows()
            ]

            if batch:
                affected = execute_many(conn, sql, batch)
                print(f"Inserted {affected} rows")

    finally:
        close_connection(conn)