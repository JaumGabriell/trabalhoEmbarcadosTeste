import paho.mqtt.client as mqtt
import json
import time

class MQTTClient:
    """Cliente MQTT para monitoramento"""
    
    def __init__(self, broker="localhost", port=1883):
        self.broker = broker
        self.port = port
        self.client = mqtt.Client()
        self.connected = False
        
        self.topics = {
            'alert': 'datacenter/fuzzy/alert',
            'control': 'datacenter/fuzzy/control',
            'temp': 'datacenter/fuzzy/temp'
        }
    
    def connect(self):
        """Conecta ao broker MQTT"""
        try:
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
            self.connected = True
            return True
        except:
            self.connected = False
            return False
    
    def disconnect(self):
        """Desconecta do broker"""
        self.client.loop_stop()
        self.client.disconnect()
        self.connected = False
    
    def publish_alert(self, alert_data):
        """Publica alerta"""
        if self.connected:
            try:
                payload = json.dumps(alert_data)
                self.client.publish(self.topics['alert'], payload)
            except:
                pass
    
    def publish_control_data(self, data):
        """Publica dados de controle"""
        if self.connected:
            try:
                payload = json.dumps(data)
                self.client.publish(self.topics['control'], payload)
                self.client.publish(self.topics['temp'], str(data.get('erro', 0)))
            except:
                pass
    
    def is_connected(self):
        """Verifica se está conectado"""
        return self.connected
