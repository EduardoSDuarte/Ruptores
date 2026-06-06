def knapsack(cartas, capacidade):
    n = len(cartas)
    dp = [[0] * (capacidade + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        carta = cartas[i - 1]
        custo = carta["custo"]
        valor = carta["dano"] + carta["vida"]

        for w in range(capacidade + 1):
            dp[i][w] = dp[i - 1][w]
            if custo <= w:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - custo] + valor)

    # Rastreia quais cartas foram escolhidas
    w = capacidade
    selecionadas = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selecionadas.append(cartas[i - 1])
            w -= cartas[i - 1]["custo"]

    return {
        "valor_otimo": dp[n][capacidade],
        "cartas_otimas": selecionadas
    }