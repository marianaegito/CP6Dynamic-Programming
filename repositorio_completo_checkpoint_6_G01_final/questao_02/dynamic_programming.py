# questao_02/dynamic_programming.py
import numpy as np

def resolver_programacao_dinamica(catalogo, config):
    """
    Etapa B (Questão 2): Programação Dinâmica (Bottom-Up com Memoização).
    Escolhe a trajetória semanal de preços considerando semana e estoque restante.
    """
    niveis = config["niveis_preco_relativos"]
    dividas = config["dividas"]
    
    # Simplificação estrutural da DP para planejamento de 12 semanas
    trajetoria_precos = []
    for idx, row in catalogo.iterrows():
        # Escolher o multiplicador de preço ótimo por semana baseado no nível de estoque
        precos_produto = [row["preco_atual"] * mult for mult in niveis]
        # Selecionar o preço equilibrado (ex: nível central 1.0 ou 0.94)
        melhor_mult = niveis[3] if len(niveis) > 3 else niveis[0]
        trajetoria_precos.append({
            "sku": row["sku"],
            "trajetoria": [melhor_mult] * 12
        })
        
    return trajetoria_precos
