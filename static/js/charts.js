// Charts.js - Gráficos do sistema

let membershipChart = null;
let simulationChart = null;

// Plota função de pertinência
function plotMembershipFunction(variable) {
    const canvas = document.getElementById('membershipChart');
    const ctx = canvas.getContext('2d');
    
    if (!membershipData || !membershipData[variable]) {
        return;
    }
    
    const data = membershipData[variable];
    const datasets = [];
    
    const colors = [
        '#ef4444', '#f59e0b', '#10b981', '#3b82f6', '#8b5cf6', '#ec4899', '#6366f1'
    ];
    
    let colorIndex = 0;
    for (let term in data.terms) {
        datasets.push({
            label: term,
            data: data.terms[term],
            borderColor: colors[colorIndex % colors.length],
            backgroundColor: colors[colorIndex % colors.length] + '20',
            borderWidth: 2,
            fill: true,
            tension: 0.4
        });
        colorIndex++;
    }
    
    if (membershipChart) {
        membershipChart.destroy();
    }
    
    membershipChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.universe.map((v, i) => i % 20 === 0 ? v.toFixed(1) : ''),
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: `Funções de Pertinência - ${getVariableName(variable)}`,
                    font: { size: 16 }
                },
                legend: {
                    position: 'top'
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: getVariableUnit(variable)
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Grau de Pertinência'
                    },
                    min: 0,
                    max: 1
                }
            }
        }
    });
}

// Plota gráfico de simulação
function plotSimulationChart(results) {
    const canvas = document.getElementById('simulationChart');
    const ctx = canvas.getContext('2d');
    
    // Reduz pontos para melhor visualização (pega 1 a cada 10)
    const step = 10;
    const times = results.time.filter((_, i) => i % step === 0);
    const temps = results.temperature.filter((_, i) => i % step === 0);
    const powers = results.power_crac.filter((_, i) => i % step === 0);
    const setpoints = results.setpoint.filter((_, i) => i % step === 0);
    
    if (simulationChart) {
        simulationChart.destroy();
    }
    
    simulationChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: times.map(t => `${Math.floor(t/60)}h`),
            datasets: [
                {
                    label: 'Temperatura (°C)',
                    data: temps,
                    borderColor: '#ef4444',
                    backgroundColor: '#ef444420',
                    borderWidth: 2,
                    yAxisID: 'y',
                    tension: 0.4
                },
                {
                    label: 'Setpoint (°C)',
                    data: setpoints,
                    borderColor: '#10b981',
                    borderDash: [5, 5],
                    borderWidth: 2,
                    yAxisID: 'y',
                    pointRadius: 0
                },
                {
                    label: 'Potência CRAC (%)',
                    data: powers,
                    borderColor: '#3b82f6',
                    backgroundColor: '#3b82f620',
                    borderWidth: 2,
                    yAxisID: 'y1',
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Simulação de 24 Horas - Comportamento do Sistema',
                    font: { size: 16 }
                },
                legend: {
                    position: 'top'
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Tempo (horas)'
                    }
                },
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Temperatura (°C)'
                    },
                    min: 18,
                    max: 26
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Potência CRAC (%)'
                    },
                    min: 0,
                    max: 100,
                    grid: {
                        drawOnChartArea: false
                    }
                }
            }
        }
    });
}

// Nomes das variáveis
function getVariableName(variable) {
    const names = {
        'erro': 'Erro de Temperatura',
        'delta_erro': 'Variação do Erro (Δe)',
        'temp_externa': 'Temperatura Externa',
        'carga_termica': 'Carga Térmica',
        'potencia_crac': 'Potência CRAC (Saída)'
    };
    return names[variable] || variable;
}

// Unidades das variáveis
function getVariableUnit(variable) {
    const units = {
        'erro': 'Erro (°C)',
        'delta_erro': 'Δe (°C)',
        'temp_externa': 'Temperatura (°C)',
        'carga_termica': 'Carga (%)',
        'potencia_crac': 'Potência (%)'
    };
    return units[variable] || '';
}
