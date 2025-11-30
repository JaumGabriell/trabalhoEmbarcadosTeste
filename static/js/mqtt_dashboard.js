// JavaScript para Dashboard MQTT - Atualizado para mostrar mensagens reais

let currentMqttTab = 'control';
let startTime = Date.now();

// Atualiza status MQTT
async function updateMqttStatus() {
    try {
        const response = await fetch('/api/mqtt/status');
        const data = await response.json();
        
        const statusContainer = document.getElementById('mqtt-status');
        const brokerInfo = document.getElementById('broker-info');
        const portInfo = document.getElementById('port-info');
        
        if (data.connected) {
            statusContainer.innerHTML = `
                <span class="status-dot connected"></span>
                <span class="status-text">✅ Conectado</span>
            `;
        } else {
            statusContainer.innerHTML = `
                <span class="status-dot disconnected"></span>
                <span class="status-text">⚠️ Desconectado (Modo Simulação)</span>
            `;
        }
        
        brokerInfo.textContent = data.broker;
        portInfo.textContent = data.port;
    } catch (error) {
        console.error('Erro ao atualizar status MQTT:', error);
    }
}

// Atualiza alertas
async function updateAlerts() {
    try {
        const response = await fetch('/api/alerts');
        const data = await response.json();
        
        const container = document.getElementById('alerts-container');
        
        if (data.alerts && data.alerts.length > 0) {
            document.getElementById('alert-count').textContent = data.alerts.length;
            
            let html = '<div class="alert-list">';
            data.alerts.forEach(alert => {
                const time = new Date(alert.timestamp * 1000).toLocaleTimeString();
                html += `
                    <div class="alert-item ${alert.level}">
                        <strong>[${time}]</strong> ${alert.message}
                    </div>
                `;
            });
            html += '</div>';
            container.innerHTML = html;
        } else {
            container.innerHTML = '<p class="text-muted">Nenhum alerta recente</p>';
        }
    } catch (error) {
        console.error('Erro ao atualizar alertas:', error);
    }
}

// Atualiza mensagens MQTT (NOVO!)
async function updateMqttMessages() {
    try {
        const response = await fetch('/api/mqtt/messages');
        const result = await response.json();
        
        // Atualiza contador
        document.getElementById('msg-count').textContent = result.total_count || 0;
        
        // Exibe mensagens
        displayMqttMessages(result.messages || []);
    } catch (error) {
        console.error('Erro ao atualizar mensagens MQTT:', error);
    }
}

// Troca aba MQTT
function showMqttTab(tabName, event) {
    currentMqttTab = tabName;
    
    // Atualiza botões
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    if (event && event.target) {
        event.target.classList.add('active');
    }
}

// Exibe mensagens MQTT (NOVO! Mostra dados REAIS)
function displayMqttMessages(messages) {
    const container = document.getElementById('mqtt-messages');
    
    if (messages && messages.length > 0) {
        let html = '<div class="message-list" style="max-height: 400px; overflow-y: auto;">';
        
        // Inverte para mostrar mais recentes primeiro
        const reversedMessages = [...messages].reverse();
        
        reversedMessages.forEach(msg => {
            const time = new Date(msg.timestamp * 1000).toLocaleTimeString();
            const data = msg.data;
            
            html += `
                <div class="message-item" style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 12px; margin-bottom: 10px; background: #f9f9f9;">
                    <div class="message-header" style="margin-bottom: 8px; padding-bottom: 8px; border-bottom: 1px solid #e0e0e0;">
                        <span class="message-time" style="color: #666; font-size: 0.9em;">🕐 ${time}</span>
                        <span class="message-topic" style="color: #2196F3; font-weight: bold; margin-left: 15px;">📡 ${msg.topic}</span>
                    </div>
                    <div class="message-data" style="font-size: 0.95em; line-height: 1.6;">
                        <strong>Erro:</strong> ${data.erro?.toFixed(2) || 'N/A'}°C | 
                        <strong>ΔErro:</strong> ${data.delta_erro?.toFixed(2) || 'N/A'} | 
                        <strong>Temp Ext:</strong> ${data.temp_externa?.toFixed(1) || 'N/A'}°C | 
                        <strong>Carga:</strong> ${data.carga_termica?.toFixed(0) || 'N/A'}%<br>
                        <strong style="color: #4CAF50;">🎯 Potência CRAC:</strong> <span style="background: #4CAF50; color: white; padding: 2px 8px; border-radius: 4px; font-weight: bold;">${data.potencia_crac?.toFixed(2) || 'N/A'}%</span>
                    </div>
                </div>
            `;
        });
        
        html += '</div>';
        container.innerHTML = html;
    } else {
        container.innerHTML = `
            <p class="text-muted" style="text-align: center; padding: 40px;">
                📭 Aguardando mensagens...<br>
                <small>Execute um cálculo na <a href="/">interface principal</a>!</small>
            </p>
        `;
    }
}

// Atualiza tempo online
function updateUptime() {
    const elapsed = Date.now() - startTime;
    const minutes = Math.floor(elapsed / 60000);
    const seconds = Math.floor((elapsed % 60000) / 1000);
    
    document.getElementById('uptime').textContent = 
        `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}

// Inicializa dashboard
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Dashboard MQTT inicializado');
    
    // Carrega dados iniciais
    updateMqttStatus();
    updateAlerts();
    updateMqttMessages();
    
    // Atualiza a cada 2 segundos
    setInterval(updateMqttStatus, 2000);
    setInterval(updateAlerts, 2000);
    setInterval(updateMqttMessages, 2000);
    setInterval(updateUptime, 1000);
});
