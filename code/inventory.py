from item import Item


class Inventory:
    def __init__(self):
        self.items = []
        self.medicine = []
        self.CT_CS = []
        self.berries = []
        self.keys_items = []

    def add_item(self, item):
        if item.socket == 1:
            self.items.append(item)
        elif item.socket == 5:
            self.keys_items.append(item)
        elif item.socket == 6:
            self.medicine.append(item)

    def use_item(self, item):
        pass

    def save_inventory(self):
        return {
            "items": [item.dbSymbol for item in self.items],
            "medicine": [item.dbSymbol for item in self.medicine],
            "CT_CS": [item.dbSymbol for item in self.CT_CS],
            "berries": [item.dbSymbol for item in self.berries],
            "keys_items": [item.dbSymbol for item in self.keys_items]
        }

    def load_inventory(self, data):
        self.items = [Item(dbsymbol) for dbsymbol in data["items"]]
        self.medicine = [Item(dbsymbol) for dbsymbol in data["medicine"]]
        self.CT_CS = [Item(dbsymbol) for dbsymbol in data["CT_CS"]]
        self.berries = [Item(dbsymbol) for dbsymbol in data["berries"]]
        self.keys_items = [Item(dbsymbol) for dbsymbol in data["keys_items"]]
