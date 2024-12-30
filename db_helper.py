import sqlite3
import pandas as pd
import os


def get_db_connection(db_file):
    """Returns a connection to the SQLite database."""
    if not os.path.exists(db_file):
        initialize_database(db_file, table_name="generic_table")
    return sqlite3.connect(db_file)


def initialize_database(db_file, table_name="generic_table"):
    """Initializes the database with a generic table."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            field1 TEXT,
            field2 TEXT,
            field3 TEXT
        )
    """
    )
    conn.commit()
    conn.close()
    print(f"Database '{db_file}' initialized with table '{table_name}'.")


def add_row(db_file, table_name, row_data):
    """Adds a new row to a specified table."""
    conn = get_db_connection(db_file)
    cursor = conn.cursor()
    columns = ", ".join(row_data.keys())
    placeholders = ", ".join(["?"] * len(row_data))
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    cursor.execute(query, tuple(row_data.values()))
    conn.commit()
    conn.close()
