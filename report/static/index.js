document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById('portfolio-chart').getContext('2d');

    const labels = backtestData.history.map(h => h.date);
    const portfolioValues = backtestData.history.map(h => h.value);

    const buyTrades = backtestData.trades.filter(t => t.action === 'buy');
    const sellTrades = backtestData.trades.filter(t => t.action === 'sell');

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Portfolio Value',
                data: portfolioValues,
                borderColor: '#4A90E2',
                tension: 0.1,
                pointRadius: 0, // Hide points by default
            }, {
                label: 'Buy',
                data: buyTrades.map(trade => ({
                    x: trade.date,
                    y: portfolioValues[labels.indexOf(trade.date)]
                })),
                pointStyle: 'triangle',
                radius: 8,
                backgroundColor: '#7ED321',
                borderColor: '#5E9D1A',
                showLine: false,
            }, {
                label: 'Sell',
                data: sellTrades.map(trade => ({
                    x: trade.date,
                    y: portfolioValues[labels.indexOf(trade.date)]
                })),
                pointStyle: 'crossRot',
                radius: 8,
                backgroundColor: '#D0021B',
                borderColor: '#A00115',
                showLine: false,
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: false,
                    ticks: {
                        callback: function(value, index, values) {
                            return '$' + value.toLocaleString();
                        }
                    }
                }
            },
            plugins: {
                tooltip: {
                    mode: 'index',
                    intersect: false,
                }
            }
        }
    });
});