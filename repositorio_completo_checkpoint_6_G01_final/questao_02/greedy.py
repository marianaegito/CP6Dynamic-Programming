# questao_02/greedy.py
def aplicar_greedy_semanal(catalogo, config):
    """
    Etapa C (Questão 2): Greedy Semanal.
    Aloca destaques e mídia promocional semanalmente aos produtos de maior margem.
    """
    orcamento_semanal = config["orcamento_promocional_semanal"]
    destaques_semanais = {}
    
    for semana in range(1, 13):
        # Selecionar top 3 produtos com maior margem unitária
        catalogo_ordenado = catalogo.copy()
        catalogo_ordenado["margem"] = catalogo_ordenado["preco_atual"] * (1 - catalogo_ordenado["taxa_marketplace"]) - catalogo_ordenado["custo_unitario"]
        top_produtos = catalogo_ordenado.sort_values(by="margem", ascending=False).head(3)["sku"].tolist()
        destaques_semanais[f"semana_{semana}"] = top_produtos
        
    return destaques_semanais
