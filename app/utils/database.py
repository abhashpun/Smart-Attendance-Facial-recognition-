import psycopg2
from contextlib import contextmanager
from app.config import DB_HOST, DB_NAME, DB_USER, DB_PASS

@contextmanager
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    try:
        yield conn
    finally:
        conn.close()
