import numpy as np

class MembershipFunctions:
    """
    Define as funções de pertinência para todas as variáveis do sistema
    """
    
    def __init__(self):
        # Termos linguísticos
        self.erro_terms = ['NB', 'NM', 'NS', 'ZE', 'PS', 'PM', 'PB']  # Negativo/Positivo Grande/Médio/Pequeno/Zero
        self.delta_erro_terms = ['NB', 'NM', 'NS', 'ZE', 'PS', 'PM', 'PB']
        self.temp_externa_terms = ['Baixa', 'Media', 'Alta']
        self.carga_termica_terms = ['Baixa', 'Media', 'Alta']
        self.potencia_crac_terms = ['MB', 'B', 'M', 'A', 'MA']  # Muito Baixa/Baixa/Média/Alta/Muito Alta
        
        # Universos de discurso
        self.erro_universe = np.linspace(-10, 10, 200)
        self.delta_erro_universe = np.linspace(-5, 5, 200)
        self.temp_externa_universe = np.linspace(10, 35, 200)
        self.carga_termica_universe = np.linspace(0, 100, 200)
        self.potencia_crac_universe = np.linspace(0, 100, 200)
        
        # Define as funções de pertinência
        self._define_membership_functions()
    
    def _define_membership_functions(self):
        """Define todas as funções de pertinência"""
        
        # ERRO DE TEMPERATURA
        self.erro_mf = {
            'NB': lambda x: self._trapmf(x, [-10, -10, -8, -4]),     # Negativo Grande
            'NM': lambda x: self._trimf(x, [-8, -4, -2]),            # Negativo Médio
            'NS': lambda x: self._trimf(x, [-4, -2, 0]),             # Negativo Pequeno
            'ZE': lambda x: self._trimf(x, [-2, 0, 2]),              # Zero
            'PS': lambda x: self._trimf(x, [0, 2, 4]),               # Positivo Pequeno
            'PM': lambda x: self._trimf(x, [2, 4, 8]),               # Positivo Médio
            'PB': lambda x: self._trapmf(x, [4, 8, 10, 10])          # Positivo Grande
        }
        
        # DELTA ERRO
        self.delta_erro_mf = {
            'NB': lambda x: self._trapmf(x, [-5, -5, -4, -2]),       # Negativo Grande
            'NM': lambda x: self._trimf(x, [-4, -2, -1]),            # Negativo Médio
            'NS': lambda x: self._trimf(x, [-2, -1, 0]),             # Negativo Pequeno
            'ZE': lambda x: self._trimf(x, [-1, 0, 1]),              # Zero
            'PS': lambda x: self._trimf(x, [0, 1, 2]),               # Positivo Pequeno
            'PM': lambda x: self._trimf(x, [1, 2, 4]),               # Positivo Médio
            'PB': lambda x: self._trapmf(x, [2, 4, 5, 5])            # Positivo Grande
        }
        
        # TEMPERATURA EXTERNA
        self.temp_externa_mf = {
            'Baixa': lambda x: self._trapmf(x, [10, 10, 15, 20]),
            'Media': lambda x: self._trimf(x, [15, 22, 28]),
            'Alta': lambda x: self._trapmf(x, [25, 30, 35, 35])
        }
        
        # CARGA TÉRMICA
        self.carga_termica_mf = {
            'Baixa': lambda x: self._trapmf(x, [0, 0, 20, 40]),
            'Media': lambda x: self._trimf(x, [30, 50, 70]),
            'Alta': lambda x: self._trapmf(x, [60, 80, 100, 100])
        }
        
        # POTÊNCIA CRAC (SAÍDA)
        self.potencia_crac_mf = {
            'MB': lambda x: self._trapmf(x, [0, 0, 10, 25]),         # Muito Baixa
            'B': lambda x: self._trimf(x, [15, 30, 45]),             # Baixa
            'M': lambda x: self._trimf(x, [35, 50, 65]),             # Média
            'A': lambda x: self._trimf(x, [55, 70, 85]),             # Alta
            'MA': lambda x: self._trapmf(x, [75, 90, 100, 100])      # Muito Alta
        }
    
    def _trimf(self, x, params):
        """Função de pertinência triangular"""
        a, b, c = params
        if isinstance(x, np.ndarray):
            result = np.zeros_like(x, dtype=float)
            result = np.maximum(np.minimum((x - a) / (b - a + 1e-10), 
                                          (c - x) / (c - b + 1e-10)), 0)
            return result
        else:
            if x <= a or x >= c:
                return 0.0
            elif a < x <= b:
                return (x - a) / (b - a + 1e-10)
            else:
                return (c - x) / (c - b + 1e-10)
    
    def _trapmf(self, x, params):
        """Função de pertinência trapezoidal"""
        a, b, c, d = params
        if isinstance(x, np.ndarray):
            result = np.zeros_like(x, dtype=float)
            result = np.maximum(np.minimum(np.minimum((x - a) / (b - a + 1e-10), 1.0),
                                          (d - x) / (d - c + 1e-10)), 0)
            return result
        else:
            if x <= a or x >= d:
                return 0.0
            elif a < x < b:
                return (x - a) / (b - a + 1e-10)
            elif b <= x <= c:
                return 1.0
            else:
                return (d - x) / (d - c + 1e-10)
    
    def get_membership(self, variable, term, value):
        """Retorna o grau de pertinência de um valor em um termo linguístico"""
        if variable == 'erro':
            return self.erro_mf[term](value)
        elif variable == 'delta_erro':
            return self.delta_erro_mf[term](value)
        elif variable == 'temp_externa':
            return self.temp_externa_mf[term](value)
        elif variable == 'carga_termica':
            return self.carga_termica_mf[term](value)
        elif variable == 'potencia_crac':
            return self.potencia_crac_mf[term](value)
        else:
            raise ValueError(f"Variável desconhecida: {variable}")
    
    def get_all_membership_data(self):
        """Retorna dados de todas as funções de pertinência para visualização"""
        data = {}
        
        # Erro
        data['erro'] = {
            'universe': self.erro_universe.tolist(),
            'terms': {}
        }
        for term in self.erro_terms:
            data['erro']['terms'][term] = self.erro_mf[term](self.erro_universe).tolist()
        
        # Delta Erro
        data['delta_erro'] = {
            'universe': self.delta_erro_universe.tolist(),
            'terms': {}
        }
        for term in self.delta_erro_terms:
            data['delta_erro']['terms'][term] = self.delta_erro_mf[term](self.delta_erro_universe).tolist()
        
        # Temperatura Externa
        data['temp_externa'] = {
            'universe': self.temp_externa_universe.tolist(),
            'terms': {}
        }
        for term in self.temp_externa_terms:
            data['temp_externa']['terms'][term] = self.temp_externa_mf[term](self.temp_externa_universe).tolist()
        
        # Carga Térmica
        data['carga_termica'] = {
            'universe': self.carga_termica_universe.tolist(),
            'terms': {}
        }
        for term in self.carga_termica_terms:
            data['carga_termica']['terms'][term] = self.carga_termica_mf[term](self.carga_termica_universe).tolist()
        
        # Potência CRAC
        data['potencia_crac'] = {
            'universe': self.potencia_crac_universe.tolist(),
            'terms': {}
        }
        for term in self.potencia_crac_terms:
            data['potencia_crac']['terms'][term] = self.potencia_crac_mf[term](self.potencia_crac_universe).tolist()
        
        return data