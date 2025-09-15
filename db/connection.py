from sqlite3 import connect

db_name = "db_management.db"


def get_connection():
    return connect(database=db_name)