from flask import Flask, request, jsonify, render_template
import subprocess
import db_helper
import pandas as pd

app = Flask(__name__)

# Path to the database file
DB_FILE = "data.db"


def main():
    """Main entry point of the application."""
    # Ensure the database is initialized with a generic table
    db_helper.initialize_database(DB_FILE, table_name="generic_table")
    app.run(host="0.0.0.0", port=5000)


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
    """Retrieve all data from a table."""
    table_name = request.args.get("table_name", "generic_table")

    conn = db_helper.get_db_connection(DB_FILE)
    query = f"SELECT * FROM {table_name}"
    data = pd.read_sql_query(query, conn)
    conn.close()
    return data.to_json(orient="records")


@app.route("/add-row", methods=["POST"])
def add_row():
    """Add a new row to a specified table."""
    table_name = request.json.get("table_name", "generic_table")
    row_data = request.json.get(
        "row_data", {}
    )  # Example: {"title": "Task 1", "field1": "Value1"}
    db_helper.add_row(DB_FILE, table_name, row_data)
    return jsonify({"status": "success", "message": f"Row added to {table_name}"})


if __name__ == "__main__":
    main()
