from faulthandler import is_enabled


class Inventory:
    def __init__(self):
        self.items = {}
        self.medicine = {}
        self.CT_CS = {}
        self.berries = {}
        self.keys_items = {}

    def add_item(self, item):
        pass

    def use_item(self, item):
        pass

    def check_id(self, id):
        for item in self.items:
            if item.id == id:
                return True
        for item in self.medicine:
            if item.id == id:
                return True
        for item in self.CT_CS:
            if item.id == id:
                return True
        for item in self.berries:
            if item.id == id:
                return True
        for item in self.keys_items:
            if item.id == id:
                return True
        return False

    def save_inventory(self):
        return {
            "items": self.items,
            "medicine": self.medicine,
            "CT_CS": self.CT_CS,
            "berries": self.berries,
            "keys_items": self.keys_items
        }

    def load_inventory(self, data):
        self.items = data["items"]
        self.medicine = data["medicine"]
        self.CT_CS = data["CT_CS"]
        self.berries = data["berries"]
        self.keys_items = data["keys_items"]
