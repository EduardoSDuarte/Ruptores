from itertools import combinations

def held_karp(distancias, salas):
    n = len(salas)
    INF = float('inf')

    # dp[mascara][i] = menor custo para chegar em i visitando as salas na mascara
    dp = [[INF] * n for _ in range(1 << n)]
    pai = [[-1] * n for _ in range(1 << n)]

    dp[1][0] = 0  # começa na sala 0 (entrada)

    for mascara in range(1 << n):
        for u in range(n):
            if not (mascara & (1 << u)):
                continue
            if dp[mascara][u] == INF:
                continue
            for v in range(n):
                if mascara & (1 << v):
                    continue
                nova_mascara = mascara | (1 << v)
                novo_custo = dp[mascara][u] + distancias[u][v]
                if novo_custo < dp[nova_mascara][v]:
                    dp[nova_mascara][v] = novo_custo
                    pai[nova_mascara][v] = u

    mascara_final = (1 << n) - 1
    custo_minimo = INF
    ultimo = -1

    for u in range(1, n):
        if dp[mascara_final][u] + distancias[u][0] < custo_minimo:
            custo_minimo = dp[mascara_final][u] + distancias[u][0]
            ultimo = u

    # Reconstrói o caminho
    caminho = []
    mascara = mascara_final
    atual = ultimo
    while atual != -1:
        caminho.append(salas[atual])
        anterior = pai[mascara][atual]
        mascara ^= (1 << atual)
        atual = anterior

    caminho.reverse()

    return {
        "custo_otimo": custo_minimo,
        "rota_otima": caminho
    }