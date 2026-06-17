class Partida:
    def __init__(self):
        self.deck_jogador = []
        self.rota_jogador = []
        self.vida_time = 100
        self.inventario = []
        self.sala_atual = 0
        self.resultado_knapsack = None
        self.resultado_tsp = None
        self.score_final = None

    def calcular_vida_time(self):
        return sum(c["vida"] for c in self.deck_jogador)

    def calcular_dano_time(self):
        dano_base = sum(c["dano"] for c in self.deck_jogador)
        bonus = 0
        for item in self.inventario:
            if "dano_time" in item.get("efeito", ""):
                percentual = int(item["efeito"].split("+")[1].replace("%", ""))
                bonus += dano_base * (percentual / 100)
        return int(dano_base + bonus)

    def to_dict(self):
        return {
            "deck_jogador": self.deck_jogador,
            "rota_jogador": self.rota_jogador,
            "vida_time": self.vida_time,
            "inventario": self.inventario,
            "sala_atual": self.sala_atual,
        }
