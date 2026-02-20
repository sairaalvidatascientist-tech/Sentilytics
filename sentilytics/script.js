// ===== Global Variables =====
let sentimentPieChart = null;
let sentimentLineChart = null;
let keywordBarChart = null;
let websocket = null;
let currentKeyword = '';
let activityLogCount = 0;

// ===== Startup Popup Logic =====
document.addEventListener('DOMContentLoaded', () => {
    const popup = document.getElementById('startupPopup');
    const closeBtn = document.getElementById('closePopup');
    const mainApp = document.getElementById('mainApp');

    closeBtn.addEventListener('click', () => {
        popup.style.animation = 'fadeOut 0.5s ease-in-out';
        setTimeout(() => {
            popup.style.display = 'none';
            mainApp.classList.remove('hidden');
            mainApp.style.animation = 'fadeIn 0.5s ease-in-out';
            initializeDashboard();
        }, 500);
    });

    // Auto-close popup after 5 seconds
    setTimeout(() => {
        if (popup.style.display !== 'none') closeBtn.click();
    }, 5000);

    // Initialize Theme
    initTheme();
});

// ===== Theme Initialization & Toggle =====
function initTheme() {
    const themeToggle = document.getElementById('themeToggle');
    const themeIcon = document.getElementById('themeIcon');
    const body = document.body;

    // Check saved theme
    const savedTheme = localStorage.getItem('sentilytics-theme') || 'dark';
    if (savedTheme === 'light') {
        body.classList.add('light-mode');
        themeIcon.textContent = '☀️';
    }

    themeToggle.addEventListener('click', () => {
        body.classList.toggle('light-mode');
        const isLight = body.classList.contains('light-mode');
        localStorage.setItem('sentilytics-theme', isLight ? 'light' : 'dark');
        themeIcon.textContent = isLight ? '☀️' : '🌓';

        // Update Chart Colors if necessary
        updateChartThemes(isLight);
    });
}

function updateChartThemes(isLight) {
    const textColor = isLight ? '#64748b' : '#a0aec0';
    const gridColor = isLight ? 'rgba(0, 0, 0, 0.05)' : 'rgba(255, 255, 255, 0.1)';

    [sentimentPieChart, sentimentLineChart, keywordBarChart].forEach(chart => {
        if (!chart) return;

        if (chart.options.plugins.legend && chart.options.plugins.legend.labels) {
            chart.options.plugins.legend.labels.color = textColor;
        }

        if (chart.options.scales) {
            Object.values(chart.options.scales).forEach(scale => {
                if (scale.ticks) scale.ticks.color = textColor;
                if (scale.grid) scale.grid.color = gridColor;
            });
        }
        chart.update();
    });
}

// ===== Initialize Dashboard =====
function initializeDashboard() {
    initializeCharts();
    setupEventListeners();
    connectWebSocket();
    addActivityLog('Dashboard initialized successfully');
    addActivityLog('WebSocket connection established');
}

