# questao_01/brute_force.py
import itertools
import numpy as np
import pandas as pd

def resolver_brute_force(catalogo_subset, config):
    """
    Etapa A (Questão 1): Brute Force.
    Testa todas as combinações de preços permitidos para um subconjunto pequeno (>= 6 produtos).
    Retorna a combinação ótima (máximo caixa operacional respeitando margem mínima e estoque).
    """
    niveis = config["niveis_preco_relativos"]
    margem_min = config["margem_minima_percentual"]
    
    skus = catalogo_subset["sku"].tolist()
    precos_base = catalogo_subset["preco_atual"].tolist()
    custos = catalogo_subset["custo_unitario"].tolist()
    estoques = catalogo_subset["estoque"].tolist()
    demandas = catalogo_subset["demanda_base_90d"].tolist()
    elasticidades = catalogo_subset["elasticidade"].tolist()
    taxas_mkt = catalogo_subset["taxa_marketplace"].tolist()
    custos_log = catalogo_subset["custo_logistico"].tolist()
    
    # Gerar todas as combinações de multiplicadores de preço para o subconjunto
    melhor_caixa = -float("inf")
    melhor_combinacao = None
    
    # Produto cartesiano dos níveis de preço permitidos
    for comb in itertools.product(niveis, repeat=len(skus)):
        caixa_total = 0.0
        valido = True
        
        for i, mult in enumerate(comb):
            p_novo = precos_base[i] * mult
            # Demanda ajustada pela elasticidade
            delta_preco_pct = (p_novo - precos_base[i]) / precos_base[i]
            demanda_estimada = demandas[i] * (1 - elasticidades[i] * delta_preco_pct)
            demanda_estimada = max(0.0, demanda_estimada)
            unidades_vendidas = min(estoques[i], demanda_estimada)
            
            # Margem unitária
            margem_unit = (p_novo * (1 - taxas_mkt[i]) - custos[i] - custos_log[i])
            if p_novo > 0:
                margem_pct = margem_unit / p_novo
            else:
                margem_pct = 0.0
                
            if margem_pct < margem_min:
                valido = False
                break
                
            caixa_total += unidades_vendidas * margem_unit
            
        if valido and caixa_total > melhor_caixa:
            melhor_caixa = caixa_total
            melhor_combinacao = comb
            
    return melhor_combinacao, melhor_caixa
