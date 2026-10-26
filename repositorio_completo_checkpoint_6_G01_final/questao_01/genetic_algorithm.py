# questao_01/genetic_algorithm.py
import random
import numpy as np

def resolver_algoritmo_genetico(catalogo, config, n_geracoes=50, tam_populacao=40, taxa_mutacao=0.15):
    """
    Etapa B (Questão 1): Algoritmo Genético.
    Busca a configuração de preços para o catálogo completo (30 SKUs).
    """
    niveis = config["niveis_preco_relativos"]
    margem_min = config["margem_minima_percentual"]
    
    skus = catalogo["sku"].tolist()
    precos_base = catalogo["preco_atual"].tolist()
    custos = catalogo["custo_unitario"].tolist()
    estoques = catalogo["estoque"].tolist()
    demandas = catalogo["demanda_base_90d"].tolist()
    elasticidades = catalogo["elasticidade"].tolist()
    taxas_mkt = catalogo["taxa_marketplace"].tolist()
    custos_log = catalogo["custo_logistico"].tolist()
    
    n_produtos = len(skus)
    
    def calcular_fitness(individuo):
        caixa_total = 0.0
        penalidade = 0.0
        
        for i, mult in enumerate(individuo):
            p_novo = precos_base[i] * mult
            delta_preco_pct = (p_novo - precos_base[i]) / precos_base[i]
            demanda_estimada = demandas[i] * (1 - elasticidades[i] * delta_preco_pct)
            unidades_vendidas = min(estoques[i], max(0.0, demanda_estimada))
            
            margem_unit = (p_novo * (1 - taxas_mkt[i]) - custos[i] - custos_log[i])
            margem_pct = (margem_unit / p_novo) if p_novo > 0 else 0.0
            
            if margem_pct < margem_min:
                penalidade += 10000.0  # Penalidade forte por violar margem mínima
                
            caixa_total += unidades_vendidas * margem_unit
            
        return caixa_total - penalidade

    # Inicializar população
     populacao = [[random.choice(niveis) for _ in range(n_produtos)] for _ in range(tam_populacao)]
    
    historico_fitness = []
    
    for geracao in range(n_geracoes):
        fitness_scores = [calcular_fitness(ind) for ind in populacao]
        
        # Elitismo: manter os 2 melhores
        pares = sorted(zip(populacao, fitness_scores), key=lambda x: x[1], reverse=True)
        populacao = [p[0] for p in pares]
        
        historico_fitness.append(pares[0][1])
        
        nova_geracao = populacao[:2] # Elitismo
        
        while len(nova_geracao) < tam_populacao:
            # Torneio simples para seleção
            pai1 = max(random.sample(pares[:20], 2), key=lambda x: x[1])[0]
            pai2 = max(random.sample(pares[:20], 2), key=lambda x: x[1])[0]
            
            # Crossover de um ponto
            ponto = random.randint(1, n_produtos - 1)
            filho = pai1[:ponto] + pai2[ponto:]
            
            # Mutação
            for i in range(n_produtos):
                if random.random() < taxa_mutacao:
                    filho[i] = random.choice(niveis)
                    
            nova_geracao.append(filho)
            
        populacao = nova_geracao
        
    melhor_ind = pares[0][0]
    melhor_fit = pares[0][1]
    
    return melhor_ind, melhor_fit, historico_fitness
