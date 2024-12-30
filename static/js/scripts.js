document.addEventListener('DOMContentLoaded', () => {
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

    document.getElementById('add-row-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const form = e.target;
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
            alert(result.message);
            fetchData();
            form.reset();
        } catch (error) {
            console.error("Error adding row:", error);
            alert("Failed to add the row. Please try again.");
        }
    });

    const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('file-input');
    const preview = document.getElementById('json-preview');
    const parsedDataElement = document.getElementById('parsed-data');
    const confirmButton = document.getElementById('confirm-json-button');
    const cancelButton = document.getElementById('cancel-json-button');
    let parsedJsonData = [];

    dropArea.addEventListener('click', () => {
        fileInput.value = "";
        fileInput.click();
    });

    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) handleFile(file);
    });

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

    function handleFile(file) {
        if (file.type === 'application/json') {
            const reader = new FileReader();
            reader.onload = (e) => {
                try {
                    parsedJsonData = JSON.parse(e.target.result);
                    parsedDataElement.innerText = JSON.stringify(parsedJsonData, null, 2);
                    preview.style.display = 'block';
                } catch (err) {
                    alert("Invalid JSON file.");
                }
            };
            reader.readAsText(file);
        } else {
            alert("Please upload a valid JSON file.");
        }
    }

    confirmButton.addEventListener('click', async () => {
        if (parsedJsonData.length === 0) {
            alert("No data to add.");
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
            alert(result.message);
            preview.style.display = 'none';
            fetchData();
        } catch (error) {
            console.error("Error adding rows:", error);
            alert("Failed to add rows. Please try again.");
        }
    });

    cancelButton.addEventListener('click', () => {
        parsedJsonData = [];
        preview.style.display = 'none';
    });

    const refreshButton = document.getElementById('refresh-data-button');
    if (refreshButton) refreshButton.addEventListener('click', fetchData);

    fetchData();
});
