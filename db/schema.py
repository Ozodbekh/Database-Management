from .connection import get_connection


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        phone_number TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE,
        password TEXT,
        role TEXT CHECK(role IN ('admin', 'teacher', 'student')) NOT NULL
    )
    """)
    print("Created user schema.")

    conn.commit()
    conn.commit()