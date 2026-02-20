const API_URL = '';

window.onload = () => {
    initPopup();
    fetchContributors();
    fetchVariables();
    initChart();
    initScrollReveal();
};

// --- Animations Logic ---
function initScrollReveal() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: "0px 0px -50px 0px"
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.reveal').forEach(el => {
        observer.observe(el);
    });
}

// --- Startup Pop-up Logic ---
function initPopup() {
    const popup = document.getElementById('startup-popup');
    setTimeout(() => {
        popup.style.opacity = '1';
    }, 250);

    // Auto-dismiss after 5 seconds if not interacted
    const autoDismiss = setTimeout(() => {
        dismissPopup();
    }, 5000);

    // Clear auto-dismiss on button click
    window.dismissPopup = () => {
        clearTimeout(autoDismiss);
        popup.style.opacity = '0';
        setTimeout(() => {
            popup.style.display = 'none';
        }, 300);
    };
}

// --- Data Fetching ---
async function fetchContributors() {
    try {
        const response = await fetch(`${API_URL}/api/contributors`);
        const contributors = await response.json();
        const tbody = document.querySelector('#contributors-list tbody');
        tbody.innerHTML = contributors.map(c => `
            <tr>
                <td>${c.name}</td>
                <td><span class="role-tag">${c.role}</span></td>
                <td><a href="${c.profile_link || '#'}" target="_blank" style="color: var(--primary-green); text-decoration: none;">${c.profile_link ? 'Link' : '—'}</a></td>
            </tr>
        `).join('');
    } catch (e) {
        console.error("Failed to fetch contributors", e);
    }
}

async function fetchVariables() {
    try {
        const response = await fetch(`${API_URL}/api/variables`);
        const variables = await response.json();
        const container = document.getElementById('input-fields-container');

        // Group by category
        const groups = variables.reduce((acc, v) => {
            if (!acc[v.category]) acc[v.category] = [];
            acc[v.category].push(v);
            return acc;
        }, {});

        container.innerHTML = Object.entries(groups).map(([cat, vars]) => `
            <div class="input-category">
                <h4 style="font-size: 0.9rem; color: var(--earth-brown); margin: 1rem 0 0.5rem;">${cat}</h4>
                ${vars.map(v => `
                    <div class="input-group">
                        <label>${v.name} (${v.unit})</label>
                        <input type="number" id="var-${v.id}" step="0.1" placeholder="Enter ${v.name.toLowerCase()}">
                    </div>
                `).join('')}
            </div>
        `).join('');
    } catch (e) {
        console.error("Failed to fetch variables", e);
    }
}

// --- Prediction Logic ---
async function runPrediction() {
    const resultsDiv = document.getElementById('prediction-results');
    resultsDiv.style.display = 'block';

    // In a real app, we'd collect inputs here
    try {
        const response = await fetch(`${API_URL}/api/predict`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ algorithm: document.getElementById('algorithm-select').value })
        });
        const result = await response.json();

        document.getElementById('res-height').innerText = `${result.predicted_height} cm`;
        document.getElementById('res-yield').innerText = `${result.yield_estimate} kg/m²`;
        document.getElementById('res-r2').innerText = result.metrics.r2;

        updateChartData(result);
    } catch (e) {
        console.error("Prediction failed", e);
    }
}

// --- Charting ---
let mainChart;
function initChart() {
    const ctx = document.getElementById('predictionChart').getContext('2d');
    mainChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Day 0', 'Day 5', 'Day 10', 'Day 15', 'Day 20'],
            datasets: [{
                label: 'Observed Growth (cm)',
                data: [5, 8, 12, 18, 25],
                borderColor: '#2d5a27',
                backgroundColor: 'rgba(45, 90, 39, 0.1)',
                tension: 0.3,
                fill: true
            }, {
                label: 'Predicted Growth (cm)',
                data: [5, 8, 12, 17.5, 24.2],
                borderColor: '#8bc34a',
                borderDash: [5, 5],
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'top' },
                title: { display: true, text: 'Plant Growth Trajectory Analysis' }
            },
            scales: {
                y: { beginAtZero: true, title: { display: true, text: 'Height (cm)' } },
                x: { title: { display: true, text: 'Time (Days)' } }
            }
        }
    });
}

function updateChart(type) {
    if (!mainChart) return;
    // Simplified toggle for demo
    if (type === 'bar') {
        mainChart.config.type = 'bar';
        mainChart.data.datasets[0].label = 'Feature Importance';
        mainChart.data.datasets[1].hidden = true;
    } else {
        mainChart.config.type = 'line';
        mainChart.data.datasets[0].label = 'Observed Growth';
        mainChart.data.datasets[1].hidden = false;
    }
    mainChart.update();
}

// --- Report Generation ---
function generateReport() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    doc.setFontSize(22);
    doc.setTextColor(45, 90, 39);
    doc.text("AgroPredict Scientific Report", 20, 30);

    doc.setFontSize(12);
    doc.setTextColor(0);
    doc.text("Institutional Host: University of Layyah", 20, 45);
    doc.text("Faculty: Faculty of Agricultural Sciences and Technology", 20, 52);

    doc.line(20, 60, 190, 60);

    doc.text("Prediction Results Summary:", 20, 75);
    doc.text("- Model: Random Forest", 30, 85);
    doc.text(`- Predicted Height: ${document.getElementById('res-height').innerText}`, 30, 95);
    doc.text(`- Predicted Yield: ${document.getElementById('res-yield').innerText}`, 30, 105);
    doc.text(`- Model R-squared: ${document.getElementById('res-r2').innerText}`, 30, 115);

    doc.save("AgroPredict_Scientific_Report.pdf");
}

function exportData(format) {
    alert(`Exporting dataset in ${format.toUpperCase()} format...`);
}
