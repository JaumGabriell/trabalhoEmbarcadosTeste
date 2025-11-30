class FuzzyRules:
    """
    Base de regras fuzzy para controle de refrigeração
    Tipo: Mamdani
    Estrutura: IF-THEN com 4 antecedentes e 1 consequente
    """
    
    def __init__(self):
        self.rules_base = self._create_rules_base()
    
    def _create_rules_base(self):
        """
        Cria a base de regras fuzzy completa
        
        Lógica de controle:
        - Erro positivo (temp < setpoint) -> Reduzir potência CRAC
        - Erro negativo (temp > setpoint) -> Aumentar potência CRAC
        - Delta_erro positivo (erro crescendo) -> Ação preventiva
        - Temperatura externa alta -> Aumentar potência
        - Carga térmica alta -> Aumentar potência
        """
        rules = []
        
        # === REGRAS CRÍTICAS - TEMPERATURA MUITO ALTA (Erro Negativo Grande) ===
        # Temp muito acima do setpoint - REFRIGERAÇÃO MÁXIMA
        
        rules.extend([
            # Erro NB (temp muito alta), qualquer tendência -> Potência MÁXIMA
            {'erro': 'NB', 'delta_erro': 'NB', 'temp_externa': 'Baixa', 'carga_termica': 'Baixa', 'potencia_crac': 'MA'},
            {'erro': 'NB', 'delta_erro': 'NB', 'temp_externa': 'Baixa', 'carga_termica': 'Media', 'potencia_crac': 'MA'},
            {'erro': 'NB', 'delta_erro': 'NB', 'temp_externa': 'Baixa', 'carga_termica': 'Alta', 'potencia_crac': 'MA'},
            {'erro': 'NB', 'delta_erro': 'NB', 'temp_externa': 'Media', 'carga_termica': 'Baixa', 'potencia_crac': 'MA'},
            {'erro': 'NB', 'delta_erro': 'NB', 'temp_externa': 'Media', 'carga_termica': 'Media', 'potencia_crac': 'MA'},
            {'erro': 'NB', 'delta_erro': 'NB', 'temp_externa': 'Media', 'carga_termica': 'Alta', 'potencia_crac': 'MA'},
            {'erro': 'NB', 'delta_erro': 'NB', 'temp_externa': 'Alta', 'carga_termica': 'Baixa', 'potencia_crac': 'MA'},
            {'erro': 'NB', 'delta_erro': 'NB', 'temp_externa': 'Alta', 'carga_termica': 'Media', 'potencia_crac': 'MA'},
            {'erro': 'NB', 'delta_erro': 'NB', 'temp_externa': 'Alta', 'carga_termica': 'Alta', 'potencia_crac': 'MA'},
            
            {'erro': 'NB', 'delta_erro': 'NM', 'temp_externa': 'Baixa', 'carga_termica': 'Baixa', 'potencia_crac': 'MA'},
            {'erro': 'NB', 'delta_erro': 'NM', 'temp_externa': 'Baixa', 'carga_termica': 'Media', 'potencia_crac': 'MA'},
            {'erro': 'NB', 'delta_erro': 'NM', 'temp_externa': 'Baixa', 'carga_termica': 'Alta', 'potencia_crac': 'MA'},
            {'erro': 'NB', 'delta_erro': 'NM', 'temp_externa': 'Media', 'carga_termica': 'Baixa', 'potencia_crac': 'MA'},
            {'erro': 'NB', 'delta_erro': 'NM', 'temp_externa': 'Media', 'carga_termica': 'Media', 'potencia_crac': 'MA'},
            {'erro': 'NB', 'delta_erro': 'NM', 'temp_externa': 'Media', 'carga_termica': 'Alta', 'potencia_crac': 'MA'},
            {'erro': 'NB', 'delta_erro': 'NM', 'temp_externa': 'Alta', 'carga_termica': 'Baixa', 'potencia_crac': 'MA'},
            {'erro': 'NB', 'delta_erro': 'NM', 'temp_externa': 'Alta', 'carga_termica': 'Media', 'potencia_crac': 'MA'},
            {'erro': 'NB', 'delta_erro': 'NM', 'temp_externa': 'Alta', 'carga_termica': 'Alta', 'potencia_crac': 'MA'},
            
            {'erro': 'NB', 'delta_erro': 'NS', 'temp_externa': 'Baixa', 'carga_termica': 'Baixa', 'potencia_crac': 'MA'},
            {'erro': 'NB', 'delta_erro': 'NS', 'temp_externa': 'Baixa', 'carga_termica': 'Media', 'potencia_crac': 'MA'},
            {'erro': 'NB', 'delta_erro': 'NS', 'temp_externa': 'Baixa', 'carga_termica': 'Alta', 'potencia_crac': 'MA'},
            {'erro': 'NB', 'delta_erro': 'NS', 'temp_externa': 'Media', 'carga_termica': 'Baixa', 'potencia_crac': 'MA'},
            {'erro': 'NB', 'delta_erro': 'NS', 'temp_externa': 'Media', 'carga_termica': 'Media', 'potencia_crac': 'MA'},
            {'erro': 'NB', 'delta_erro': 'NS', 'temp_externa': 'Media', 'carga_termica': 'Alta', 'potencia_crac': 'MA'},
            {'erro': 'NB', 'delta_erro': 'NS', 'temp_externa': 'Alta', 'carga_termica': 'Baixa', 'potencia_crac': 'MA'},
            {'erro': 'NB', 'delta_erro': 'NS', 'temp_externa': 'Alta', 'carga_termica': 'Media', 'potencia_crac': 'MA'},
            {'erro': 'NB', 'delta_erro': 'NS', 'temp_externa': 'Alta', 'carga_termica': 'Alta', 'potencia_crac': 'MA'},
            
            {'erro': 'NB', 'delta_erro': 'ZE', 'temp_externa': 'Baixa', 'carga_termica': 'Baixa', 'potencia_crac': 'A'},
            {'erro': 'NB', 'delta_erro': 'ZE', 'temp_externa': 'Baixa', 'carga_termica': 'Media', 'potencia_crac': 'MA'},
            {'erro': 'NB', 'delta_erro': 'ZE', 'temp_externa': 'Baixa', 'carga_termica': 'Alta', 'potencia_crac': 'MA'},
            {'erro': 'NB', 'delta_erro': 'ZE', 'temp_externa': 'Media', 'carga_termica': 'Baixa', 'potencia_crac': 'MA'},
            {'erro': 'NB', 'delta_erro': 'ZE', 'temp_externa': 'Media', 'carga_termica': 'Media', 'potencia_crac': 'MA'},
            {'erro': 'NB', 'delta_erro': 'ZE', 'temp_externa': 'Media', 'carga_termica': 'Alta', 'potencia_crac': 'MA'},
            {'erro': 'NB', 'delta_erro': 'ZE', 'temp_externa': 'Alta', 'carga_termica': 'Baixa', 'potencia_crac': 'MA'},
            {'erro': 'NB', 'delta_erro': 'ZE', 'temp_externa': 'Alta', 'carga_termica': 'Media', 'potencia_crac': 'MA'},
            {'erro': 'NB', 'delta_erro': 'ZE', 'temp_externa': 'Alta', 'carga_termica': 'Alta', 'potencia_crac': 'MA'},
        ])
        
        # === REGRAS PARA ERRO NEGATIVO MÉDIO ===
        # Temp acima do setpoint - Potência ALTA
        rules.extend([
            {'erro': 'NM', 'delta_erro': 'NB', 'temp_externa': 'Baixa', 'carga_termica': 'Baixa', 'potencia_crac': 'A'},
            {'erro': 'NM', 'delta_erro': 'NB', 'temp_externa': 'Baixa', 'carga_termica': 'Media', 'potencia_crac': 'MA'},
            {'erro': 'NM', 'delta_erro': 'NB', 'temp_externa': 'Baixa', 'carga_termica': 'Alta', 'potencia_crac': 'MA'},
            {'erro': 'NM', 'delta_erro': 'NB', 'temp_externa': 'Media', 'carga_termica': 'Baixa', 'potencia_crac': 'A'},
            {'erro': 'NM', 'delta_erro': 'NB', 'temp_externa': 'Media', 'carga_termica': 'Media', 'potencia_crac': 'MA'},
            {'erro': 'NM', 'delta_erro': 'NB', 'temp_externa': 'Media', 'carga_termica': 'Alta', 'potencia_crac': 'MA'},
            {'erro': 'NM', 'delta_erro': 'NB', 'temp_externa': 'Alta', 'carga_termica': 'Baixa', 'potencia_crac': 'MA'},
            {'erro': 'NM', 'delta_erro': 'NB', 'temp_externa': 'Alta', 'carga_termica': 'Media', 'potencia_crac': 'MA'},
            {'erro': 'NM', 'delta_erro': 'NB', 'temp_externa': 'Alta', 'carga_termica': 'Alta', 'potencia_crac': 'MA'},
            
            {'erro': 'NM', 'delta_erro': 'NM', 'temp_externa': 'Baixa', 'carga_termica': 'Baixa', 'potencia_crac': 'A'},
            {'erro': 'NM', 'delta_erro': 'NM', 'temp_externa': 'Baixa', 'carga_termica': 'Media', 'potencia_crac': 'A'},
            {'erro': 'NM', 'delta_erro': 'NM', 'temp_externa': 'Baixa', 'carga_termica': 'Alta', 'potencia_crac': 'MA'},
            {'erro': 'NM', 'delta_erro': 'NM', 'temp_externa': 'Media', 'carga_termica': 'Baixa', 'potencia_crac': 'A'},
            {'erro': 'NM', 'delta_erro': 'NM', 'temp_externa': 'Media', 'carga_termica': 'Media', 'potencia_crac': 'A'},
            {'erro': 'NM', 'delta_erro': 'NM', 'temp_externa': 'Media', 'carga_termica': 'Alta', 'potencia_crac': 'MA'},
            {'erro': 'NM', 'delta_erro': 'NM', 'temp_externa': 'Alta', 'carga_termica': 'Baixa', 'potencia_crac': 'A'},
            {'erro': 'NM', 'delta_erro': 'NM', 'temp_externa': 'Alta', 'carga_termica': 'Media', 'potencia_crac': 'MA'},
            {'erro': 'NM', 'delta_erro': 'NM', 'temp_externa': 'Alta', 'carga_termica': 'Alta', 'potencia_crac': 'MA'},
            
            {'erro': 'NM', 'delta_erro': 'NS', 'temp_externa': 'Baixa', 'carga_termica': 'Baixa', 'potencia_crac': 'M'},
            {'erro': 'NM', 'delta_erro': 'NS', 'temp_externa': 'Baixa', 'carga_termica': 'Media', 'potencia_crac': 'A'},
            {'erro': 'NM', 'delta_erro': 'NS', 'temp_externa': 'Baixa', 'carga_termica': 'Alta', 'potencia_crac': 'A'},
            {'erro': 'NM', 'delta_erro': 'NS', 'temp_externa': 'Media', 'carga_termica': 'Baixa', 'potencia_crac': 'A'},
            {'erro': 'NM', 'delta_erro': 'NS', 'temp_externa': 'Media', 'carga_termica': 'Media', 'potencia_crac': 'A'},
            {'erro': 'NM', 'delta_erro': 'NS', 'temp_externa': 'Media', 'carga_termica': 'Alta', 'potencia_crac': 'MA'},
            {'erro': 'NM', 'delta_erro': 'NS', 'temp_externa': 'Alta', 'carga_termica': 'Baixa', 'potencia_crac': 'A'},
            {'erro': 'NM', 'delta_erro': 'NS', 'temp_externa': 'Alta', 'carga_termica': 'Media', 'potencia_crac': 'A'},
            {'erro': 'NM', 'delta_erro': 'NS', 'temp_externa': 'Alta', 'carga_termica': 'Alta', 'potencia_crac': 'MA'},
            
            {'erro': 'NM', 'delta_erro': 'ZE', 'temp_externa': 'Baixa', 'carga_termica': 'Baixa', 'potencia_crac': 'M'},
            {'erro': 'NM', 'delta_erro': 'ZE', 'temp_externa': 'Baixa', 'carga_termica': 'Media', 'potencia_crac': 'A'},
            {'erro': 'NM', 'delta_erro': 'ZE', 'temp_externa': 'Baixa', 'carga_termica': 'Alta', 'potencia_crac': 'A'},
            {'erro': 'NM', 'delta_erro': 'ZE', 'temp_externa': 'Media', 'carga_termica': 'Baixa', 'potencia_crac': 'M'},
            {'erro': 'NM', 'delta_erro': 'ZE', 'temp_externa': 'Media', 'carga_termica': 'Media', 'potencia_crac': 'A'},
            {'erro': 'NM', 'delta_erro': 'ZE', 'temp_externa': 'Media', 'carga_termica': 'Alta', 'potencia_crac': 'A'},
            {'erro': 'NM', 'delta_erro': 'ZE', 'temp_externa': 'Alta', 'carga_termica': 'Baixa', 'potencia_crac': 'A'},
            {'erro': 'NM', 'delta_erro': 'ZE', 'temp_externa': 'Alta', 'carga_termica': 'Media', 'potencia_crac': 'A'},
            {'erro': 'NM', 'delta_erro': 'ZE', 'temp_externa': 'Alta', 'carga_termica': 'Alta', 'potencia_crac': 'MA'},
        ])
        
        # === REGRAS PARA ERRO NEGATIVO PEQUENO ===
        rules.extend([
            {'erro': 'NS', 'delta_erro': 'NB', 'temp_externa': 'Baixa', 'carga_termica': 'Baixa', 'potencia_crac': 'M'},
            {'erro': 'NS', 'delta_erro': 'NB', 'temp_externa': 'Baixa', 'carga_termica': 'Media', 'potencia_crac': 'A'},
            {'erro': 'NS', 'delta_erro': 'NB', 'temp_externa': 'Baixa', 'carga_termica': 'Alta', 'potencia_crac': 'A'},
            {'erro': 'NS', 'delta_erro': 'NB', 'temp_externa': 'Media', 'carga_termica': 'Baixa', 'potencia_crac': 'A'},
            {'erro': 'NS', 'delta_erro': 'NB', 'temp_externa': 'Media', 'carga_termica': 'Media', 'potencia_crac': 'A'},
            {'erro': 'NS', 'delta_erro': 'NB', 'temp_externa': 'Media', 'carga_termica': 'Alta', 'potencia_crac': 'MA'},
            {'erro': 'NS', 'delta_erro': 'NB', 'temp_externa': 'Alta', 'carga_termica': 'Baixa', 'potencia_crac': 'A'},
            {'erro': 'NS', 'delta_erro': 'NB', 'temp_externa': 'Alta', 'carga_termica': 'Media', 'potencia_crac': 'A'},
            {'erro': 'NS', 'delta_erro': 'NB', 'temp_externa': 'Alta', 'carga_termica': 'Alta', 'potencia_crac': 'MA'},
            
            {'erro': 'NS', 'delta_erro': 'NM', 'temp_externa': 'Baixa', 'carga_termica': 'Baixa', 'potencia_crac': 'M'},
            {'erro': 'NS', 'delta_erro': 'NM', 'temp_externa': 'Baixa', 'carga_termica': 'Media', 'potencia_crac': 'M'},
            {'erro': 'NS', 'delta_erro': 'NM', 'temp_externa': 'Baixa', 'carga_termica': 'Alta', 'potencia_crac': 'A'},
            {'erro': 'NS', 'delta_erro': 'NM', 'temp_externa': 'Media', 'carga_termica': 'Baixa', 'potencia_crac': 'M'},
            {'erro': 'NS', 'delta_erro': 'NM', 'temp_externa': 'Media', 'carga_termica': 'Media', 'potencia_crac': 'A'},
            {'erro': 'NS', 'delta_erro': 'NM', 'temp_externa': 'Media', 'carga_termica': 'Alta', 'potencia_crac': 'A'},
            {'erro': 'NS', 'delta_erro': 'NM', 'temp_externa': 'Alta', 'carga_termica': 'Baixa', 'potencia_crac': 'A'},
            {'erro': 'NS', 'delta_erro': 'NM', 'temp_externa': 'Alta', 'carga_termica': 'Media', 'potencia_crac': 'A'},
            {'erro': 'NS', 'delta_erro': 'NM', 'temp_externa': 'Alta', 'carga_termica': 'Alta', 'potencia_crac': 'MA'},
            
            {'erro': 'NS', 'delta_erro': 'NS', 'temp_externa': 'Baixa', 'carga_termica': 'Baixa', 'potencia_crac': 'M'},
            {'erro': 'NS', 'delta_erro': 'NS', 'temp_externa': 'Baixa', 'carga_termica': 'Media', 'potencia_crac': 'M'},
            {'erro': 'NS', 'delta_erro': 'NS', 'temp_externa': 'Baixa', 'carga_termica': 'Alta', 'potencia_crac': 'A'},
            {'erro': 'NS', 'delta_erro': 'NS', 'temp_externa': 'Media', 'carga_termica': 'Baixa', 'potencia_crac': 'M'},
            {'erro': 'NS', 'delta_erro': 'NS', 'temp_externa': 'Media', 'carga_termica': 'Media', 'potencia_crac': 'M'},
            {'erro': 'NS', 'delta_erro': 'NS', 'temp_externa': 'Media', 'carga_termica': 'Alta', 'potencia_crac': 'A'},
            {'erro': 'NS', 'delta_erro': 'NS', 'temp_externa': 'Alta', 'carga_termica': 'Baixa', 'potencia_crac': 'M'},
            {'erro': 'NS', 'delta_erro': 'NS', 'temp_externa': 'Alta', 'carga_termica': 'Media', 'potencia_crac': 'A'},
            {'erro': 'NS', 'delta_erro': 'NS', 'temp_externa': 'Alta', 'carga_termica': 'Alta', 'potencia_crac': 'A'},
            
            {'erro': 'NS', 'delta_erro': 'ZE', 'temp_externa': 'Baixa', 'carga_termica': 'Baixa', 'potencia_crac': 'M'},
            {'erro': 'NS', 'delta_erro': 'ZE', 'temp_externa': 'Baixa', 'carga_termica': 'Media', 'potencia_crac': 'M'},
            {'erro': 'NS', 'delta_erro': 'ZE', 'temp_externa': 'Baixa', 'carga_termica': 'Alta', 'potencia_crac': 'A'},
            {'erro': 'NS', 'delta_erro': 'ZE', 'temp_externa': 'Media', 'carga_termica': 'Baixa', 'potencia_crac': 'M'},
            {'erro': 'NS', 'delta_erro': 'ZE', 'temp_externa': 'Media', 'carga_termica': 'Media', 'potencia_crac': 'M'},
            {'erro': 'NS', 'delta_erro': 'ZE', 'temp_externa': 'Media', 'carga_termica': 'Alta', 'potencia_crac': 'A'},
            {'erro': 'NS', 'delta_erro': 'ZE', 'temp_externa': 'Alta', 'carga_termica': 'Baixa', 'potencia_crac': 'M'},
            {'erro': 'NS', 'delta_erro': 'ZE', 'temp_externa': 'Alta', 'carga_termica': 'Media', 'potencia_crac': 'A'},
            {'erro': 'NS', 'delta_erro': 'ZE', 'temp_externa': 'Alta', 'carga_termica': 'Alta', 'potencia_crac': 'A'},
            
            {'erro': 'NS', 'delta_erro': 'PS', 'temp_externa': 'Baixa', 'carga_termica': 'Baixa', 'potencia_crac': 'B'},
            {'erro': 'NS', 'delta_erro': 'PS', 'temp_externa': 'Baixa', 'carga_termica': 'Media', 'potencia_crac': 'M'},
            {'erro': 'NS', 'delta_erro': 'PS', 'temp_externa': 'Baixa', 'carga_termica': 'Alta', 'potencia_crac': 'M'},
            {'erro': 'NS', 'delta_erro': 'PS', 'temp_externa': 'Media', 'carga_termica': 'Baixa', 'potencia_crac': 'M'},
            {'erro': 'NS', 'delta_erro': 'PS', 'temp_externa': 'Media', 'carga_termica': 'Media', 'potencia_crac': 'M'},
            {'erro': 'NS', 'delta_erro': 'PS', 'temp_externa': 'Media', 'carga_termica': 'Alta', 'potencia_crac': 'A'},
            {'erro': 'NS', 'delta_erro': 'PS', 'temp_externa': 'Alta', 'carga_termica': 'Baixa', 'potencia_crac': 'M'},
            {'erro': 'NS', 'delta_erro': 'PS', 'temp_externa': 'Alta', 'carga_termica': 'Media', 'potencia_crac': 'M'},
            {'erro': 'NS', 'delta_erro': 'PS', 'temp_externa': 'Alta', 'carga_termica': 'Alta', 'potencia_crac': 'A'},
        ])
        
        # === REGRAS PARA ERRO ZERO ===
        # Sistema próximo ao setpoint
        rules.extend([
            {'erro': 'ZE', 'delta_erro': 'NB', 'temp_externa': 'Baixa', 'carga_termica': 'Baixa', 'potencia_crac': 'M'},
            {'erro': 'ZE', 'delta_erro': 'NB', 'temp_externa': 'Baixa', 'carga_termica': 'Media', 'potencia_crac': 'A'},
            {'erro': 'ZE', 'delta_erro': 'NB', 'temp_externa': 'Baixa', 'carga_termica': 'Alta', 'potencia_crac': 'A'},
            {'erro': 'ZE', 'delta_erro': 'NB', 'temp_externa': 'Media', 'carga_termica': 'Baixa', 'potencia_crac': 'M'},
            {'erro': 'ZE', 'delta_erro': 'NB', 'temp_externa': 'Media', 'carga_termica': 'Media', 'potencia_crac': 'A'},
            {'erro': 'ZE', 'delta_erro': 'NB', 'temp_externa': 'Media', 'carga_termica': 'Alta', 'potencia_crac': 'A'},
            {'erro': 'ZE', 'delta_erro': 'NB', 'temp_externa': 'Alta', 'carga_termica': 'Baixa', 'potencia_crac': 'A'},
            {'erro': 'ZE', 'delta_erro': 'NB', 'temp_externa': 'Alta', 'carga_termica': 'Media', 'potencia_crac': 'A'},
            {'erro': 'ZE', 'delta_erro': 'NB', 'temp_externa': 'Alta', 'carga_termica': 'Alta', 'potencia_crac': 'MA'},
            
            {'erro': 'ZE', 'delta_erro': 'NM', 'temp_externa': 'Baixa', 'carga_termica': 'Baixa', 'potencia_crac': 'M'},
            {'erro': 'ZE', 'delta_erro': 'NM', 'temp_externa': 'Baixa', 'carga_termica': 'Media', 'potencia_crac': 'M'},
            {'erro': 'ZE', 'delta_erro': 'NM', 'temp_externa': 'Baixa', 'carga_termica': 'Alta', 'potencia_crac': 'A'},
            {'erro': 'ZE', 'delta_erro': 'NM', 'temp_externa': 'Media', 'carga_termica': 'Baixa', 'potencia_crac': 'M'},
            {'erro': 'ZE', 'delta_erro': 'NM', 'temp_externa': 'Media', 'carga_termica': 'Media', 'potencia_crac': 'M'},
            {'erro': 'ZE', 'delta_erro': 'NM', 'temp_externa': 'Media', 'carga_termica': 'Alta', 'potencia_crac': 'A'},
            {'erro': 'ZE', 'delta_erro': 'NM', 'temp_externa': 'Alta', 'carga_termica': 'Baixa', 'potencia_crac': 'M'},
            {'erro': 'ZE', 'delta_erro': 'NM', 'temp_externa': 'Alta', 'carga_termica': 'Media', 'potencia_crac': 'A'},
            {'erro': 'ZE', 'delta_erro': 'NM', 'temp_externa': 'Alta', 'carga_termica': 'Alta', 'potencia_crac': 'A'},
            
            {'erro': 'ZE', 'delta_erro': 'NS', 'temp_externa': 'Baixa', 'carga_termica': 'Baixa', 'potencia_crac': 'M'},
            {'erro': 'ZE', 'delta_erro': 'NS', 'temp_externa': 'Baixa', 'carga_termica': 'Media', 'potencia_crac': 'M'},
            {'erro': 'ZE', 'delta_erro': 'NS', 'temp_externa': 'Baixa', 'carga_termica': 'Alta', 'potencia_crac': 'A'},
            {'erro': 'ZE', 'delta_erro': 'NS', 'temp_externa': 'Media', 'carga_termica': 'Baixa', 'potencia_crac': 'M'},
            {'erro': 'ZE', 'delta_erro': 'NS', 'temp_externa': 'Media', 'carga_termica': 'Media', 'potencia_crac': 'M'},
            {'erro': 'ZE', 'delta_erro': 'NS', 'temp_externa': 'Media', 'carga_termica': 'Alta', 'potencia_crac': 'A'},
            {'erro': 'ZE', 'delta_erro': 'NS', 'temp_externa': 'Alta', 'carga_termica': 'Baixa', 'potencia_crac': 'M'},
            {'erro': 'ZE', 'delta_erro': 'NS', 'temp_externa': 'Alta', 'carga_termica': 'Media', 'potencia_crac': 'M'},
            {'erro': 'ZE', 'delta_erro': 'NS', 'temp_externa': 'Alta', 'carga_termica': 'Alta', 'potencia_crac': 'A'},
            
            {'erro': 'ZE', 'delta_erro': 'ZE', 'temp_externa': 'Baixa', 'carga_termica': 'Baixa', 'potencia_crac': 'B'},
            {'erro': 'ZE', 'delta_erro': 'ZE', 'temp_externa': 'Baixa', 'carga_termica': 'Media', 'potencia_crac': 'M'},
            {'erro': 'ZE', 'delta_erro': 'ZE', 'temp_externa': 'Baixa', 'carga_termica': 'Alta', 'potencia_crac': 'M'},
            {'erro': 'ZE', 'delta_erro': 'ZE', 'temp_externa': 'Media', 'carga_termica': 'Baixa', 'potencia_crac': 'M'},
            {'erro': 'ZE', 'delta_erro': 'ZE', 'temp_externa': 'Media', 'carga_termica': 'Media', 'potencia_crac': 'M'},
            {'erro': 'ZE', 'delta_erro': 'ZE', 'temp_externa': 'Media', 'carga_termica': 'Alta', 'potencia_crac': 'A'},
            {'erro': 'ZE', 'delta_erro': 'ZE', 'temp_externa': 'Alta', 'carga_termica': 'Baixa', 'potencia_crac': 'M'},
            {'erro': 'ZE', 'delta_erro': 'ZE', 'temp_externa': 'Alta', 'carga_termica': 'Media', 'potencia_crac': 'M'},
            {'erro': 'ZE', 'delta_erro': 'ZE', 'temp_externa': 'Alta', 'carga_termica': 'Alta', 'potencia_crac': 'A'},
        ])
        
        # === REGRAS PARA ERRO POSITIVO (Temperatura Baixa) ===
        # Reduzir refrigeração
        rules.extend([
            # Erro Positivo Pequeno
            {'erro': 'PS', 'delta_erro': 'NB', 'temp_externa': 'Baixa', 'carga_termica': 'Baixa', 'potencia_crac': 'M'},
            {'erro': 'PS', 'delta_erro': 'NS', 'temp_externa': 'Baixa', 'carga_termica': 'Baixa', 'potencia_crac': 'B'},
            {'erro': 'PS', 'delta_erro': 'ZE', 'temp_externa': 'Baixa', 'carga_termica': 'Baixa', 'potencia_crac': 'B'},
            {'erro': 'PS', 'delta_erro': 'ZE', 'temp_externa': 'Baixa', 'carga_termica': 'Media', 'potencia_crac': 'M'},
            {'erro': 'PS', 'delta_erro': 'ZE', 'temp_externa': 'Media', 'carga_termica': 'Media', 'potencia_crac': 'M'},
            {'erro': 'PS', 'delta_erro': 'PS', 'temp_externa': 'Baixa', 'carga_termica': 'Baixa', 'potencia_crac': 'MB'},
            
            # Erro Positivo Médio
            {'erro': 'PM', 'delta_erro': 'NB', 'temp_externa': 'Baixa', 'carga_termica': 'Baixa', 'potencia_crac': 'M'},
            {'erro': 'PM', 'delta_erro': 'NS', 'temp_externa': 'Baixa', 'carga_termica': 'Baixa', 'potencia_crac': 'B'},
            {'erro': 'PM', 'delta_erro': 'ZE', 'temp_externa': 'Baixa', 'carga_termica': 'Baixa', 'potencia_crac': 'B'},
            {'erro': 'PM', 'delta_erro': 'ZE', 'temp_externa': 'Baixa', 'carga_termica': 'Media', 'potencia_crac': 'M'},
            {'erro': 'PM', 'delta_erro': 'ZE', 'temp_externa': 'Media', 'carga_termica': 'Media', 'potencia_crac': 'M'},
            {'erro': 'PM', 'delta_erro': 'PS', 'temp_externa': 'Baixa', 'carga_termica': 'Baixa', 'potencia_crac': 'MB'},
            
            # Erro Positivo Grande
            {'erro': 'PB', 'delta_erro': 'NB', 'temp_externa': 'Baixa', 'carga_termica': 'Baixa', 'potencia_crac': 'B'},
            {'erro': 'PB', 'delta_erro': 'NS', 'temp_externa': 'Baixa', 'carga_termica': 'Baixa', 'potencia_crac': 'B'},
            {'erro': 'PB', 'delta_erro': 'ZE', 'temp_externa': 'Baixa', 'carga_termica': 'Baixa', 'potencia_crac': 'MB'},
            {'erro': 'PB', 'delta_erro': 'ZE', 'temp_externa': 'Media', 'carga_termica': 'Baixa', 'potencia_crac': 'B'},
            {'erro': 'PB', 'delta_erro': 'ZE', 'temp_externa': 'Media', 'carga_termica': 'Media', 'potencia_crac': 'M'},
            {'erro': 'PB', 'delta_erro': 'PS', 'temp_externa': 'Baixa', 'carga_termica': 'Baixa', 'potencia_crac': 'MB'},
            {'erro': 'PB', 'delta_erro': 'PM', 'temp_externa': 'Baixa', 'carga_termica': 'Baixa', 'potencia_crac': 'MB'},
        ])
        
        return rules