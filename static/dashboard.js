async function executeScript() {
    const system = document.getElementById('system').value;
    const scriptPath = document.getElementById('script_path').value;
    const outputDiv = document.getElementById('output');

    if (!scriptPath) {
        alert('Please provide a script path');
        return;
    }

    try {
        const response = await fetch('/execute', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ system, script_path: scriptPath })
        });

        const data = await response.json();
        if (data.success) {
            outputDiv.innerHTML = `
                <h3>Output:</h3>
                <pre>${data.output || 'No output'}</pre>
                ${data.error ? `<h3>Error:</h3><pre>${data.error}</pre>` : ''}
            `;
        } else {
            alert(data.message || 'Script execution failed');
        }
    } catch (error) {
        alert('An error occurred during script execution');
    }
}