

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json
import numpy as np
from fuzzy_controler.fuzzy_engine import FuzzyController
from simulation.temporal_simulation import TemporalSimulation
from mqtt.mqtt_client import MQTTClient
import threading
import time

app = Flask(__name__)
CORS(app)

# Instâncias globais
fuzzy_controller = FuzzyController()
simulation = TemporalSimulation(fuzzy_controller)
mqtt_client = MQTTClient()

# Estado global
system_state = {
    'running': False,
    'current_temp': 22.0,
    'current_power': 50.0,
    'alerts': []
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mqtt_dashboard')
def mqtt_dashboard():
    return render_template('mqtt_dashboard.html')

@app.route('/api/calculate', methods=['POST'])
def calculate():
    """Calcula a saída fuzzy para entradas dadas"""
    try:
        data = request.get_json()
        
        erro = float(data.get('erro', 0))
        delta_erro = float(data.get('delta_erro', 0))
        temp_externa = float(data.get('temp_externa', 25))
        carga_termica = float(data.get('carga_termica', 40))
        
        # Calcula potência CRAC usando controlador fuzzy
        potencia_crac = fuzzy_controller.calculate(
            erro, delta_erro, temp_externa, carga_termica
        )
        
        # Obtém detalhes do processo de inferência
        inference_details = fuzzy_controller.get_inference_details()
        
        # Atualiza estado global
        system_state['current_power'] = potencia_crac
        
        # Envia para MQTT
        mqtt_client.publish_control_data({
            'erro': erro,
            'delta_erro': delta_erro,
            'temp_externa': temp_externa,
            'carga_termica': carga_termica,
            'potencia_crac': potencia_crac
        })
        
        return jsonify({
            'success': True,
            'potencia_crac': round(potencia_crac, 2),
            'inference_details': inference_details
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/membership_functions', methods=['GET'])
def get_membership_functions():
    """Retorna dados das funções de pertinência"""
    try:
        mf_data = fuzzy_controller.get_membership_functions_data()
        return jsonify({
            'success': True,
            'data': mf_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/simulation/start', methods=['POST'])
def start_simulation():
    """Inicia simulação de 24 horas"""
    try:
        data = request.get_json()
        
        # Parâmetros da simulação
        temp_inicial = float(data.get('temp_inicial', 22.0))
        temp_externa_base = float(data.get('temp_externa_base', 25.0))
        carga_base = float(data.get('carga_base', 40.0))
        
        # Executa simulação
        results = simulation.run_24h_simulation(
            temp_inicial=temp_inicial,
            temp_externa_base=temp_externa_base,
            carga_base=carga_base
        )
        
        # Calcula métricas
        metrics = simulation.calculate_metrics(results)
        
        return jsonify({
            'success': True,
            'results': results,
            'metrics': metrics
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/rules', methods=['GET'])
def get_rules():
    """Retorna a base de regras fuzzy"""
    try:
        rules = fuzzy_controller.get_rules_base()
        return jsonify({
            'success': True,
            'rules': rules
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/mqtt/status', methods=['GET'])
def mqtt_status():
    """Retorna status da conexão MQTT"""
    return jsonify({
        'connected': mqtt_client.is_connected(),
        'broker': mqtt_client.broker,
        'port': mqtt_client.port
    })

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """Retorna alertas do sistema"""
    return jsonify({
        'alerts': system_state['alerts'][-10:]  # Últimos 10 alertas
    })

def check_alerts(temp, power):
    """Verifica condições de alerta"""
    alerts = []
    
    if temp < 18:
        alert = {
            'level': 'critical',
            'message': f'Temperatura crítica baixa: {temp:.1f}°C',
            'timestamp': time.time()
        }
        alerts.append(alert)
        mqtt_client.publish_alert(alert)
        
    elif temp > 26:
        alert = {
            'level': 'critical',
            'message': f'Temperatura crítica alta: {temp:.1f}°C',
            'timestamp': time.time()
        }
        alerts.append(alert)
        mqtt_client.publish_alert(alert)
    
    if power > 95:
        alert = {
            'level': 'warning',
            'message': f'Potência CRAC muito alta: {power:.1f}%',
            'timestamp': time.time()
        }
        alerts.append(alert)
        mqtt_client.publish_alert(alert)
    
    system_state['alerts'].extend(alerts)
    
    # Mantém apenas últimos 100 alertas
    if len(system_state['alerts']) > 100:
        system_state['alerts'] = system_state['alerts'][-100:]

if __name__ == '__main__':
    print("=" * 60)
    print("Sistema Fuzzy para Controle de Refrigeração de Data Center")
    print("=" * 60)
    print("\n🚀 Iniciando servidor...")
    print("📡 Conectando ao broker MQTT...")
    
    # Tenta conectar ao MQTT (modo simulação se falhar)
    try:
        mqtt_client.connect()
        print("✅ MQTT conectado com sucesso!")
    except:
        print("⚠️  MQTT em modo simulação (broker não disponível)")
    
    print("\n🌐 Acesse: http://localhost:3500")
    print("📊 Dashboard MQTT: http://localhost:3500/mqtt_dashboard")
    print("\n" + "=" * 60 + "\n")
    
    app.run(debug=False, host='0.0.0.0', port=3500, threaded=True)