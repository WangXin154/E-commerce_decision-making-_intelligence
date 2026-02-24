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

def load_order_items_raw(csv_path, batch_size=1000):
    df = pd.read_csv(csv_path)

    column_order = [
    "order_id",
    "order_item_id",
    "product_id",
    "seller_id",
    "shipping_limit_date",
    "price",
    "freight_value"
]

    sql = """
    INSERT  IGNORE INTO order_items_raw (
        order_id,
        order_item_id,
        product_id,
        seller_id,
        shipping_limit_date,
        price,
        freight_value
    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
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