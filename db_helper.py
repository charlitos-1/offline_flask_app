import sqlite3
import pandas as pd
import os


def get_db_connection(db_file):
    """Returns a connection to the SQLite database."""
    if not os.path.exists(db_file):
        initialize_database(db_file)
    return sqlite3.connect(db_file)


def initialize_database(db_file):
    """Initializes the database with a default 'users' table."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()
    print(f"Database '{db_file}' initialized and 'users' table created.")


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


def remove_row(db_file, table_name, condition):
    """Removes rows from a table based on a condition (e.g., 'id = 1')."""
    conn = get_db_connection(db_file)
    cursor = conn.cursor()
    query = f"DELETE FROM {table_name} WHERE {condition}"
    cursor.execute(query)
    conn.commit()
    conn.close()


def add_column(db_file, table_name, column_name, column_type="TEXT"):
    """Adds a new column to a table."""
    conn = get_db_connection(db_file)
    cursor = conn.cursor()
    query = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"
    cursor.execute(query)
    conn.commit()
    conn.close()


def remove_column(db_file, table_name, column_name):
    """Removes a column from a table (requires creating a new table)."""
    conn = get_db_connection(db_file)
    cursor = conn.cursor()

    # Fetch current columns
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [col[1] for col in cursor.fetchall() if col[1] != column_name]

    # Create a new table without the column
    columns_str = ", ".join(columns)
    cursor.execute(
        f"CREATE TABLE {table_name}_temp AS SELECT {columns_str} FROM {table_name}"
    )
    cursor.execute(f"DROP TABLE {table_name}")
    cursor.execute(f"ALTER TABLE {table_name}_temp RENAME TO {table_name}")

    conn.commit()
    conn.close()


def print_table(db_file, table_name):
    """Prints the content of a table."""
    conn = get_db_connection(db_file)
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    conn.close()
    print(df)


def get_table_data(db_file, table_name):
    """Returns the content of a table as a pandas DataFrame."""
    conn = get_db_connection(db_file)
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df
