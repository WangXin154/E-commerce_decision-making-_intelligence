# The basic tool layer responsible for "database connection + SQL execution"
# sql script
# Feature engineering script
# Data extraction before model training
# API layer query data

# Data Layer
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user":"root",
    "password": "Xrwyx13795",
    "database": "ecommerce_platform",
    "charset": "utf8mb4"
}

import pymysql
from sqlalchemy import create_engine

def get_connection():
    try:
        conn = pymysql.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"],
            charset=DB_CONFIG["charset"],
            autocommit=False
        )
        return conn
    except Exception as e:
        print("Database connection failed", e)
        raise

def get_engine():
    """
    Returns a SQLAlchemy Engine for pandas.read_sql
    """
    user = 'root'
    password = 'Xrwyx13795'
    host = 'localhost'
    port = 3306
    db = 'ecommerce_platform'
    url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset=utf8mb4"
    engine = create_engine(url)
    return engine

def execute_sql(conn, sql, params=None):
    cursor = conn.cursor()
    try:
        if params:
            result = cursor.execute(sql, params)
        else:
            result = cursor.execute(sql)

        conn.commit()
        return result
    except Exception as e:
        conn.rollback()
        print("SQL execution failed", e)
        raise
    finally:
        cursor.close()

def execute_many(conn, sql, params_list):
    cursor = conn.cursor()
    try:
        result = cursor.executemany(sql, params_list)
        conn.commit()
        return result
    except Exception as e:
        conn.rollback()
        print("Batch SQL execution failed:", e)
        raise
    finally:
        cursor.close()


def close_connection(conn):
    if conn:
        conn.close()