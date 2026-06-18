
def calcular_eficiencia_knapsack(valor_jogador, valor_otimo):
    if valor_otimo == 0:
        return 100
    return round((valor_jogador / valor_otimo) * 100)


def calcular_eficiencia_tsp(custo_jogador, custo_otimo):
    if custo_jogador == 0:
        return 100
    return round((custo_otimo / custo_jogador) * 100)


def calcular_score_final(ef_knapsack, ef_tsp, itens_coletados, total_itens):
    ef_inventario = round((itens_coletados / total_itens) * 100) if total_itens > 0 else 0
    score = round((ef_knapsack + ef_tsp + ef_inventario) / 3)
    return {
        "ef_knapsack": ef_knapsack,
        "ef_tsp": ef_tsp,
        "ef_inventario": ef_inventario,
        "score_final": score,
        "estrelas": calcular_estrelas(score)
    }


def calcular_estrelas(score):
    if score >= 90:
        return 5
    elif score >= 75:
        return 4
    elif score >= 60:
        return 3
    elif score >= 40:
        return 2
    else:
        return 1
