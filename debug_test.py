#!/usr/bin/env python3
"""Debug específico para teste 8 - Condições Extremas"""

import sys
sys.path.insert(0, '.')

from fuzzy_controler.fuzzy_engine import FuzzyController

def debug_extreme_case():
    """Debugar caso extremo que está falhando"""
    
    print("=" * 70)
    print("🔍 DEBUG: Condições Extremas (Teste 8)")
    print("=" * 70)
    
    fuzzy = FuzzyController()
    
    # Teste 8: Condições Extremas
    erro = 4.0  # Temperatura alta
    delta_erro = -1.5  # Aumentando
    temp_externa = 35.0  # Máxima
    carga_termica = 100.0  # Máxima
    
    print(f"\n📥 ENTRADAS:")
    print(f"   Erro: {erro:+.1f}°C (temp 4°C acima do setpoint)")
    print(f"   Delta Erro: {delta_erro:+.1f}°C (erro aumentando)")
    print(f"   Temperatura Externa: {temp_externa:.1f}°C (máxima)")
    print(f"   Carga Térmica: {carga_termica:.1f}% (máxima)")
    
    # Fuzzificação manual
    print(f"\n🔢 FUZZIFICAÇÃO:")
    
    # Erro
    print(f"\n   ERRO ({erro:+.1f}°C):")
    for term in fuzzy.mf.erro_terms:
        membership = fuzzy.mf.get_membership('erro', term, erro)
        if membership > 0:
            print(f"      {term}: {membership:.3f}")
    
    # Delta Erro
    print(f"\n   DELTA ERRO ({delta_erro:+.1f}°C):")
    for term in fuzzy.mf.delta_erro_terms:
        membership = fuzzy.mf.get_membership('delta_erro', term, delta_erro)
        if membership > 0:
            print(f"      {term}: {membership:.3f}")
    
    # Temp Externa
    print(f"\n   TEMP EXTERNA ({temp_externa:.1f}°C):")
    for term in fuzzy.mf.temp_externa_terms:
        membership = fuzzy.mf.get_membership('temp_externa', term, temp_externa)
        if membership > 0:
            print(f"      {term}: {membership:.3f}")
    
    # Carga
    print(f"\n   CARGA TÉRMICA ({carga_termica:.1f}%):")
    for term in fuzzy.mf.carga_termica_terms:
        membership = fuzzy.mf.get_membership('carga_termica', term, carga_termica)
        if membership > 0:
            print(f"      {term}: {membership:.3f}")
    
    # Calcula e mostra detalhes
    potencia = fuzzy.calculate(erro, delta_erro, temp_externa, carga_termica)
    details = fuzzy.get_inference_details()
    
    print(f"\n⚙️  REGRAS ATIVAS:")
    if 'rules_fired' in details:
        for i, rule in enumerate(details['rules_fired'][:10], 1):  # Top 10
            print(f"\n   Regra {i}:")
            print(f"      IF erro={rule['conditions']['erro']} AND delta_erro={rule['conditions']['delta_erro']}")
            print(f"         temp_externa={rule['conditions']['temp_externa']} AND carga={rule['conditions']['carga_termica']}")
            print(f"      THEN potencia_crac={rule['conclusion']}")
            print(f"      Ativação: {rule['activation']:.3f}")
    
    print(f"\n📊 AGREGAÇÃO DE SAÍDA:")
    if 'output_aggregation' in details:
        for term, value in details['output_aggregation'].items():
            if value > 0:
                print(f"      {term}: {value:.3f}")
    
    print(f"\n📤 RESULTADO FINAL:")
    print(f"   Potência CRAC: {potencia:.2f}%")
    print(f"   Esperado: 80-100%")
    print(f"   Status: {'✅ OK' if 80 <= potencia <= 100 else '❌ FALHOU'}")
    
    # Análise
    print(f"\n🔬 ANÁLISE:")
    if potencia < 80:
        print(f"   ⚠️  Potência muito baixa para condições extremas!")
        print(f"   Possíveis causas:")
        print(f"   1. Erro {erro}°C não está ativando PM/PB fortemente")
        print(f"   2. Regras PM/PB não estão mapeando para MA corretamente")
        print(f"   3. Defuzzificação pode estar sendo dominada por regras de média potência")
    
    print(f"\n{'=' * 70}\n")

if __name__ == '__main__':
    debug_extreme_case()