// ===== Chart Initialization =====
function initializeCharts() {
    // Sentiment Pie Chart
    const pieCtx = document.getElementById('sentimentPieChart').getContext('2d');
    sentimentPieChart = new Chart(pieCtx, {
        type: 'doughnut',
        data: {
            labels: ['Positive', 'Negative', 'Neutral'],
            datasets: [{
                data: [0, 0, 0],
                backgroundColor: [
                    'rgba(16, 185, 129, 0.8)',
                    'rgba(239, 68, 68, 0.8)',
                    'rgba(99, 102, 241, 0.8)'
                ],
                borderColor: [
                    'rgba(16, 185, 129, 1)',
                    'rgba(239, 68, 68, 1)',
                    'rgba(99, 102, 241, 1)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#a0aec0',
                        font: {
                            size: 12,
                            family: 'Inter'
                        },
                        padding: 15
                    }
                }
            }
        }
    });

    // Sentiment Line Chart
    const lineCtx = document.getElementById('sentimentLineChart').getContext('2d');
    sentimentLineChart = new Chart(lineCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Positive',
                    data: [],
                    borderColor: 'rgba(16, 185, 129, 1)',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    tension: 0.4,
                    fill: true
                },
                {
                    label: 'Negative',
                    data: [],
                    borderColor: 'rgba(239, 68, 68, 1)',
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    tension: 0.4,
                    fill: true
                },
                {
                    label: 'Neutral',
                    data: [],
                    borderColor: 'rgba(99, 102, 241, 1)',
                    backgroundColor: 'rgba(99, 102, 241, 0.1)',
                    tension: 0.4,
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#a0aec0',
                        font: {
                            family: 'Inter'
                        }
                    }
                },
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#a0aec0',
                        font: {
                            family: 'Inter'
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    labels: {
                        color: '#a0aec0',
                        font: {
                            family: 'Inter'
                        }
                    }
                }
            }
        }
    });

    // Keyword Bar Chart
    const barCtx = document.getElementById('keywordBarChart').getContext('2d');
    keywordBarChart = new Chart(barCtx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: 'Frequency',
                data: [],
                backgroundColor: 'rgba(102, 126, 234, 0.8)',
                borderColor: 'rgba(102, 126, 234, 1)',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            indexAxis: 'y',
            scales: {
                x: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#a0aec0',
                        font: {
                            family: 'Inter'
                        }
                    }
                },
                y: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#a0aec0',
                        font: {
                            family: 'Inter'
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

// ===== Event Listeners =====
function setupEventListeners() {
    // Analyze button
    document.getElementById('analyzeBtn').addEventListener('click', analyzeSentiment);

    // Enter key on input
    document.getElementById('keywordInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            analyzeSentiment();
        }
    });

    // Quick filter buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const keyword = btn.getAttribute('data-keyword');
            document.getElementById('keywordInput').value = keyword;
            analyzeSentiment();
        });
    });

    // Time range buttons
    document.querySelectorAll('.time-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.time-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            // In real implementation, this would fetch data for the selected time range
        });
    });

    // Clear log button
    document.getElementById('clearLog').addEventListener('click', () => {
        const logContainer = document.getElementById('activityLog');
        logContainer.innerHTML = '<div class="log-item"><span class="log-time">--:--:--</span><span class="log-message">Activity log cleared</span></div>';
        activityLogCount = 0;
    });

    // Alert close button
    document.querySelector('.alert-close').addEventListener('click', () => {
        document.getElementById('alertBanner').classList.add('hidden');
    });
}

// ===== WebSocket Connection =====
function connectWebSocket() {
    // In production, this would connect to the actual backend WebSocket
    // For now, we'll simulate real-time updates
    simulateRealTimeUpdates();
}

function simulateRealTimeUpdates() {
    // Simulate periodic updates every 5 seconds
    setInterval(() => {
        if (currentKeyword) {
            updateDashboardData();
        }
    }, 5000);
}

// ===== Sentiment Analysis =====
async function analyzeSentiment() {
    const keyword = document.getElementById('keywordInput').value.trim();

    if (!keyword) {
        showAlert('Please enter a keyword to analyze');
        return;
    }

    currentKeyword = keyword;
    addActivityLog(`Starting analysis for keyword: "${keyword}"`);

    try {
        // In production, this would call the backend API
        // For now, we'll use simulated data
        const response = await fetch(`http://localhost:8000/api/analyze?keyword=${encodeURIComponent(keyword)}`);

        if (!response.ok) {
            throw new Error('Backend not available - using simulated data');
        }

        const data = await response.json();
        updateDashboard(data);
    } catch (error) {
        console.log('Using simulated data:', error.message);
        addActivityLog('Backend unavailable - using simulated data');

        // Generate simulated data
        const simulatedData = generateSimulatedData(keyword);
        updateDashboard(simulatedData);
    }
}

// ===== Generate Simulated Data =====
function generateSimulatedData(keyword) {
    const positive = Math.floor(Math.random() * 100) + 50;
    const negative = Math.floor(Math.random() * 80) + 20;
    const neutral = Math.floor(Math.random() * 60) + 30;

    return {
        keyword: keyword,
        sentiment: {
            positive: positive,
            negative: negative,
            neutral: neutral,
            total: positive + negative + neutral
        },
        emotions: {
            joy: Math.floor(Math.random() * 60) + 20,
            anger: Math.floor(Math.random() * 40) + 10,
            fear: Math.floor(Math.random() * 30) + 10,
            sadness: Math.floor(Math.random() * 35) + 15
        },
        keywords: [
            { word: keyword, count: Math.floor(Math.random() * 100) + 50 },
            { word: 'innovation', count: Math.floor(Math.random() * 80) + 30 },
            { word: 'technology', count: Math.floor(Math.random() * 70) + 25 },
            { word: 'future', count: Math.floor(Math.random() * 60) + 20 },
            { word: 'growth', count: Math.floor(Math.random() * 50) + 15 }
        ],
        timestamp: new Date().toISOString()
    };
}

