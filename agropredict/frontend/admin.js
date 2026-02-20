const API_URL = '';

window.onload = () => {
    loadAllData();
};

function showSection(id) {
    ['settings', 'contributors', 'variables', 'models'].forEach(s => {
        const el = document.getElementById(`sec-${s}`);
        if (el) el.style.display = s === id ? 'block' : 'none';
    });
}

async function loadAllData() {
    await loadSettings();
    await loadContributors();
    await loadVariables();
}

async function loadSettings() {
    const res = await fetch(`${API_URL}/api/settings`);
    const data = await res.json();
    document.getElementById('set-platform-name').value = data.platform_name;
    document.getElementById('set-host').value = data.institutional_host;
    document.getElementById('set-dept').value = data.department;
}

async function loadContributors() {
    const res = await fetch(`${API_URL}/api/contributors`);
    const data = await res.json();
    const tbody = document.querySelector('#admin-contributors-table tbody');
    tbody.innerHTML = data.map(c => `
        <tr>
            <td>${c.name}</td>
            <td>${c.role}</td>
            <td>${c.profile_link}</td>
            <td><button class="btn" style="background:#ffcdd2; padding: 4px 8px;" onclick="deleteContributor(${c.id})">Delete</button></td>
        </tr>
    `).join('');
}

async function loadVariables() {
    const res = await fetch(`${API_URL}/api/variables`);
    const data = await res.json();
    const tbody = document.querySelector('#admin-variables-table tbody');
    tbody.innerHTML = data.map(v => `
        <tr>
            <td>${v.name}</td>
            <td>${v.category}</td>
            <td>${v.unit}</td>
            <td>${v.is_visible ? 'Visible' : 'Hidden'}</td>
            <td><button class="btn" style="background:#eee; padding: 4px 8px;" onclick="toggleVariable(${v.id})">Toggle</button></td>
        </tr>
    `).join('');
}

async function saveSettings() {
    const payload = {
        platform_name: document.getElementById('set-platform-name').value,
        institutional_host: document.getElementById('set-host').value,
        department: document.getElementById('set-dept').value
    };
    alert("Settings saved successfully! (Simulated)");
}

function addContributor() {
    const name = prompt("Enter contributor name:");
    const role = prompt("Enter role:");
    if (name && role) {
        alert("Contributor added! (Simulated)");
    }
}
