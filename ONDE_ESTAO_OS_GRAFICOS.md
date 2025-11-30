# 📍 Onde Estão os 4 Gráficos da Simulação?

## 🎯 Localização

Os **4 gráficos** estão na seção **"🕐 Simulação de 24 Horas"** da página principal.

### ⚠️ IMPORTANTE: Os gráficos só aparecem DEPOIS de executar a simulação!

---

## 📊 Como Visualizar os Gráficos

### Passo 1: Acesse a Página Principal
```
http://localhost:5500
```

### Passo 2: Role até a Seção "Simulação de 24 Horas"
- Você verá um **preview visual** dos 4 gráficos
- Cards com ícones mostrando:
  - 📊 Temperatura Atual vs Setpoint
  - ❄️ Potência de Refrigeração (PCRAC)
  - 📈 Erro de Temperatura
  - 🌡️ Temperatura de Saída

### Passo 3: Configure os Parâmetros (opcional)
- **Temperatura Inicial:** 22°C (padrão)
- **Temp. Externa Base:** 25°C (padrão)
- **Carga Base:** 40% (padrão)

### Passo 4: Clique em "▶️ Executar Simulação"
- Aguarde 20-30 segundos
- O preview desaparece
- Os **4 gráficos reais** aparecem!

---

## 📈 Os 4 Gráficos que Aparecem

### 1️⃣ 📊 Temperatura Atual vs Setpoint
**Cores:**
- 🔴 Vermelho: Temperatura Real
- 🟢 Verde (linha tracejada): Setpoint 22°C

**O que mostra:**
- Como a temperatura varia ao longo de 24h
- Se está mantendo próximo do setpoint

---

### 2️⃣ ❄️ Potência de Refrigeração (PCRAC)
**Cor:**
- 🔵 Azul

**O que mostra:**
- % de potência do CRAC ao longo do tempo
- Varia de 0% a 100%
- Mostra quando precisa mais/menos refrigeração

---

### 3️⃣ 📈 Erro de Temperatura (T_atual - Setpoint)
**Cor:**
- 🟠 Laranja

**O que mostra:**
- Diferença entre temperatura real e setpoint
- Erro positivo = temp acima
- Erro negativo = temp abaixo
- Ideal: próximo de 0

---

### 4️⃣ 🌡️ Temperatura de Saída ao Longo do Tempo
**Cor:**
- 🟣 Roxo

**O que mostra:**
- Temperatura do sistema ao longo de 24h
- Deve ficar entre 20-24°C
- Mostra comportamento temporal do sistema

---

## 🖼️ Layout dos Gráficos

```
┌─────────────────────────┬─────────────────────────┐
│                         │                         │
│  📊 Temp vs Setpoint   │  ❄️ Potência CRAC      │
│  (Vermelho + Verde)     │  (Azul)                 │
│                         │                         │
├─────────────────────────┼─────────────────────────┤
│                         │                         │
│  📈 Erro de Temp       │  🌡️ Temp de Saída      │
│  (Laranja)              │  (Roxo)                 │
│                         │                         │
└─────────────────────────┴─────────────────────────┘
```

**No mobile:** Fica 1 coluna (um embaixo do outro)

---

## ❓ Problemas Comuns

### "Não vejo os gráficos!"
✅ **Solução:** Clique em "▶️ Executar Simulação" primeiro!

### "O preview não desaparece!"
✅ **Solução:** Aguarde a simulação terminar (~20-30s)

### "Página em branco depois de clicar!"
✅ **Solução:** 
1. Verifique o console do navegador (F12)
2. Verifique o terminal do servidor
3. Recarregue a página (Ctrl+Shift+R)

### "Erro 500 ou timeout!"
✅ **Solução:**
1. Certifique-se que o servidor está rodando
2. A simulação demora ~20-30s mesmo
3. Acompanhe o progresso no terminal

---

## 🔍 Verificação Rápida

### Antes de Executar a Simulação:
```
✅ Preview visual dos 4 gráficos
✅ Mensagem: "Clique em Executar Simulação para visualizar"
❌ Gráficos reais NÃO aparecem
```

### Durante a Simulação:
```
⏳ Loading spinner
⏳ Mensagem: "Simulando 1440 minutos..."
⏳ Preview desapareceu
❌ Gráficos ainda não aparecem (processando...)
```

### Depois da Simulação:
```
✅ 4 métricas (RMSE, Tempo em Faixa, etc.)
✅ 4 gráficos completos e interativos
✅ Dados de 24 horas plotados
❌ Preview NÃO volta mais
```

---

## 🎓 Teste Agora!

```bash
# 1. Inicie o servidor (se não estiver rodando)
python app.py

# 2. Acesse
http://localhost:5500

# 3. Role até "Simulação de 24 Horas"

# 4. Clique em "▶️ Executar Simulação"

# 5. Aguarde 20-30 segundos

# 6. BOOM! 🎉 Os 4 gráficos aparecem!
```

---

## 📝 Resumo

| Item | Status | Como Ver |
|------|--------|----------|
| **Preview dos Gráficos** | ✅ Sempre visível | Role até seção de simulação |
| **Gráficos Reais** | ⏳ Só após simulação | Clique em "Executar Simulação" |
| **Métricas (RMSE, etc.)** | ⏳ Só após simulação | Aparecem junto com gráficos |
| **Processo de Inferência** | ❌ Removido | Substituído pelos gráficos |

---

**✨ Os gráficos ESTÃO LÁ, só precisa executar a simulação!** ✨
