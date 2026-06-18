class Inventario:
    def __init__(self):
        self.itens = []

    def adicionar_item(self, item):
        self.itens.append(item)

    def remover_item(self, item_id):
        self.itens = [i for i in self.itens if i.get("id") != item_id]

    def consultar_itens(self):
        return self.itens

    def to_dict(self):
        return {"itens": self.itens}
