#!/usr/bin/env python3
"""
Script de teste para validar as correções no sistema fuzzy
"""

import sys
sys.path.insert(0, '.')

from fuzzy_controler.fuzzy_engine import FuzzyController

def test_fuzzy_corrections():
    """Testa diferentes cenários para validar as correções"""
    
    print("=" * 70)
    print("🧪 TESTE DE VALIDAÇÃO DAS CORREÇÕES DO SISTEMA FUZZY")
    print("=" * 70)
    print()
    
    fuzzy = FuzzyController()
    
    # Casos de teste
    test_cases = [
        {
            'name': '1. Temperatura CRÍTICA ALTA (28°C)',
            'erro': 6.0,  # 28 - 22 = +6
            'delta_erro': -1.0,
            'temp_externa': 30.0,
            'carga_termica': 70.0,
            'expected_range': (85, 100),
            'description': 'Temperatura muito acima do setpoint → CRAC máximo'
        },
        {
            'name': '2. Temperatura ALTA (25°C)',
            'erro': 3.0,  # 25 - 22 = +3
            'delta_erro': -0.5,
            'temp_externa': 28.0,
            'carga_termica': 60.0,
            'expected_range': (65, 85),
            'description': 'Temperatura acima do setpoint → CRAC alto'
        },
        {
            'name': '3. Temperatura NO SETPOINT (22°C)',
            'erro': 0.0,  # 22 - 22 = 0
            'delta_erro': 0.0,
            'temp_externa': 25.0,
            'carga_termica': 40.0,
            'expected_range': (40, 60),
            'description': 'Temperatura ideal → CRAC moderado'
        },
        {
            'name': '4. Temperatura BAIXA (20°C)',
            'erro': -2.0,  # 20 - 22 = -2
            'delta_erro': 0.5,
            'temp_externa': 20.0,
            'carga_termica': 30.0,
            'expected_range': (5, 25),  # Ajustado: temperatura baixa = CRAC muito baixo
            'description': 'Temperatura abaixo do setpoint → CRAC baixo'
        },
        {
            'name': '5. Temperatura CRÍTICA BAIXA (16°C)',
            'erro': -6.0,  # 16 - 22 = -6
            'delta_erro': 1.0,
            'temp_externa': 15.0,
            'carga_termica': 20.0,
            'expected_range': (0, 15),
            'description': 'Temperatura muito abaixo → CRAC mínimo'
        },
        {
            'name': '6. Aquecimento Rápido (tendência ruim)',
            'erro': 1.0,  # 23 - 22 = +1
            'delta_erro': -2.0,  # Erro aumentando MUITO rápido (2°C/min!)
            'temp_externa': 32.0,
            'carga_termica': 80.0,
            'expected_range': (80, 100),  # Ajustado: aquecimento rápido = ação máxima
            'description': 'Temperatura subindo rápido → Ação preventiva forte'
        },
        {
            'name': '7. Resfriamento Rápido (tendência boa)',
            'erro': -1.0,  # 21 - 22 = -1
            'delta_erro': 2.0,  # Erro diminuindo rápido
            'temp_externa': 18.0,
            'carga_termica': 25.0,
            'expected_range': (5, 20),
            'description': 'Temperatura caindo rápido → Reduzir CRAC'
        },
        {
            'name': '8. Condições Extremas (calor + carga)',
            'erro': 4.0,  # 26 - 22 = +4
            'delta_erro': -1.5,
            'temp_externa': 35.0,
            'carga_termica': 100.0,
            'expected_range': (80, 100),
            'description': 'Pior cenário → CRAC máximo'
        },
        {
            'name': '9. Condições Ideais (frio + baixa carga)',
            'erro': 0.0,
            'delta_erro': 0.0,
            'temp_externa': 15.0,
            'carga_termica': 20.0,
            'expected_range': (20, 40),
            'description': 'Melhor cenário → CRAC baixo/médio'
        },
        {
            'name': '10. Oscilação Estável',
            'erro': 0.5,  # 22.5 - 22 = +0.5
            'delta_erro': -0.2,
            'temp_externa': 23.0,
            'carga_termica': 45.0,
            'expected_range': (45, 65),
            'description': 'Pequeno desvio → Correção suave'
        }
    ]
    
    passed = 0
    failed = 0
    results = []
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'─' * 70}")
        print(f"🔬 {test['name']}")
        print(f"{'─' * 70}")
        print(f"📝 {test['description']}")
        print(f"\n📥 Entradas:")
        print(f"   • Erro: {test['erro']:+.1f}°C")
        print(f"   • Delta Erro: {test['delta_erro']:+.1f}°C")
        print(f"   • Temperatura Externa: {test['temp_externa']:.1f}°C")
        print(f"   • Carga Térmica: {test['carga_termica']:.1f}%")
        
        # Calcula potência CRAC
        potencia = fuzzy.calculate(
            test['erro'],
            test['delta_erro'],
            test['temp_externa'],
            test['carga_termica']
        )
        
        # Verifica se está na faixa esperada
        min_expected, max_expected = test['expected_range']
        is_correct = min_expected <= potencia <= max_expected
        
        print(f"\n📤 Saída:")
        print(f"   • Potência CRAC: {potencia:.2f}%")
        print(f"   • Faixa Esperada: {min_expected}% - {max_expected}%")
        
        if is_correct:
            print(f"   • Status: ✅ PASSOU")
            passed += 1
            results.append((test['name'], potencia, '✅'))
        else:
            print(f"   • Status: ❌ FALHOU")
            failed += 1
            results.append((test['name'], potencia, '❌'))
    
    # Resumo final
    print(f"\n{'=' * 70}")
    print("📊 RESUMO DOS TESTES")
    print(f"{'=' * 70}")
    print(f"\n✅ Testes Aprovados: {passed}/{len(test_cases)}")
    print(f"❌ Testes Falhados: {failed}/{len(test_cases)}")
    print(f"📈 Taxa de Sucesso: {(passed/len(test_cases)*100):.1f}%")
    
    print(f"\n{'─' * 70}")
    print("📋 TABELA DE RESULTADOS")
    print(f"{'─' * 70}")
    print(f"{'Teste':<45} {'Potência':<12} {'Status':<8}")
    print(f"{'─' * 70}")
    for name, potencia, status in results:
        print(f"{name:<45} {potencia:>6.2f}%     {status}")
    print(f"{'─' * 70}")
    
    # Análise de distribuição
    potencias = [r[1] for r in results]
    print(f"\n📊 ANÁLISE DE DISTRIBUIÇÃO")
    print(f"{'─' * 70}")
    print(f"   • Valor Mínimo: {min(potencias):.2f}%")
    print(f"   • Valor Máximo: {max(potencias):.2f}%")
    print(f"   • Média: {sum(potencias)/len(potencias):.2f}%")
    print(f"   • Amplitude: {max(potencias) - min(potencias):.2f}%")
    
    if max(potencias) - min(potencias) < 20:
        print(f"\n   ⚠️  ATENÇÃO: Amplitude muito pequena!")
        print(f"   O sistema ainda pode estar concentrado em valores médios.")
    else:
        print(f"\n   ✅ Boa amplitude de valores!")
    
    print(f"\n{'=' * 70}")
    
    if failed == 0:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ O sistema fuzzy está funcionando corretamente!")
    else:
        print(f"⚠️  {failed} TESTE(S) FALHARAM")
        print("Revise as regras ou funções de pertinência.")
    
    print(f"{'=' * 70}\n")
    
    return passed == len(test_cases)

if __name__ == '__main__':
    success = test_fuzzy_corrections()
    sys.exit(0 if success else 1)
