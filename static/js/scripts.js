async function runScript() {
    const response = await fetch('/run-script', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ script_name: 'example_script.py' })
    });
    const result = await response.json();
    document.getElementById('output').innerText = result.output || result.error;
}

async function fetchData() {
    const response = await fetch('/get-data');
    const data = await response.json();
    document.getElementById('output').innerText = JSON.stringify(data, null, 2);
}

document.getElementById('add-user-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const response = await fetch('/add-user', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            name: formData.get('name'),
            age: formData.get('age')
        })
    });
    const result = await response.json();
    alert('User added successfully!');
});

