from flask import Flask, request, jsonify, render_template
import sqlite3
import subprocess
import os

app = Flask(__name__)

DB_FILE = "data.db"


def get_db_connection():
    # Check if the database file exists; if not, initialize it
    if not os.path.exists(DB_FILE):
        initialize_database()
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    # Create the database and tables
    conn = sqlite3.connect(DB_FILE)
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
    print("Database initialized and 'users' table created.")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/run-script", methods=["POST"])
def run_script():
    script_name = request.json.get("script_name")
    try:
        result = subprocess.run(
            ["python", f"scripts/{script_name}"], capture_output=True, text=True
        )
        return jsonify({"output": result.stdout, "error": result.stderr})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/get-data", methods=["GET"])
def get_data():
    conn = get_db_connection()
    data = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return jsonify([dict(row) for row in data])


@app.route("/add-user", methods=["POST"])
def add_user():
    name = request.json.get("name")
    age = request.json.get("age")
    conn = get_db_connection()
    conn.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})


def main():
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
