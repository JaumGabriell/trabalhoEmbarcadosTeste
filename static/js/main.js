// Main JavaScript para o Sistema Fuzzy

let currentTab = 'erro';
let membershipData = null;

// Carrega funções de pertinência ao iniciar
document.addEventListener('DOMContentLoaded', function() {
    loadMembershipFunctions();
});

// Carrega dados das funções de pertinência
async function loadMembershipFunctions() {
    try {
        const response = await fetch('/api/membership_functions');
        const result = await response.json();
        
        if (result.success) {
            membershipData = result.data;
            // Plota o gráfico inicial sem passar evento
            plotMembershipFunction('erro');
        }
    } catch (error) {
        console.error('Erro ao carregar funções de pertinência:', error);
    }
}

// Calcula potência CRAC
async function calculate() {
    const erro = parseFloat(document.getElementById('erro').value);
    const delta_erro = parseFloat(document.getElementById('delta_erro').value);
    const temp_externa = parseFloat(document.getElementById('temp_externa').value);
    const carga_termica = parseFloat(document.getElementById('carga_termica').value);
    
    try {
        const response = await fetch('/api/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                erro: erro,
                delta_erro: delta_erro,
                temp_externa: temp_externa,
                carga_termica: carga_termica
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            displayOutput(result.potencia_crac);
            displayInferenceDetails(result.inference_details);
        } else {
            alert('Erro no cálculo: ' + result.error);
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao calcular potência CRAC');
    }
}

// Exibe resultado
function displayOutput(power) {
    document.getElementById('output-value').textContent = power.toFixed(2);
    document.getElementById('power-bar-fill').style.width = power + '%';
}

// Exibe detalhes da inferência
function displayInferenceDetails(details) {
    if (!details) return;
    
    let html = '<h3>Valores Fuzzy das Entradas:</h3>';
    html += '<div class="metrics-grid">';
    
    // Mostra os valores fuzzy mais significativos
    for (let variable in details.fuzzy_values) {
        html += `<div class="metric"><strong>${variable}:</strong><br>`;
        for (let term in details.fuzzy_values[variable]) {
            const value = details.fuzzy_values[variable][term];
            if (value > 0.01) {
                html += `${term}: ${value.toFixed(3)}<br>`;
            }
        }
        html += '</div>';
    }
    html += '</div>';
    
    html += `<h3>Regras Ativadas: ${details.activated_rules_count}</h3>`;
    html += '<div class="message-container">';
    
    details.activated_rules.forEach((rule, i) => {
        html += `<div class="message-item">
            <strong>Regra ${i+1}:</strong> 
            Ativação: ${rule.activation.toFixed(3)}<br>
            IF Erro=${rule.conditions.erro} AND ΔErro=${rule.conditions.delta_erro} 
            AND TempExt=${rule.conditions.temp_externa} AND Carga=${rule.conditions.carga_termica}
            THEN Potência=${rule.output}
        </div>`;
    });
    
    html += '</div>';
    
    document.getElementById('inference-details').innerHTML = html;
}

// Muda aba de funções de pertinência
function showTab(tabName, event) {
    currentTab = tabName;
    
    // Atualiza botões
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    if (event && event.target) {
        event.target.classList.add('active');
    }
    
    // Atualiza gráfico
    if (membershipData) {
        plotMembershipFunction(tabName);
    }
}

// Reseta inputs
function resetInputs() {
    document.getElementById('erro').value = 0;
    document.getElementById('delta_erro').value = 0;
    document.getElementById('temp_externa').value = 25;
    document.getElementById('carga_termica').value = 40;
    document.getElementById('output-value').textContent = '--';
    document.getElementById('power-bar-fill').style.width = '0%';
    document.getElementById('inference-details').innerHTML = 
        '<p class="text-muted">Execute o cálculo para ver os detalhes da inferência</p>';
}

// Executa simulação de 24h
async function runSimulation() {
    const temp_inicial = parseFloat(document.getElementById('sim_temp_inicial').value);
    const temp_externa = parseFloat(document.getElementById('sim_temp_externa').value);
    const carga_base = parseFloat(document.getElementById('sim_carga_base').value);
    
    // Mostra loading com mensagem
    document.getElementById('simulation-results').innerHTML = `
        <div style="text-align: center; padding: 40px;">
            <div class="loading"></div>
            <h3 style="margin-top: 20px; color: #2196F3;">⏳ Simulando 1440 minutos (24 horas)...</h3>
            <p style="color: #666;">Isso pode levar 20-30 segundos. Por favor, aguarde...</p>
            <p style="color: #999; font-size: 0.9em;">🔍 Acompanhe o progresso no terminal do servidor</p>
        </div>
    `;
    document.getElementById('simulation-results').style.display = 'block';
    
    try {
        // Aumenta o timeout para 60 segundos
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 60000);
        
        const response = await fetch('/api/simulation/start', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                temp_inicial: temp_inicial,
                temp_externa_base: temp_externa,
                carga_base: carga_base
            }),
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        const result = await response.json();
        
        if (result.success) {
            displaySimulationResults(result.results, result.metrics);
        } else {
            document.getElementById('simulation-results').innerHTML = `
                <div style="text-align: center; padding: 40px; color: #f44336;">
                    <h3>❌ Erro na simulação</h3>
                    <p>${result.error}</p>
                </div>
            `;
        }
    } catch (error) {
        console.error('Erro:', error);
        if (error.name === 'AbortError') {
            document.getElementById('simulation-results').innerHTML = `
                <div style="text-align: center; padding: 40px; color: #ff9800;">
                    <h3>⏱️ Tempo esgotado</h3>
                    <p>A simulação está demorando mais que o esperado.</p>
                    <p>Verifique o console do navegador e o terminal do servidor.</p>
                </div>
            `;
        } else {
            document.getElementById('simulation-results').innerHTML = `
                <div style="text-align: center; padding: 40px; color: #f44336;">
                    <h3>❌ Erro ao executar simulação</h3>
                    <p>Verifique o console do navegador (F12) para mais detalhes.</p>
                    <p style="font-size: 0.9em; color: #666;">Erro: ${error.message}</p>
                </div>
            `;
        }
    }
}

// Exibe resultados da simulação
function displaySimulationResults(results, metrics) {
    // Primeiro cria a estrutura HTML
    document.getElementById('simulation-results').innerHTML = `
        <div class="metrics-grid">
            <div class="metric">
                <div class="metric-value" id="metric-rmse">${metrics.rmse.toFixed(3)}</div>
                <div class="metric-label">RMSE</div>
            </div>
            <div class="metric">
                <div class="metric-value" id="metric-range">${metrics.percent_in_range.toFixed(1)}%</div>
                <div class="metric-label">% Tempo em Faixa</div>
            </div>
            <div class="metric">
                <div class="metric-value" id="metric-violations">${metrics.violations}</div>
                <div class="metric-label">Violações</div>
            </div>
            <div class="metric">
                <div class="metric-value" id="metric-energy">${metrics.energy_consumption.toFixed(0)}</div>
                <div class="metric-label">Energia Total</div>
            </div>
        </div>
        <div class="chart-container">
            <canvas id="simulationChart"></canvas>
        </div>
    `;
    
    // Plota gráfico
    plotSimulationChart(results);
}
