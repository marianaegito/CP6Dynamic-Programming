# questao_01/main.py
import argparse
import time
import tracemalloc
import pandas as pd
import json
from pathlib import Path
from brute_force import resolver_brute_force
from genetic_algorithm import resolver_algoritmo_genetico
from greedy import aplicar_greedy_incentivos

def executar_questao_1(seed, modo):
    print(f"=== EXECUTANDO QUESTÃO 1 (Operação Caixa 90) ===")
    print(f"Seed: {seed} | Modo: {modo}")
    
    start_time = time.perf_counter()
    tracemalloc.start()
    
    # Carregar dados
    base_path = Path(__file__).parent.parent / "data"
    catalogo = pd.read_csv(base_path / f"q1_catalogo_G01.csv")
    with open(base_path / f"q1_config_G01.json", "r", encoding="utf-8") as f:
        config = json.load(f)
        
    print(f"Catálogo carregado com {len(catalogo)} SKUs.")
    
    # Etapa A: Brute Force em subconjunto reduzido (6 produtos)
    subset = catalogo.head(6).copy()
    print("\n[Etapa A] Executando Brute Force no subconjunto (6 SKUs)...")
    melhor_comb_bf, caixa_bf = resolver_brute_force(subset, config)
    print(f" -> Caixa Ótimo (Brute Force): R$ {caixa_bf:,.2f}")
    
    # Etapa B: Algoritmo Genético no catálogo completo
    print("\n[Etapa B] Executando Algoritmo Genético no catálogo completo (30 SKUs)...")
    melhor_ind_ga, caixa_ga, hist_fit = resolver_algoritmo_genetico(catalogo, config, n_geracoes=30, tam_populacao=30)
    print(f" -> Caixa Gerado (Algoritmo Genético): R$ {caixa_ga:,.2f}")
    
    # Etapa C: Greedy para alocação de incentivos
    print("\n[Etapa C] Executando Greedy para alocação de orçamento promocional...")
    incentivos, gasto_orcamento = aplicar_greedy_incentivos(catalogo, melhor_ind_ga, config)
    print(f" -> Orçamento Promocional Utilizado: R$ {gasto_orcamento:,.2f} de R$ {config['orcamento_promocional']:,.2f}")
    
    # Resultados Finais
    meta = config["meta_caixa_90d"]
    divida = config["divida_total_90d"]
    folga = caixa_ga - meta
    cobertura_divida = (caixa_ga / divida) * 100
    
    print("\n================ RESULTADOS FINAIS - QUESTÃO 1 ================")
    print(f"Caixa Operacional Gerado: R$ {caixa_ga:,.2f}")
    print(f"Meta de Caixa (90 dias): R$ {meta:,.2f}")
    print(f"Dívida Total (90 dias): R$ {divida:,.2f}")
    print(f"Cobertura da Dívida: {cobertura_divida:.2f}%")
    print(f"Meta Atingida? {'SIM (Folga de R$ ' + f'{folga:,.2f})' if folga >= 0 else 'NÃO (Insuficiência de R$ ' + f'{abs(folga):,.2f})'}")
    print("================================================================")
    
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    elapsed = time.perf_counter() - start_time
    
    print(f"Desempenho -> Tempo: {elapsed:.4f}s | Memória Pico: {peak / 1024 / 1024:.2f} MB")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=1011)
    parser.add_argument("--modo", type=str, default="completo")
    args = parser.parse_args()
    executar_questao_1(args.seed, args.modo)
