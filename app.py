from flask import Flask, request, jsonify, render_template
import subprocess
import db_helper

app = Flask(__name__)

# Path to the database file
DB_FILE = "data.db"

# Ensure the database is initialized
db_helper.initialize_database(DB_FILE)


@app.route("/")
def index():
    """Render the main HTML page."""
    return render_template("index.html")


@app.route("/run-script", methods=["POST"])
def run_script():
    """Run a Python script and return its output."""
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
    """Retrieve data from the 'users' table."""
    data = db_helper.get_table_data(DB_FILE, "users")
    return data.to_json(orient="records")


@app.route("/add-user", methods=["POST"])
def add_user():
    """Add a new user to the 'users' table."""
    name = request.json.get("name")
    age = request.json.get("age")
    db_helper.add_row(DB_FILE, "users", {"name": name, "age": age})
    return jsonify({"status": "success", "message": f"User {name} added successfully"})


@app.route("/add-column", methods=["POST"])
def add_column():
    """Add a new column to a table."""
    table_name = request.json.get("table_name")
    column_name = request.json.get("column_name")
    column_type = request.json.get("column_type", "TEXT")
    db_helper.add_column(DB_FILE, table_name, column_name, column_type)
    return jsonify(
        {"status": "success", "message": f"Column {column_name} added to {table_name}"}
    )


@app.route("/remove-user", methods=["POST"])
def remove_user():
    """Remove a user from the 'users' table."""
    condition = request.json.get("condition")  # e.g., 'id = 1'
    db_helper.remove_row(DB_FILE, "users", condition)
    return jsonify(
        {
            "status": "success",
            "message": f'User(s) matching condition "{condition}" removed successfully',
        }
    )


@app.route("/print-table", methods=["GET"])
def print_table():
    """Print the entire 'users' table to the console (for debugging)."""
    db_helper.print_table(DB_FILE, "users")
    return jsonify({"status": "success", "message": "Table printed to console"})


@app.route("/remove-column", methods=["POST"])
def remove_column():
    """Remove a column from a table."""
    table_name = request.json.get("table_name")
    column_name = request.json.get("column_name")
    db_helper.remove_column(DB_FILE, table_name, column_name)
    return jsonify(
        {
            "status": "success",
            "message": f"Column {column_name} removed from {table_name}",
        }
    )


def main():
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
