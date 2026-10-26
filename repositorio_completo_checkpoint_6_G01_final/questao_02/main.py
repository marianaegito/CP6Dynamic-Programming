# questao_02/main.py
import argparse
import time
import tracemalloc
import pandas as pd
import json
from pathlib import Path
from monte_carlo import simular_monte_carlo
from dynamic_programming import resolver_programacao_dinamica
from greedy import aplicar_greedy_semanal

def executar_questao_2(seed, cenarios):
    print(f"=== EXECUTANDO QUESTÃO 2 (Plano de Sobrevivência em 12 Semanas) ===")
    print(f"Seed: {seed} | Cenários: {cenarios}")
    
    start_time = time.perf_counter()
    tracemalloc.start()
    
    base_path = Path(__file__).parent.parent / "data"
    catalogo = pd.read_csv(base_path / f"q2_catalogo_G01.csv")
    with open(base_path / f"q2_config_G01.json", "r", encoding="utf-8") as f:
        config = json.load(f)
        
    print(f"Catálogo Q2 carregado com {len(catalogo)} SKUs.")
    
    # Etapa A: Monte Carlo Inicial
    print("\n[Etapa A] Executando Monte Carlo inicial (2.000 cenários)...")
    caixas_mc1 = simular_monte_carlo(catalogo, config, n_cenarios=2000)
    print(f" -> Caixa médio estimado: R$ {np.mean(caixas_mc1):,.2f}")
    
    # Etapa B: Programação Dinâmica (Trajetória Semanal)
    print("\n[Etapa B] Executando Programação Dinâmica para trajetória semanal de preços...")
    trajetoria = resolver_programacao_dinamica(catalogo, config)
    print(f" -> Trajetória calculada para {len(trajetoria)} produtos ao longo de 12 semanas.")
    
    # Etapa C: Greedy Semanal
    print("\n[Etapa C] Executando Greedy Semanal para alocação de destaques...")
    destaques = aplicar_greedy_semanal(catalogo, config)
    print(" -> Destaques semanais alocados com sucesso.")
    
    # Etapa D: Validação Monte Carlo Final (com o número de cenários recebido por argumento)
    print(f"\n[Etapa D] Executando Validação Monte Carlo Final ({cenarios} cenários independentes)...")
    caixas_val = simular_monte_carlo(catalogo, config, n_cenarios=cenarios)
    
    dividas_dict = config["dividas"]
    divida_total = sum(dividas_dict.values())
    caixa_inicial = config["caixa_inicial"]
    
    caixa_final_esperado = caixa_inicial + np.mean(caixas_val)
    prob_sucesso = np.mean((caixa_inicial + caixas_val) >= divida_total) * 100
    
    print("\n================ RESULTADOS FINAIS - QUESTÃO 2 ================")
    print(f"Caixa Inicial: R$ {caixa_inicial:,.2f}")
    print(f"Compromissos Totais de Dívida: R$ {divida_total:,.2f}")
    print(f"Caixa Final Esperado (Médio): R$ {caixa_final_esperado:,.2f}")
    print(f"Probabilidade de Pagamento no Prazo: {prob_sucesso:.2f}%")
    print(f"Meta de Risco (< {config['limite_risco_falha']*100}% de falha)? {'APROVADO' if (100 - prob_sucesso) <= (config['limite_risco_falha']*100) else 'ATENÇÃO'}")
    print("================================================================")
    
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    elapsed = time.perf_counter() - start_time
    
    print(f"Desempenho -> Tempo: {elapsed:.4f}s | Memória Pico: {peak / 1024 / 1024:.2f} MB")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=1011)
    parser.add_argument("--cenarios", type=int, default=5000)
    args = parser.parse_args()
    executar_questao_2(args.seed, args.cenarios)
