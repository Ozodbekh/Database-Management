from pathlib import Path


def get_connection_sqlite3():
    from sqlite3 import connect
    path = Path(__file__).resolve().parent.parent
    db_path = path / "mydb.db"
    return connect(database=db_path)


def get_connection_postgres():
    from psycopg2 import connect
    return connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="1",
        port=5432
    )
