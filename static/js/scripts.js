document.addEventListener('DOMContentLoaded', () => {
    /**
     * Fetch all data from the database and display it in the output section.
     */
    async function fetchData() {
        try {
            const response = await fetch(`/get-data?table_name=generic_table`);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const data = await response.json();
            document.getElementById('output').innerText = JSON.stringify(data, null, 2);
        } catch (error) {
            console.error("Error fetching data:", error);
            alert("Failed to load data. Please check the server or database.");
        }
    }

    /**
     * Handle the submission of the "Add Row" form.
     * Collects user input, sends it to the server, and refreshes the displayed data.
     */
    document.getElementById('add-row-form').addEventListener('submit', async (e) => {
        e.preventDefault(); // Prevent default form submission

        // Collect form input values
        const title = document.getElementById('title').value;
        const field1 = document.getElementById('field1').value;
        const field2 = document.getElementById('field2').value;
        const field3 = document.getElementById('field3').value;

        const rowData = { title, field1, field2, field3 };

        try {
            const response = await fetch('/add-row', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ table_name: 'generic_table', row_data: rowData }),
            });

            if (!response.ok) throw new Error(`Failed to add row: ${response.statusText}`);

            const result = await response.json();
            alert(result.message); // Notify the user

            fetchData(); // Refresh data display

            e.target.reset(); // Clear the form inputs
        } catch (error) {
            console.error("Error adding row:", error);
            alert("Failed to add the row. Please try again.");
        }
    });

    /**
     * Handle drag-and-drop or click-to-upload JSON files for bulk data upload.
     */
    const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('file-input');
    const preview = document.getElementById('json-preview');
    const parsedDataElement = document.getElementById('parsed-data');
    const confirmButton = document.getElementById('confirm-json-button');
    const cancelButton = document.getElementById('cancel-json-button');
    let parsedJsonData = [];

    /**
     * Trigger the file input when the drop area is clicked.
     */
    dropArea.addEventListener('click', () => {
        fileInput.value = ""; // Reset file input to allow re-uploading the same file
        fileInput.click();
    });

    /**
     * Handle file selection from the file input.
     */
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) handleFile(file);
    });

    /**
     * Drag-and-drop functionality.
     */
    dropArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropArea.classList.add('dragging');
    });

    dropArea.addEventListener('dragleave', () => dropArea.classList.remove('dragging'));

    dropArea.addEventListener('drop', (e) => {
        e.preventDefault();
        dropArea.classList.remove('dragging');
        const file = e.dataTransfer.files[0];
        if (file) handleFile(file);
    });

    /**
     * Process the uploaded JSON file and display its preview.
     * @param {File} file - The uploaded file object.
     */
    function handleFile(file) {
        if (file && file.type === 'application/json') {
            const reader = new FileReader();
            reader.onload = (e) => {
                try {
                    parsedJsonData = JSON.parse(e.target.result); // Parse the JSON data
                    parsedDataElement.innerText = JSON.stringify(parsedJsonData, null, 2);
                    preview.style.display = 'block'; // Show the preview section
                } catch (err) {
                    alert('Invalid JSON file.');
                }
            };
            reader.readAsText(file);
        } else {
            alert('Please upload a valid JSON file.');
        }
    }

    /**
     * Confirm and upload the parsed JSON data to the database.
     */
    confirmButton.addEventListener('click', async () => {
        if (parsedJsonData.length === 0) {
            alert('No data to add.');
            return;
        }

        try {
            const response = await fetch('/add-rows', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ table_name: 'generic_table', rows: parsedJsonData }),
            });

            if (!response.ok) throw new Error(`Failed to add rows: ${response.statusText}`);

            const result = await response.json();
            alert(result.message); // Notify the user

            preview.style.display = 'none'; // Hide the preview section
            fetchData(); // Refresh data display
        } catch (error) {
            console.error("Error adding rows:", error);
            alert("Failed to add rows. Please try again.");
        }
    });

    /**
     * Cancel the JSON upload process and clear the preview.
     */
    cancelButton.addEventListener('click', () => {
        parsedJsonData = []; // Clear parsed data
        preview.style.display = 'none'; // Hide the preview section
    });

    /**
     * Refresh data manually when the "Refresh Data" button is clicked.
     */
    const refreshButton = document.getElementById('refresh-data-button');
    if (refreshButton) {
        refreshButton.addEventListener('click', fetchData);
    } else {
        console.error("Refresh Data button not found in the DOM.");
    }

    // Fetch initial data when the page loads
    fetchData();
});
