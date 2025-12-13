import psycopg2
from psycopg2.extensions import connection
from dotenv import load_dotenv
import os


load_dotenv()  # тянет .env из корня


def get_connection() -> connection:
    """Создаёт подключение к PostgreSQL с параметрами из .env"""

    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432")
    )
    return conn
