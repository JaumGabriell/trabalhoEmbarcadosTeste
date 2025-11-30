#!/usr/bin/env python3
"""
Script para monitorar mensagens MQTT do sistema fuzzy
Execute em um terminal separado enquanto o sistema está rodando
"""

import paho.mqtt.client as mqtt
import json
from datetime import datetime

# Callback quando conecta
def on_connect(client, userdata, flags, rc):
    print("=" * 60)
    print("🟢 CONECTADO AO BROKER MQTT!")
    print("=" * 60)
    print("\n📡 Inscrito nos tópicos:")
    
    # Subscribe em todos os tópicos
    topics = [
        'datacenter/fuzzy/control',
        'datacenter/fuzzy/temp',
        'datacenter/fuzzy/alert'
    ]
    
    for topic in topics:
        client.subscribe(topic)
        print(f"   ✓ {topic}")
    
    print("\n👂 Aguardando mensagens...\n")
    print("-" * 60)

# Callback quando recebe mensagem
def on_message(client, userdata, msg):
    timestamp = datetime.now().strftime('%H:%M:%S')
    topic = msg.topic
    
    print(f"\n[{timestamp}] 📨 Tópico: {topic}")
    
    try:
        # Tenta decodificar como JSON
        payload = json.loads(msg.payload.decode())
        print(f"Dados: {json.dumps(payload, indent=2, ensure_ascii=False)}")
    except:
        # Se não for JSON, mostra como texto
        payload = msg.payload.decode()
        print(f"Mensagem: {payload}")
    
    print("-" * 60)

# Cria cliente MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Conecta ao broker local
print("\n🔄 Conectando ao broker MQTT (localhost:1883)...")

try:
    client.connect("localhost", 1883, 60)
    
    # Loop para processar mensagens
    client.loop_forever()
    
except KeyboardInterrupt:
    print("\n\n👋 Encerrando subscriber MQTT...")
    client.disconnect()
    
except Exception as e:
    print(f"\n❌ Erro ao conectar: {e}")
    print("\n💡 Certifique-se de que o mosquitto está rodando:")
    print("   sudo systemctl start mosquitto")
