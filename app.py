from flask import Flask, request, jsonify, render_template
import subprocess
import db_helper
import pandas as pd

app = Flask(__name__)

# Path to the database file
DB_FILE = "data.db"


def main():
    """Main entry point of the application."""
    # Initialize the database with the default table if not already present
    db_helper.initialize_database(DB_FILE, table_name="generic_table")
    app.run(host="0.0.0.0", port=5000)


@app.route("/")
def index():
    """Render the main HTML page."""
    return render_template("index.html")


@app.route("/run-script", methods=["POST"])
def run_script():
    """Run a Python script from the 'scripts' directory and return its output."""
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
    """Retrieve all data from the specified table in the database."""
    table_name = request.args.get("table_name", "generic_table")
    conn = db_helper.get_db_connection(DB_FILE)
    query = f"SELECT * FROM {table_name}"
    data = pd.read_sql_query(query, conn)
    conn.close()
    return data.to_json(orient="records")


@app.route("/add-row", methods=["POST"])
def add_row():
    """Add a single row to the specified table in the database."""
    table_name = request.json.get("table_name", "generic_table")
    row_data = request.json.get("row_data", {})
    db_helper.add_row(DB_FILE, table_name, row_data)
    return jsonify({"status": "success", "message": f"Row added to {table_name}"})


@app.route("/add-rows", methods=["POST"])
def add_rows():
    """Add multiple rows to the specified table in the database."""
    table_name = request.json.get("table_name", "generic_table")
    rows = request.json.get("rows", [])
    for row in rows:
        db_helper.add_row(DB_FILE, table_name, row)
    return jsonify(
        {"status": "success", "message": f"{len(rows)} rows added to {table_name}"}
    )


if __name__ == "__main__":
    main()
