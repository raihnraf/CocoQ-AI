const CHART_COLORS = {
    'Grade A': '#2d6a4f',
    'Grade B': '#e9c46a',
    'Reject': '#e76f51',
};

const CHART_DEFAULTS = {
    responsive: true,
    maintainAspectRatio: false,
};

function renderGradeDistribution(canvasId, gradeDistribution) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Grade A', 'Grade B', 'Reject'],
            datasets: [{
                data: [
                    gradeDistribution['Grade A'].count,
                    gradeDistribution['Grade B'].count,
                    gradeDistribution['Reject'].count,
                ],
                backgroundColor: [CHART_COLORS['Grade A'], CHART_COLORS['Grade B'], CHART_COLORS['Reject']],
                borderWidth: 2,
                borderColor: '#fff',
            }],
        },
        options: {
            ...CHART_DEFAULTS,
            plugins: {
                legend: { position: 'bottom' },
            },
        },
    });
}

function renderRejectTrend(canvasId, trendData) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: trendData.map(d => d.date),
            datasets: [{
                label: 'Reject Rate (%)',
                data: trendData.map(d => d.reject_rate),
                borderColor: '#e76f51',
                backgroundColor: 'rgba(231,111,81,0.1)',
                fill: true,
                tension: 0.3,
                pointRadius: 4,
                pointBackgroundColor: '#e76f51',
            }],
        },
        options: {
            ...CHART_DEFAULTS,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: { callback: v => v + '%' },
                },
            },
        },
    });
}

function renderFeatureImportance(canvasId, features) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: features.map(f => f.feature),
            datasets: [{
                label: 'Importance',
                data: features.map(f => f.importance),
                backgroundColor: '#2d6a4f',
                borderRadius: 4,
            }],
        },
        options: {
            ...CHART_DEFAULTS,
            indexAxis: 'y',
            scales: {
                x: {
                    beginAtZero: true,
                    max: 1,
                    ticks: { callback: v => (v * 100).toFixed(0) + '%' },
                },
            },
            plugins: {
                legend: { display: false },
            },
        },
    });
}

async function loadAndRenderFeatureImportance(canvasId) {
    try {
        const res = await fetch('/api/feature-importance');
        const data = await res.json();
        renderFeatureImportance(canvasId, data.features);
    } catch (e) {
        console.error('Failed to load feature importance:', e);
    }
}

async function loadAndRenderDashboardCharts() {
    try {
        const res = await fetch('/api/stats');
        const stats = await res.json();

        if (document.getElementById('grade-dist-chart')) {
            renderGradeDistribution('grade-dist-chart', stats.grade_distribution);
        }
        if (document.getElementById('reject-trend-chart')) {
            renderRejectTrend('reject-trend-chart', stats.reject_trend);
        }
    } catch (e) {
        console.error('Failed to load dashboard charts:', e);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    loadAndRenderDashboardCharts();
    if (document.getElementById('feature-importance-chart')) {
        loadAndRenderFeatureImportance('feature-importance-chart');
    }
});
