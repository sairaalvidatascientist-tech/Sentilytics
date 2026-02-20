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

// --- 3. Real-Time WebSocket Connection ---
let websocket = null;
let totalPosts = 0;

function startLiveSimulation() {
    connectWebSocket();
}

function connectWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws`;

    websocket = new WebSocket(wsUrl);

    websocket.onopen = () => {
        console.log('✅ Connected to Sentilytics real-time stream');
    };

    websocket.onmessage = (event) => {
        const data = JSON.parse(event.data);

        if (data.type === 'connection') {
            console.log('📡', data.message);
        } else if (data.type === 'sentiment_update') {
            handleSentimentUpdate(data);
        } else if (data.type === 'crisis_alert') {
            triggerCrisis(data.message);
        }
    };

    websocket.onerror = (error) => {
        console.error('WebSocket error:', error);
    };

    websocket.onclose = () => {
        console.log('❌ Disconnected from stream. Reconnecting in 3s...');
        setTimeout(connectWebSocket, 3000);
    };
}

function handleSentimentUpdate(data) {
    const { post, analysis, stats } = data;

    // Update total posts
    totalPosts = stats.total_posts;
    document.getElementById('kpi-volume').innerText = totalPosts.toLocaleString();

    // Update sentiment percentages
    const distribution = stats.sentiment_distribution;
    document.getElementById('kpi-positive').innerText = distribution.positive + '%';
    document.getElementById('kpi-negative').innerText = distribution.negative + '%';

    // Update emotion chart
    updateEmotionChart(stats.emotion_distribution);

    // Update trend chart with new data
    updateTrendChartWithData(analysis.scores.compound);

    // Log activity (optional visual feedback)
    console.log(`📊 ${post.username}: ${analysis.sentiment} (${analysis.emotion})`);
}

function updateEmotionChart(emotionData) {
    if (!emotionChart) return;

    const emotions = ['joy', 'anger', 'sadness', 'fear', 'neutral'];
    const data = emotions.map(e => emotionData[e] || 0);

    emotionChart.data.datasets[0].data = data;
    emotionChart.update('none');
}

function updateTrendChartWithData(compoundScore) {
    if (!trendChart) return;

    const data = trendChart.data.datasets[0].data;
    const labels = trendChart.data.labels;

    // Remove first
    data.shift();
    labels.shift();

    // Add new (convert compound score -1 to 1 into 0-100 range)
    const newValue = Math.round((compoundScore + 1) * 50);
    data.push(newValue);

    // Time label
    const now = new Date();
    const timeStr = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}`;
    labels.push(timeStr);

    trendChart.update('none');
}

function triggerCrisis(message) {
    const banner = document.getElementById('crisis-banner');
    if (banner.classList.contains('hidden')) {
        // Update message if provided
        if (message) {
            const messageSpan = banner.querySelector('.crisis-content span');
            if (messageSpan) {
                messageSpan.innerHTML = `<strong>CRITICAL ALERT:</strong> ${message}`;
            }
        }

        banner.classList.remove('hidden');

        // Auto hide after 8s
        setTimeout(() => {
            banner.classList.add('hidden');
        }, 8000);
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
