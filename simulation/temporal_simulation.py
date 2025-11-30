import numpy as np
from .physical_model import PhysicalModel

class TemporalSimulation:
    """Simulação temporal de 24 horas"""
    
    def __init__(self, fuzzy_controller):
        self.fuzzy = fuzzy_controller
        self.model = PhysicalModel()
        self.setpoint = 22.0
    
    def run_24h_simulation(self, temp_inicial=22.0, temp_externa_base=25.0, carga_base=40.0):
        """
        Executa simulação de 1440 minutos (24h)
        Otimizada para executar mais rápido
        """
        minutes = 1440
        # Simula a cada 5 minutos para performance, depois interpola
        step_size = 5
        sim_points = minutes // step_size
        
        results = {
            'time': [],
            'temperature': [],
            'power_crac': [],
            'temp_externa': [],
            'carga_termica': [],
            'erro': [],
            'setpoint': []
        }
        
        T_atual = temp_inicial
        erro_anterior = 0
        
        print(f"⚙️ Simulando {minutes} minutos (otimizado)...")
        
        # Arrays temporários para armazenar pontos simulados
        temp_points = []
        time_points = []
        
        for i in range(sim_points + 1):
            t = i * step_size
            if t > minutes:
                t = minutes
                
            # Progresso
            if i % (sim_points // 10 + 1) == 0:
                progress = (t / minutes) * 100
                print(f"   {progress:.0f}% completo")
            
            # Temperatura externa (padrão senoidal + ruído)
            T_ext = temp_externa_base + 5 * np.sin(2 * np.pi * t / 1440) + np.random.normal(0, 0.5)
            T_ext = np.clip(T_ext, 10, 35)
            
            # Carga térmica (perfil de uso)
            if 480 <= t < 1080:  # 8h às 18h - horário comercial
                Q_est = carga_base + 20 + np.random.normal(0, 5)
            else:
                Q_est = carga_base - 10 + np.random.normal(0, 3)
            Q_est = np.clip(Q_est, 0, 100)
            
            # Calcula erro e variação
            erro = T_atual - self.setpoint
            delta_erro = erro - erro_anterior
            
            # Controlador fuzzy
            P_crac = self.fuzzy.calculate(erro, delta_erro, T_ext, Q_est)
            
            # Atualiza temperatura
            T_atual = self.model.update_temperature(T_atual, P_crac, Q_est, T_ext)
            
            # Armazena pontos simulados
            time_points.append(t)
            temp_points.append(T_atual)
            
            results['time'].append(t)
            results['temperature'].append(float(T_atual))
            results['power_crac'].append(float(P_crac))
            results['temp_externa'].append(float(T_ext))
            results['carga_termica'].append(float(Q_est))
            results['erro'].append(float(erro))
            results['setpoint'].append(self.setpoint)
            
            erro_anterior = erro
        
        print("✅ Simulação completa!")
        return results
    
    def calculate_metrics(self, results):
        """Calcula métricas de desempenho"""
        temps = np.array(results['temperature'])
        erros = np.array(results['erro'])
        
        # RMSE
        rmse = np.sqrt(np.mean(erros**2))
        
        # Tempo em faixa (20-24°C)
        in_range = np.sum((temps >= 20) & (temps <= 24))
        percent_in_range = (in_range / len(temps)) * 100
        
        # Violações críticas (<18 ou >26)
        violations = np.sum((temps < 18) | (temps > 26))
        
        # Consumo energético
        energy = np.sum(results['power_crac'])
        
        return {
            'rmse': float(rmse),
            'percent_in_range': float(percent_in_range),
            'violations': int(violations),
            'energy_consumption': float(energy),
            'avg_temp': float(np.mean(temps)),
            'max_temp': float(np.max(temps)),
            'min_temp': float(np.min(temps))
        }
