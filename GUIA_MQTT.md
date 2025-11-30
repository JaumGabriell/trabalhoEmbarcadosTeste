# 📡 Guia de Uso do MQTT

## 🎯 O que é MQTT?

MQTT (Message Queuing Telemetry Transport) é um protocolo leve de mensagens usado para comunicação IoT. Neste projeto, usamos para monitorar o sistema de controle em tempo real.

## 🚀 Como Testar o MQTT

Você tem um broker Mosquitto rodando localmente na porta **1883**.

### Opção 1: Usar o Script Python (Recomendado)

Em um **terminal separado** (deixe o app.py rodando), execute:

```bash
# Ative o venv primeiro
source venv/bin/activate

# Execute o subscriber
python mqtt_subscriber.py
```

Você verá:
```
🟢 CONECTADO AO BROKER MQTT!
📡 Inscrito nos tópicos:
   ✓ datacenter/fuzzy/control
   ✓ datacenter/fuzzy/temp
   ✓ datacenter/fuzzy/alert

👂 Aguardando mensagens...
```

### Opção 2: Usar mosquitto_sub (linha de comando)

```bash
# Terminal 1 - Controle
mosquitto_sub -h localhost -t "datacenter/fuzzy/control" -v

# Terminal 2 - Temperatura
mosquitto_sub -h localhost -t "datacenter/fuzzy/temp" -v

# Terminal 3 - Alertas
mosquitto_sub -h localhost -t "datacenter/fuzzy/alert" -v
```

### Opção 3: Usar MQTT Explorer (Interface Gráfica)

1. Baixe: http://mqtt-explorer.com/
2. Conecte em `localhost:1883`
3. Veja todos os tópicos `datacenter/fuzzy/*`

## 📊 Tópicos MQTT

### 1. `datacenter/fuzzy/control`
Dados de cada cálculo do controlador:
```json
{
  "erro": 0.5,
  "delta_erro": -0.2,
  "temp_externa": 25.3,
  "carga_termica": 42.0,
  "potencia_crac": 48.5
}
```

### 2. `datacenter/fuzzy/temp`
Valor do erro de temperatura:
```
0.5
```

### 3. `datacenter/fuzzy/alert`
Alertas críticos do sistema:
```json
{
  "level": "critical",
  "message": "Temperatura crítica alta: 27.2°C",
  "timestamp": 1701363892.123
}
```

## 🧪 Como Gerar Mensagens

### 1. Calcular Potência CRAC
Na interface web (http://localhost:3500):
- Preencha os campos de entrada
- Clique em "Calcular Potência CRAC"
- ✅ Mensagem enviada para `datacenter/fuzzy/control`

### 2. Gerar Alerta
Configure valores extremos:
- **Erro**: -5 (temperatura alta)
- Calcule
- ✅ Se temperatura ultrapassar limites, alerta será enviado

### 3. Simular 24h
- Execute a simulação de 24 horas
- ✅ 1440 mensagens serão enviadas (uma por minuto simulado)

## 🐛 Troubleshooting

### Erro: Connection refused
```bash
# Verifique se mosquitto está rodando
sudo systemctl status mosquitto

# Se não estiver, inicie:
sudo systemctl start mosquitto
```

### Erro: Address already in use
✅ Isso é normal! Significa que o mosquitto já está rodando.

### Não recebo mensagens
1. Certifique-se de que o subscriber está rodando ANTES de fazer cálculos
2. Verifique se o app.py está conectado (deve mostrar "✅ MQTT conectado")
3. Tente fazer um cálculo manual na interface web

## 📈 Exemplo de Uso Completo

### Terminal 1: Servidor Flask
```bash
source venv/bin/activate
python app.py
```

### Terminal 2: MQTT Subscriber
```bash
source venv/bin/activate
python mqtt_subscriber.py
```

### Navegador:
1. Abra http://localhost:3500
2. Preencha:
   - Erro: -2
   - Delta Erro: -0.5
   - Temp Externa: 28
   - Carga Térmica: 60
3. Clique "Calcular"
4. **Veja a mensagem aparecer no Terminal 2!** 🎉

## 🎓 Dicas

- **Deixe o subscriber rodando** durante testes para ver todas as mensagens
- Use a **simulação de 24h** para gerar muitos dados rapidamente
- Os **alertas** só aparecem quando há condições críticas (temp < 18°C ou > 26°C)
- Você pode ter **múltiplos subscribers** rodando simultaneamente

## 📚 Recursos

- Documentação Mosquitto: https://mosquitto.org/documentation/
- Paho MQTT Python: https://www.eclipse.org/paho/
- MQTT Protocol: https://mqtt.org/
