#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste de valores extremos no controlador fuzzy
"""

import sys
sys.path.append('.')

from fuzzy_controler.fuzzy_engine import FuzzyController

# Cria controlador
controller = FuzzyController()

print("="*60)
print("TESTE DE VALORES EXTREMOS")
print("="*60)

# Teste 1: Erro 100°C, Carga 100%
print("\n🔥 TESTE 1: Erro 100°C, Carga Térmica 100%")
print("-" * 60)
erro = 100.0
delta_erro = 0.0
temp_externa = 35.0
carga_termica = 100.0

print(f"Entradas:")
print(f"  - Erro: {erro}°C")
print(f"  - Delta Erro: {delta_erro}")
print(f"  - Temp Externa: {temp_externa}°C")
print(f"  - Carga Térmica: {carga_termica}%")

potencia = controller.calculate(erro, delta_erro, temp_externa, carga_termica)
print(f"\n🎯 Potência CRAC: {potencia:.2f}%")
print(f"❌ ESPERADO: ~95-100%")
print(f"❌ RESULTADO: {potencia:.2f}%")

# Verifica fuzzificação
print("\n📊 Fuzzificação do ERRO (100°C):")
mf = controller.mf
for term, func in mf.erro_mf.items():
    membership = func(erro)
    if membership > 0:
        print(f"  {term}: {membership:.4f}")

print("\n📊 Fuzzificação da CARGA (100%):")
for term, func in mf.carga_termica_mf.items():
    membership = func(carga_termica)
    if membership > 0:
        print(f"  {term}: {membership:.4f}")

# Teste 2: Erro 10°C (no limite)
print("\n" + "="*60)
print("🔥 TESTE 2: Erro 10°C (Limite Superior Atual)")
print("-" * 60)
erro = 10.0
potencia = controller.calculate(erro, 0.0, temp_externa, carga_termica)
print(f"Erro: {erro}°C → Potência CRAC: {potencia:.2f}%")

# Teste 3: Erro 5°C
print("\n🔥 TESTE 3: Erro 5°C")
print("-" * 60)
erro = 5.0
potencia = controller.calculate(erro, 0.0, temp_externa, carga_termica)
print(f"Erro: {erro}°C → Potência CRAC: {potencia:.2f}%")

print("\n" + "="*60)
print("🔍 DIAGNÓSTICO:")
print("="*60)
print("❌ PROBLEMA IDENTIFICADO:")
print("   - Função de pertinência do ERRO só vai até ±10°C")
print("   - Valores > 10°C não são mapeados corretamente")
print("   - Resultado: saída default ~50%")
print("\n✅ SOLUÇÃO:")
print("   - Estender ranges das funções de pertinência")
print("   - OU saturar valores extremos no limite superior")
print("="*60)
