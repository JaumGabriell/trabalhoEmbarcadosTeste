# 🔧 Guia de Solução de Problemas

## 🚨 MQTT Desconectado

### Problema: Dashboard mostra "Desconectado (Modo Simulação)"

#### ✅ Solução 1: Verificar se Mosquitto está rodando

```bash
# Verificar status
systemctl status mosquitto

# Se não estiver rodando, iniciar
sudo systemctl start mosquitto

# Para iniciar automaticamente no boot
sudo systemctl enable mosquitto
```

#### ✅ Solução 2: Reiniciar o servidor Flask

Depois de iniciar o mosquitto:
```bash
# Parar servidor (Ctrl+C no terminal)
# Depois iniciar novamente
python app.py
```

Você deve ver:
```
🟢 MQTT conectado ao broker localhost:1883
```

#### ✅ Solução 3: Verificar firewall

```bash
# Permitir porta 1883
sudo ufw allow 1883
```

## 🐛 Erros de Simulação

### Problema: Simulação demora muito ou trava

**Causa:** Simulação está processando 1440 pontos

**Solução:** A versão otimizada já reduz para ~289 pontos (5x mais rápido)

Se ainda estiver lento:
- Aguarde 10-30 segundos
- Verifique progresso no terminal do servidor
- Não clique novamente enquanto processa

## 📊 Gráficos não aparecem

### Problema: Gráficos em branco ou erro de Chart.js

**Solução:**
```bash
# Limpar cache do navegador
Ctrl+Shift+R (Linux/Windows)
Cmd+Shift+R (Mac)
```

## 🔌 Porta em uso

### Problema: "Address already in use" na porta 3500

**Solução:**
```bash
# Encontrar processo usando a porta
sudo lsof -i :3500

# Matar o processo (substitua PID)
kill -9 PID

# Ou usar outra porta (editar app.py linha 219)
```

## 📡 MQTT Subscriber não recebe mensagens

### Checklist:

1. ✅ Mosquitto está rodando?
   ```bash
   systemctl status mosquitto
   ```

2. ✅ Servidor Flask está conectado?
   - Deve mostrar "🟢 MQTT conectado" ao iniciar

3. ✅ Subscriber está rodando?
   ```bash
   python mqtt_subscriber.py
   ```

4. ✅ Você fez algum cálculo na interface?
   - Mensagens só são enviadas quando você calcula!

## 🌐 Interface não carrega

### Problema: Página não abre em http://localhost:3500

**Soluções:**

1. Verificar se servidor está rodando
   ```bash
   # Deve mostrar "Running on http://127.0.0.1:3500"
   ```

2. Tentar IP da máquina
   ```bash
   # O servidor mostra: "Running on http://192.168.0.XXX:3500"
   # Use esse endereço
   ```

3. Verificar logs de erro no terminal

## 📦 Erros de Importação

### Problema: ModuleNotFoundError

**Solução:**
```bash
# Ativar ambiente virtual
source venv/bin/activate

# Reinstalar dependências
pip install -r requirements.txt
```

## 💾 Problemas com numpy/scipy

### Problema: Erros ao calcular (numpy errors)

**Solução:**
```bash
# Reinstalar pacotes científicos
pip uninstall numpy scipy matplotlib
pip install numpy==1.24.3 scipy==1.11.1 matplotlib==3.7.1
```

## 🔄 Reset Completo

Se tudo mais falhar:

```bash
# 1. Parar todos os processos
Ctrl+C em todos os terminais

# 2. Parar mosquitto
sudo systemctl stop mosquitto

# 3. Limpar cache Python
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# 4. Recriar ambiente virtual
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 5. Iniciar mosquitto
sudo systemctl start mosquitto

# 6. Rodar aplicação
python app.py
```

## 📞 Suporte Adicional

Se o problema persistir:

1. ✅ Verifique logs do terminal
2. ✅ Abra console do navegador (F12)
3. ✅ Verifique GUIA_MQTT.md para detalhes MQTT
4. ✅ Verifique README.md para instruções completas

## ⚡ Dicas de Performance

- Use Firefox ou Chrome (melhor suporte a Chart.js)
- Feche abas não utilizadas
- A simulação é processamento intensivo, aguarde completar
- MQTT local é muito mais rápido que broker remoto
