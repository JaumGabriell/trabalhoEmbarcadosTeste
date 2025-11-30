// MQTT Dashboard JavaScript

let mqttMessages = [];
let alertCount = 0;
let messageCount = 0;
let startTime = Date.now();
let currentMqttTab = 'control';

// Inicializa dashboard
document.addEventListener('DOMContentLoaded', function() {
    checkMqttStatus();
    loadAlerts();
    updateUptime();
    
    // Atualiza a cada 5 segundos
    setInterval(() => {
        checkMqttStatus();
        loadAlerts();
    }, 5000);
    
    // Atualiza uptime a cada segundo
    setInterval(updateUptime, 1000);
});

// Verifica status MQTT
async function checkMqttStatus() {
    try {
        const response = await fetch('/api/mqtt/status');
        const status = await response.json();
        
        const statusIndicator = document.getElementById('mqtt-status');
        const dot = statusIndicator.querySelector('.status-dot');
        const text = statusIndicator.querySelector('.status-text');
        
        if (status.connected) {
            dot.classList.add('connected');
            dot.classList.remove('disconnected');
            text.textContent = 'Conectado';
            text.style.color = '#10b981';
        } else {
            dot.classList.add('disconnected');
            dot.classList.remove('connected');
            text.textContent = 'Desconectado (Modo Simulação)';
            text.style.color = '#ef4444';
        }
        
        document.getElementById('broker-info').textContent = status.broker;
        document.getElementById('port-info').textContent = status.port;
        
    } catch (error) {
        console.error('Erro ao verificar status MQTT:', error);
    }
}

// Carrega alertas
async function loadAlerts() {
    try {
        const response = await fetch('/api/alerts');
        const data = await response.json();
        
        alertCount = data.alerts.length;
        document.getElementById('alert-count').textContent = alertCount;
        
        const container = document.getElementById('alerts-container');
        
        if (data.alerts.length === 0) {
            container.innerHTML = '<p class="text-muted">Nenhum alerta recente</p>';
            return;
        }
        
        let html = '';
        data.alerts.reverse().forEach(alert => {
            const time = new Date(alert.timestamp * 1000).toLocaleTimeString('pt-BR');
            const alertClass = alert.level === 'critical' ? 'critical' : '';
            
            html += `
                <div class="alert-item ${alertClass}">
                    <strong>${alert.level.toUpperCase()}</strong> - ${time}<br>
                    ${alert.message}
                </div>
            `;
        });
        
        container.innerHTML = html;
        
    } catch (error) {
        console.error('Erro ao carregar alertas:', error);
    }
}

// Muda aba do MQTT
function showMqttTab(tab) {
    currentMqttTab = tab;
    
    // Atualiza botões
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Atualiza conteúdo
    updateMqttMessages();
}

// Atualiza mensagens MQTT (simulado)
function updateMqttMessages() {
    const container = document.getElementById('mqtt-messages');
    
    let html = '<p class="text-muted">Mensagens seriam exibidas aqui em tempo real via WebSocket/MQTT</p>';
    html += '<p class="text-muted">Tópicos monitorados:</p>';
    html += '<ul>';
    html += '<li><code>datacenter/fuzzy/control</code> - Dados de controle</li>';
    html += '<li><code>datacenter/fuzzy/temp</code> - Temperatura atual</li>';
    html += '<li><code>datacenter/fuzzy/alert</code> - Alertas críticos</li>';
    html += '</ul>';
    
    container.innerHTML = html;
}

// Atualiza tempo online
function updateUptime() {
    const elapsed = Date.now() - startTime;
    const minutes = Math.floor(elapsed / 60000);
    const seconds = Math.floor((elapsed % 60000) / 1000);
    
    document.getElementById('uptime').textContent = 
        `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}

// Atualiza contador de mensagens (chamado do main.js quando há cálculo)
function incrementMessageCount() {
    messageCount++;
    document.getElementById('msg-count').textContent = messageCount;
}
