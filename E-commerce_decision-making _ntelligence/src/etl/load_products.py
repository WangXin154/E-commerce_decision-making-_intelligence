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

def load_products_raw(csv_path, batch_size=1000):
    df = pd.read_csv(csv_path)

    column_order = [
    "product_id",
    "product_category_name",
    "product_name_lenght",
    "product_description_lenght",
    "product_photos_qty",
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm"
]

    sql = """
    INSERT  IGNORE INTO products_raw (
        product_id,
        product_category_name,
        product_name_lenght,
        product_description_lenght,
        product_photos_qty,
        product_weight_g,
        product_length_cm,
        product_height_cm,
        product_width_cm
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
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