# questao_01/greedy.py
import numpy as np

def aplicar_greedy_incentivos(catalogo, precos_propostos, config):
    """
    Etapa C (Questão 1): Greedy.
    Distribui o orçamento limitado de incentivo comercial (cupom/cashback/frete)
    aos produtos com maior benefício marginal por real investido.
    """
    orcamento = config["orcamento_promocional"]
    
    skus = catalogo["sku"].tolist()
    precos_base = catalogo["preco_atual"].tolist()
    demandas = catalogo["demanda_base_90d"].tolist()
    estoques = catalogo["estoque"].tolist()
    elasticidades = catalogo["elasticidade"].tolist()
    custos = catalogo["custo_unitario"].tolist()
    taxas_mkt = catalogo["taxa_marketplace"].tolist()
    custos_log = catalogo["custo_logistico"].tolist()
    
    # Avaliar elasticidade e potencial de incremento de demanda por incentivo (ex: desconto adicional de 5%)
    beneficios = []
    for i in range(len(skus)):
        p = precos_base[i] * precos_propostos[i]
        # Custo do incentivo unitário (ex: 5% do preço)
        custo_incentivo = p * 0.05
        # Incremento de demanda estimado pela elasticidade
        delta_demanda = demandas[i] * elasticidades[i] * 0.05
        incremento_receita = delta_demanda * p * (1 - taxas_mkt[i])
        
        # Razão benefício / custo por unidade
        razao = incremento_receita / (custo_incentivo if custo_incentivo > 0 else 1.0)
        beneficios.append({
            "idx": i,
            "sku": skus[i],
            "razao": razao,
            "custo_unit": custo_incentivo,
            "max_unidades": min(estoques[i], demandas[i])
        })
        
    # Ordenar por maior benefício marginal
    beneficios = sorted(beneficios, key=lambda x: x["razao"], reverse=True)
    
    orcamento_gasto = 0.0
    incentivos_aplicados = {skus[i]: 0.0 for i in range(len(skus))}
    
    for item in beneficios:
        idx = item["idx"]
        unidades = item["max_unidades"]
        custo_total_item = unidades * item["custo_unit"]
        
        if orcamento_gasto + custo_total_item <= orcamento:
            orcamento_gasto += custo_total_item
            incentivos_aplicados[item["sku"]] = item["custo_unit"]
        else:
            unidades_parciais = (orcamento - orcamento_gasto) / (item["custo_unit"] if item["custo_unit"] > 0 else 1.0)
            if unidades_parciais > 0:
                orcamento_gasto = orcamento
                incentivos_aplicados[item["sku"]] = item["custo_unit"] * (unidades_parciais / unidades if unidades > 0 else 0)
            break
            
    return incentivos_aplicados, orcamento_gasto
