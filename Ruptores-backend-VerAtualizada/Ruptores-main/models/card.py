class Card:
    def __init__(self, id, nome, codinome, classificacao, custo, vida, dano, efeito):
        self.id = id
        self.nome = nome
        self.codinome = codinome
        self.classificacao = classificacao
        self.custo = custo
        self.vida = vida
        self.dano = dano
        self.efeito = efeito

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "codinome": self.codinome,
            "classificacao": self.classificacao,
            "custo": self.custo,
            "vida": self.vida,
            "dano": self.dano,
            "efeito": self.efeito,
        }
