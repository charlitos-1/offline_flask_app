
# How to Modify the Application

This guide explains how to modify the provided code to implement new features, such as adding new entries, adding new buttons, and deleting entries.

---

## 1. Adding New Entries

### Description
Adding new entries involves extending the form fields to include additional data. For instance, if you want to add a new `field4`, you need to update both the front-end (HTML and JavaScript) and back-end (Flask and database).

### Steps
1. **Modify the Database Schema**
   - **File**: `db_helper.py`
   - **Why**: The database schema needs to support the new field.
   - **Update** the `initialize_database` function:
     ```python
     def initialize_database(db_file, table_name="generic_table"):
         """Initializes the database with a default table."""
         conn = sqlite3.connect(db_file)
         cursor = conn.cursor()
         cursor.execute(f'''
             CREATE TABLE IF NOT EXISTS {table_name} (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 title TEXT NOT NULL,
                 field1 TEXT,
                 field2 TEXT,
                 field3 TEXT,
                 field4 TEXT  -- Add the new field here
             )
         ''')
         conn.commit()
         conn.close()
     ```

2. **Update the Form**
   - **File**: `templates/index.html`
   - **Why**: The front-end form needs to collect the new field data.
   - **Add** a new input field:
     ```html
     <label for="field4">Field4:</label>
     <input type="text" id="field4" name="field4" placeholder="Enter field4 value">
     ```

3. **Update Form Handling**
   - **File**: `static/js/scripts.js`
   - **Why**: The front-end needs to send the new field data to the server.
   - **Update** the form submission logic to include the new field:
     ```javascript
     const field4 = document.getElementById('field4').value;
     const rowData = { title, field1, field2, field3, field4 };
     ```

4. **Update Server Logic**
   - **File**: `app.py`
   - **Why**: The server must process and store the new field data.
   - **Update** the `/add-row` and `/add-rows` endpoints to handle the new field:
     ```python
     @app.route('/add-row', methods=['POST'])
     def add_row():
         table_name = request.json.get('table_name', 'generic_table')
         row_data = request.json.get('row_data', {})
         db_helper.add_row(DB_FILE, table_name, row_data)
         return jsonify({'status': 'success', 'message': f'Row added to {table_name}'})
     ```

---

## 2. Adding New Buttons

### Description
Adding new buttons involves extending the front-end layout (HTML), defining their behavior (JavaScript), and optionally creating new server endpoints (Flask).

### Steps
1. **Add the Button**
   - **File**: `templates/index.html`
   - **Why**: The button must exist in the HTML for users to interact with.
   - **Example**:
     ```html
     <button id="new-button">New Button</button>
     ```

2. **Define Button Behavior**
   - **File**: `static/js/scripts.js`
   - **Why**: The front-end needs to handle button clicks.
   - **Add** an event listener for the new button:
     ```javascript
     document.getElementById('new-button').addEventListener('click', async () => {
         alert('New Button Clicked!');
         // Add any additional functionality here
     });
     ```

3. **Optionally Add Server Logic**
   - **File**: `app.py`
   - **Why**: If the button triggers server-side functionality, you need to create a new endpoint.
   - **Example**:
     ```python
     @app.route('/new-action', methods=['POST'])
     def new_action():
         # Perform the server-side action
         return jsonify({'status': 'success', 'message': 'Action performed successfully'})
     ```

4. **Connect Front-End to Back-End**
   - **Update** the JavaScript to call the new endpoint:
     ```javascript
     const response = await fetch('/new-action', { method: 'POST' });
     const result = await response.json();
     alert(result.message);
     ```

---

## 3. Deleting Entries

### Description
Deleting entries involves updating the front-end to trigger deletions and adding back-end logic to process these requests.

### Steps
1. **Add a Delete Button**
   - **File**: `templates/index.html`
   - **Why**: Users need a button to delete entries.
   - **Example** (inline delete button for each row):
     ```html
     <button class="delete-button" data-id="{{ id }}">Delete</button>
     ```

2. **Handle Delete Requests**
   - **File**: `static/js/scripts.js`
   - **Why**: The front-end needs to send the ID of the row to be deleted to the server.
   - **Add** an event listener for the delete buttons:
     ```javascript
     document.addEventListener('click', async (e) => {
         if (e.target.classList.contains('delete-button')) {
             const id = e.target.dataset.id; // Get the row ID
             const response = await fetch(`/delete-row?id=${id}`, { method: 'DELETE' });
             const result = await response.json();
             alert(result.message);
             fetchData(); // Refresh the displayed data
         }
     });
     ```

3. **Add a Server Endpoint**
   - **File**: `app.py`
   - **Why**: The server needs to handle delete requests.
   - **Add** a new endpoint:
     ```python
     @app.route('/delete-row', methods=['DELETE'])
     def delete_row():
         row_id = request.args.get('id')
         conn = db_helper.get_db_connection(DB_FILE)
         cursor = conn.cursor()
         cursor.execute('DELETE FROM generic_table WHERE id = ?', (row_id,))
         conn.commit()
         conn.close()
         return jsonify({'status': 'success', 'message': 'Row deleted successfully'})
     ```

---

## Summary of Modifications

| Feature            | Files to Modify          | Reason                                                                                 |
|--------------------|--------------------------|----------------------------------------------------------------------------------------|
| Adding New Entries | `db_helper.py`, `app.py`, `index.html`, `scripts.js` | Update database schema, front-end form, and server logic to handle new fields.         |
| Adding New Buttons | `index.html`, `scripts.js`, `app.py` (optional)       | Add button to front-end, define its behavior in JavaScript, and connect to the back-end. |
| Deleting Entries   | `index.html`, `scripts.js`, `app.py`, `db_helper.py` | Enable delete actions in the front-end and add server logic to process deletions.      |

---