// ===== Update Dashboard =====
function updateDashboard(data) {
    // Update sentiment pie chart
    sentimentPieChart.data.datasets[0].data = [
        data.sentiment.positive,
        data.sentiment.negative,
        data.sentiment.neutral
    ];
    sentimentPieChart.update();

    // Update total posts
    document.getElementById('totalPosts').textContent = data.sentiment.total;

    // Update sentiment trend line chart
    const currentTime = new Date().toLocaleTimeString();

    if (sentimentLineChart.data.labels.length > 10) {
        sentimentLineChart.data.labels.shift();
        sentimentLineChart.data.datasets.forEach(dataset => dataset.data.shift());
    }

    sentimentLineChart.data.labels.push(currentTime);
    sentimentLineChart.data.datasets[0].data.push(data.sentiment.positive);
    sentimentLineChart.data.datasets[1].data.push(data.sentiment.negative);
    sentimentLineChart.data.datasets[2].data.push(data.sentiment.neutral);
    sentimentLineChart.update();

    // Update keyword bar chart
    keywordBarChart.data.labels = data.keywords.map(k => k.word);
    keywordBarChart.data.datasets[0].data = data.keywords.map(k => k.count);
    keywordBarChart.update();

    // Update emotion bars
    updateEmotionBar('joy', data.emotions.joy);
    updateEmotionBar('anger', data.emotions.anger);
    updateEmotionBar('fear', data.emotions.fear);
    updateEmotionBar('sadness', data.emotions.sadness);

    // Add activity log
    addActivityLog(`Analyzed ${data.sentiment.total} posts for "${data.keyword}"`);
    addActivityLog(`Sentiment: ${data.sentiment.positive} positive, ${data.sentiment.negative} negative, ${data.sentiment.neutral} neutral`);

    // Check for sentiment spike
    checkSentimentSpike(data);
}

// ===== Update Emotion Bar =====
function updateEmotionBar(emotion, percentage) {
    const bar = document.getElementById(`${emotion}Bar`);
    const value = document.getElementById(`${emotion}Value`);

    bar.style.width = `${percentage}%`;
    value.textContent = `${percentage}%`;
}

// ===== Check Sentiment Spike =====
function checkSentimentSpike(data) {
    const negativePercentage = (data.sentiment.negative / data.sentiment.total) * 100;

    if (negativePercentage > 40) {
        showAlert(`⚠️ High negative sentiment detected for "${data.keyword}" (${negativePercentage.toFixed(1)}%)`);
        addActivityLog(`ALERT: Negative sentiment spike detected!`);
    }
}

// ===== Show Alert =====
function showAlert(message) {
    const alertBanner = document.getElementById('alertBanner');
    const alertMessage = alertBanner.querySelector('.alert-message');

    alertMessage.textContent = message;
    alertBanner.classList.remove('hidden');

    // Auto-hide after 5 seconds
    setTimeout(() => {
        alertBanner.classList.add('hidden');
    }, 5000);
}

// ===== Add Activity Log =====
function addActivityLog(message) {
    const logContainer = document.getElementById('activityLog');
    const logItem = document.createElement('div');
    logItem.className = 'log-item';

    const currentTime = new Date().toLocaleTimeString();

    logItem.innerHTML = `
        <span class="log-time">${currentTime}</span>
        <span class="log-message">${message}</span>
    `;

    logContainer.insertBefore(logItem, logContainer.firstChild);

    // Keep only last 50 log items
    activityLogCount++;
    if (activityLogCount > 50) {
        logContainer.removeChild(logContainer.lastChild);
        activityLogCount = 50;
    }
}

// ===== Update Dashboard Data (Real-time simulation) =====
function updateDashboardData() {
    if (!currentKeyword) return;

    const simulatedData = generateSimulatedData(currentKeyword);

    // Update only the charts, not the full dashboard
    sentimentPieChart.data.datasets[0].data = [
        simulatedData.sentiment.positive,
        simulatedData.sentiment.negative,
        simulatedData.sentiment.neutral
    ];
    sentimentPieChart.update();

    const currentTime = new Date().toLocaleTimeString();

    if (sentimentLineChart.data.labels.length > 10) {
        sentimentLineChart.data.labels.shift();
        sentimentLineChart.data.datasets.forEach(dataset => dataset.data.shift());
    }

    sentimentLineChart.data.labels.push(currentTime);
    sentimentLineChart.data.datasets[0].data.push(simulatedData.sentiment.positive);
    sentimentLineChart.data.datasets[1].data.push(simulatedData.sentiment.negative);
    sentimentLineChart.data.datasets[2].data.push(simulatedData.sentiment.neutral);
    sentimentLineChart.update();

    addActivityLog(`Real-time update: ${simulatedData.sentiment.total} posts processed`);
}

// ===== Add fadeOut animation =====
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeOut {
        from {
            opacity: 1;
        }
        to {
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
