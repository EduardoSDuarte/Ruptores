from algorithms.knapsack import knapsack
from algorithms.tsp import held_karp
from algorithms.scoring import calcular_score_final

# Teste Knapsack
cartas = [
    {"nome": "Eduardo", "custo": 3, "vida": 25, "dano": 25},
    {"nome": "Monique", "custo": 4, "vida": 25, "dano": 30},
    {"nome": "Pietra",  "custo": 3, "vida": 35, "dano": 20},
    {"nome": "Vanessa", "custo": 4, "vida": 25, "dano": 35},
    {"nome": "Camila",  "custo": 3, "vida": 35, "dano": 15},
]

resultado = knapsack(cartas, 10)
print("=== KNAPSACK ===")
print(f"Valor ótimo: {resultado['valor_otimo']}")
print(f"Cartas ótimas: {[c['nome'] for c in resultado['cartas_otimas']]}")

# Teste TSP
salas = ["Entrada", "Alfa", "Beta", "Gama", "Delta"]
distancias = [
    [0, 3, 6, 7, 5],
    [3, 0, 2, 8, 4],
    [6, 2, 0, 4, 6],
    [7, 8, 4, 0, 2],
    [5, 4, 6, 2, 0],
]

resultado_tsp = held_karp(distancias, salas)
print("\n=== TSP ===")
print(f"Custo ótimo: {resultado_tsp['custo_otimo']}")
print(f"Rota ótima: {resultado_tsp['rota_otima']}")

# Teste Scoring
score = calcular_score_final(85, 70, 4, 5)
print("\n=== SCORING ===")
print(f"Eficiência Knapsack: {score['ef_knapsack']}%")
print(f"Eficiência TSP: {score['ef_tsp']}%")
print(f"Score Final: {score['score_final']}")
print(f"Estrelas: {score['estrelas']}")