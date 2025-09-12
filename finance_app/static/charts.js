document.addEventListener("DOMContentLoaded", function () {
    const chartData = document.getElementById("chart-data").dataset;

    const receitas = Number(chartData.receitas || 0);
    const despesas = Number(chartData.despesas || 0);

    let invLabels = [];
    let invValues = [];

    try {
        invLabels = JSON.parse(chartData.labels || "[]");
        invValues = JSON.parse(chartData.values || "[]");
    } catch (e) {
        console.error("Erro ao carregar dados de investimentos:", e);
    }

    // agora cria os gráficos só se tiver elementos <canvas>
    if (document.getElementById('chartReceitasDespesas')) {
        new Chart(document.getElementById('chartReceitasDespesas'), {
            type: 'bar',
            data: {
                labels: ['Receitas','Despesas'],
                datasets: [{
                    data: [receitas, despesas],
                    backgroundColor: ['#28a745','#dc3545']
                }]
            },
            options: { plugins: { legend: { display: false } } }
        });
    }

    if (document.getElementById('chartInvestimentos') && invLabels.length > 0) {
        new Chart(document.getElementById('chartInvestimentos'), {
            type: 'doughnut',
            data: {
                labels: invLabels,
                datasets: [{
                    data: invValues,
                    backgroundColor: ['#0d6efd','#20c997','#ffc107','#6f42c1']
                }]
            }
        });
    }

    if (document.getElementById('chartValorPorTipo') && invLabels.length > 0) {
        new Chart(document.getElementById('chartValorPorTipo'), {
            type: 'bar',
            data: {
                labels: invLabels,
                datasets: [{
                    data: invValues,
                    backgroundColor: '#17a2b8'
                }]
            },
            options: {
                indexAxis: 'y',
                plugins: { legend: { display: false } }
            }
        });
    }
});