import json

from data import DATA
from pokemon import Pokemon
from item import Item


class IdGenerator:
    def __init__(self):
        self.idModel = {
            "pokemons": "01",
            "items": "02"
        }

    def get_id_type(self, id):
        if id[:2] == self.idModel["pokemons"]:
            return "pokemons"
        elif id[:2] == self.idModel["items"]:
            return "items"

    @staticmethod
    def get_obj_type(obj):
        if type(obj) is Pokemon:
            return "pokemons"
        elif type(obj) is Item:
            return "items"

    def add_id(self, id):
        id_type = self.get_id_type(id)
        DATA.OBJ_ID[id_type].append(id)

    def remove_id(self, id):
        id_type = self.get_id_type(id)
        DATA.OBJ_ID[id_type].remove(id)

    def setup_id(self, obj):
        id = ""
        obj_type = self.get_obj_type(obj)
        id += self.idModel[obj_type]

        id_n = 0
        all_id_n = [int(n[2:]) for n in DATA.OBJ_ID[obj_type]]
        while id_n in all_id_n:
            id_n += 1

        id_n = str(id_n)
        while len(id_n) < 5:
            id_n = "0" + id_n
        id += id_n

        self.add_id(id)
        obj.publicId = id
