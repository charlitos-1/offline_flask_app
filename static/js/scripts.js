// Function to fetch all data
async function fetchData() {
    const response = await fetch(`/get-data?table_name=generic_table`);
    const data = await response.json();
    document.getElementById('output').innerText = JSON.stringify(data, null, 2);
}

// Function to handle form submission for adding a row
document.getElementById('add-row-form').addEventListener('submit', async (e) => {
    e.preventDefault(); // Prevent the form from reloading the page

    // Gather form data
    const title = document.getElementById('title').value;
    const field1 = document.getElementById('field1').value;
    const field2 = document.getElementById('field2').value;
    const field3 = document.getElementById('field3').value;

    // Prepare the payload
    const rowData = {
        title: title,
        field1: field1 || null,
        field2: field2 || null,
        field3: field3 || null,
    };

    // Send the data to the server
    const response = await fetch('/add-row', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ table_name: 'generic_table', row_data: rowData }),
    });

    // Handle the server response
    const result = await response.json();
    alert(result.message);

    // Optionally, fetch and display updated data
    fetchData();
});

// Automatically fetch data on page load
window.onload = async () => {
    await fetchData();
};
