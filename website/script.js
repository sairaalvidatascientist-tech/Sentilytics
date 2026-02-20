// Sentilytics Core Logic
document.addEventListener('DOMContentLoaded', () => {
    initPopup();
    initTheme();
    initCharts();
    startLiveSimulation();
});

// --- 1. Startup Popup & Transitions ---
function initPopup() {
    const enterBtn = document.getElementById('enter-btn');
    const popup = document.getElementById('startup-popup');
    const app = document.getElementById('app-container');

    enterBtn.addEventListener('click', () => {
        // 1. Button Feedback
        enterBtn.innerHTML = '<i data-lucide="loader"></i> Initializing...';
        lucide.createIcons();

        // 2. Delay for effect
        setTimeout(() => {
            // Fade out popup
            popup.classList.add('popup-hidden');

            // 3. Prepare Dashboard (Display: Block but Opacity: 0)
            app.classList.remove('dashboard-hidden');
            app.classList.add('dashboard-visible');

            // 4. Trigger Fade In (Allow slight reflow)
            setTimeout(() => {
                app.classList.add('fade-in-active');
            }, 50);

        }, 800);
    });
}

// --- 2. Charts Initialization ---
let trendChart, emotionChart, competitorChart;

function initCharts() {
    initTrendChart();
    initEmotionChart();
    initCompetitorChart();
}

function initTrendChart() {
    const ctx = document.getElementById('trendChart').getContext('2d');

    // Gradient fill
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(14, 165, 233, 0.5)'); // Sky 500
    gradient.addColorStop(1, 'rgba(14, 165, 233, 0)');

    trendChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Array.from({ length: 20 }, (_, i) => `${10 + i}:00`),
            datasets: [{
                label: 'Positive Sentiment Volume',
                data: Array.from({ length: 20 }, () => Math.floor(Math.random() * 50) + 50),
                borderColor: '#0ea5e9',
                backgroundColor: gradient,
                borderWidth: 3,
                tension: 0.4,
                fill: true,
                pointRadius: 0,
                pointHoverRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'rgba(15, 23, 42, 0.9)',
                    titleColor: '#f8fafc',
                    bodyColor: '#94a3b8',
                    borderColor: 'rgba(56, 189, 248, 0.2)',
                    borderWidth: 1
                }
            },
            scales: {
                x: {
                    grid: { color: 'rgba(255,255,255,0.05)' },
                    ticks: { color: '#94a3b8' }
                },
                y: {
                    display: false
                }
            },
            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
            }
        }
    });
}

function initEmotionChart() {
    const ctx = document.getElementById('emotionChart').getContext('2d');

    emotionChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Joy', 'Anger', 'Sadness', 'Fear', 'Neutral'],
            datasets: [{
                data: [45, 15, 10, 5, 25],
                backgroundColor: [
                    '#10b981', // Joy (Emerald)
                    '#ef4444', // Anger (Red)
                    '#6366f1', // Sadness (Indigo)
                    '#f59e0b', // Fear (Amber)
                    '#94a3b8'  // Neutral (Slate)
                ],
                borderWidth: 0,
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: { color: '#94a3b8', font: { family: 'Outfit' } }
                }
            },
            cutout: '70%'
        }
    });
}

function initCompetitorChart() {
    const ctx = document.getElementById('competitorChart').getContext('2d');

    competitorChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Nike', 'Adidas', 'Puma'],
            datasets: [{
                label: 'Sentiment Score',
                data: [85, 72, 64],
                backgroundColor: [
                    '#0ea5e9', // Sky
                    '#8b5cf6', // Violet
                    '#f43f5e'  // Rose
                ],
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(255,255,255,0.05)' },
                    ticks: { color: '#94a3b8' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#94a3b8' }
                }
            }
        }
    });
}

// --- 3. Real-Time Simulation ---
function startLiveSimulation() {
    // Update Volume & Sentiment numbers
    setInterval(() => {
        // Update Volume
        const volEl = document.getElementById('kpi-volume');
        let vol = parseInt(volEl.innerText.replace(/,/g, ''));
        vol += Math.floor(Math.random() * 15); // Add random small amount
        volEl.innerText = vol.toLocaleString();

        // Fluctuate Sentiment
        updateSentiment();

        // Update Chart
        updateTrendChart();

    }, 2000); // Every 2 seconds

    // Random Crisis Simulation (Low prob)
    setInterval(() => {
        if (Math.random() > 0.95) { // 5% chance every check
            triggerCrisis();
        }
    }, 10000);
}

function updateSentiment() {
    const posEl = document.getElementById('kpi-positive');
    const negEl = document.getElementById('kpi-negative');

    // Random fluctuation +/- 1%
    let currentPos = parseInt(posEl.innerText);
    let change = (Math.random() > 0.5 ? 1 : -1);

    let newPos = Math.min(99, Math.max(10, currentPos + change));
    let newNeg = Math.round(Math.random() * (100 - newPos - 5)); // Remaining mostly

    posEl.innerText = newPos + '%';
    negEl.innerText = newNeg + '%';
}

function updateTrendChart() {
    const data = trendChart.data.datasets[0].data;
    const labels = trendChart.data.labels;

    // Remove first
    data.shift();
    labels.shift();

    // Add new
    const newValue = Math.floor(Math.random() * 50) + 50;
    data.push(newValue);

    // Time label
    const now = new Date();
    labels.push(`${now.getHours()}:${now.getMinutes()}:${now.getSeconds()}`);

    trendChart.update('none'); // 'none' for smooth animation if enabled, or minimal re-render
}

function triggerCrisis() {
    const banner = document.getElementById('crisis-banner');
    if (banner.classList.contains('hidden')) {
        banner.classList.remove('hidden');

        // Auto hide after 5s
        setTimeout(() => {
            banner.classList.add('hidden');
        }, 5000);
    }
}

// Close banner manually
document.addEventListener('click', (e) => {
    if (e.target.closest('.close-banner')) {
        document.getElementById('crisis-banner').classList.add('hidden');
    }
});


// --- 4. Theme Logic (Simplified for brevity) ---
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    if (savedTheme === 'light') document.body.classList.add('light-mode');

    document.getElementById('theme-toggle').addEventListener('click', () => {
        document.body.classList.toggle('light-mode');
        const isLight = document.body.classList.contains('light-mode');
        localStorage.setItem('theme', isLight ? 'light' : 'dark');

        // Update Icon
        const icon = document.querySelector('#theme-toggle i');
        if (isLight) {
            icon.setAttribute('data-lucide', 'sun');
        } else {
            icon.setAttribute('data-lucide', 'moon');
        }
        lucide.createIcons();
    });
}
