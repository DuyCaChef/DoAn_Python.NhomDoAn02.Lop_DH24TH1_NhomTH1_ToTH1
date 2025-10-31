"""MySQL database connection for HRM project."""
try:
    import mysql.connector
except ImportError:
    raise ImportError("mysql-connector-python is required. Install with: pip install mysql-connector-python")

from . import db_config


def get_connection():
    """Return a MySQL database connection using credentials from .env file."""
    try:
        conn = mysql.connector.connect(
            host=db_config.DB_HOST,
            user=db_config.DB_USER,
            password=db_config.DB_PASSWORD,
            database=db_config.DB_NAME,
            autocommit=False,
        )
        return conn
    except mysql.connector.Error as e:
        raise ConnectionError(f"Failed to connect to MySQL database: {e}")


def test_connection():
    """Test database connection and return server version."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT VERSION()")
        version = cur.fetchone()[0]
        cur.execute("SELECT 1")
        cur.fetchone()
        return version
    finally:
        conn.close()


if __name__ == "__main__":
    # Quick connection test
    try:
        version = test_connection()
        print(f"✓ MySQL connection successful. Server version: {version}")
    except Exception as e:
        print(f"✗ MySQL connection failed: {e}")
