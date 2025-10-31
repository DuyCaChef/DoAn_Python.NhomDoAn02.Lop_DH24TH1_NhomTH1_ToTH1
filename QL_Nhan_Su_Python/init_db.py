"""Compatibility entry point to initialize the database."""

# Try to reuse existing db_init
try:
    from app.database import db_init as project_db_init
except Exception:
    project_db_init = None


def init_db():
    if project_db_init and hasattr(project_db_init, "init_db"):
        return project_db_init.init_db()
    # Minimal fallback: create sqlite DB file
    import sqlite3
    conn = sqlite3.connect("hrm.sqlite3")
    conn.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT
    )
    """)
    conn.commit()
    conn.close()
    print("Initialized fallback sqlite database 'hrm.sqlite3'")


if __name__ == "__main__":
    init_db()
