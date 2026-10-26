# questao_02/monte_carlo.py
import numpy as np

def simular_monte_carlo(catalogo, config, n_cenarios=2000):
    """
    Etapa A & D (Questão 2): Monte Carlo.
    Estima demanda e receitas sob incerteza (demanda, preço concorrente, custo logístico).
    """
    sigma_d = config["variabilidade"]["sigma_demanda"]
    sigma_p = config["variabilidade"]["sigma_preco_concorrente"]
    sigma_c = config["variabilidade"]["sigma_custo_logistico"]
    
    n_skus = len(catalogo)
    semanas = 12
    
    resultados_caixa = []
    
    for _ in range(n_cenarios):
        caixa_acumulado = 0.0
        for s in range(semanas):
            # Simular choques estocásticos normais
            fator_demanda = np.random.normal(1.0, sigma_d, n_skus)
            fator_preco_conc = np.random.normal(1.0, sigma_p, n_skus)
            fator_log = np.random.normal(1.0, sigma_c, n_skus)
            
            for i in range(n_skus):
                preco = catalogo.iloc[i]["preco_atual"]
                custo = catalogo.iloc[i]["custo_unitario"]
                estoque = catalogo.iloc[i]["estoque_inicial"] / 12
                demanda_base = catalogo.iloc[i]["demanda_base_semanal"]
                taxa_mkt = catalogo.iloc[i]["taxa_marketplace"]
                frete_base = catalogo.iloc[i]["custo_logistico_base"]
                
                demanda_real = max(0.0, demanda_base * fator_demanda[i])
                vendas = min(estoque, demanda_real)
                
                frete_real = frete_base * fator_log[i]
                margem_unit = (preco * (1 - taxa_mkt) - custo - frete_real)
                caixa_acumulado += vendas * max(0.0, margem_unit)
                
        resultados_caixa.append(caixa_acumulado)
        
    return np.array(resultados_caixa)
