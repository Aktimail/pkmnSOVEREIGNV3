import pygame

from entity import Entity
from pokemon import Pokemon
from inventory import Inventory
from questManager import QuestManager
from settings import SETTINGS


class Player(Entity):
    def __init__(self, screen, name, spritesheet, x, y, keyboard, controller):
        super().__init__(screen, name, x, y)
        self.name = name
        self.dbSymbol = name
        self.Keyboard = keyboard
        self.Controller = controller

        self.all_spritesheet = {
            "walk": f"../assets/graphics/spritesheets/{spritesheet}.png",
            "run": f"../assets/graphics/spritesheets/{spritesheet}_run.png",
            "bicycle_stop": f"../assets/graphics/spritesheets/{spritesheet}_cycle_stop.png",
            "bicycle": f"../assets/graphics/spritesheets/{spritesheet}_cycle_roll.png"
        }
        self.spritesheet = self.all_spritesheet["walk"]
        self.sprite_update()

        self.team = [Pokemon("bronzong", 100, {
            "ability": "heatproof",
            "moveset": ["frustration", "fire_punch"],
            "nature": "adamant",
            "ivs": {
                "hp": 31,
                "atk": 31,
                "defe": 31,
                "aspe": 31,
                "dspe": 31,
                "spd": 31
            },
        })]

        self.Inventory = Inventory()

        self.QuestManager = QuestManager()

        self.bike = False

        self.npcsEncountered = []
        self.trainersDefeated = []
        self.collectedItems = []

    def update(self):
        self.check_inputs()
        super().update()

    def check_inputs(self):
        if not self.inMotion:
            if self.Keyboard.key_pressed(self.Controller.keybinds["up"]):
                self.move("up")
            elif self.Keyboard.key_pressed(self.Controller.keybinds["down"]):
                self.move("down")
            elif self.Keyboard.key_pressed(self.Controller.keybinds["left"]):
                self.move("left")
            elif self.Keyboard.key_pressed(self.Controller.keybinds["right"]):
                self.move("right")

            if not self.bike:
                self.switch_walk()
            elif self.bike:
                if self.inMotion:
                    self.spritesheet = self.all_spritesheet["bicycle"]
                elif not self.inMotion:
                    self.spritesheet = self.all_spritesheet["bicycle_stop"]

            if self.Keyboard.key_pressed(self.Controller.keybinds["run"]):
                self.switch_run()

            if self.Keyboard.key_pressed(self.Controller.keybinds["bike"]):
                self.Keyboard.remove_key(self.Controller.keybinds["bike"])
                self.switch_bike()

            if self.Keyboard.key_pressed(self.Controller.keybinds["interact"]):
                self.Keyboard.remove_key(self.Controller.keybinds["interact"])
                self.interaction = True
            else:
                self.interaction = False

    def switch_walk(self):
        if not self.position.x % 2 and not self.position.y % 2:
            self.speed = SETTINGS.WALK_SPEED
            self.spritesheet = self.all_spritesheet["walk"]

    def switch_run(self):
        if not self.bike:
            if self.inMotion:
                self.speed = SETTINGS.RUN_SPEED
                self.spritesheet = self.all_spritesheet["run"]

    def switch_bike(self):
        if not self.interaction:
            if not self.bike:
                self.bike = True
                self.speed = SETTINGS.BIKE_SPEED
            elif self.bike:
                self.switch_walk()
                self.bike = False
                self.speed = SETTINGS.WALK_SPEED

    def save_player(self):
        return {
            "position": (self.position.x, self.position.y),
            "direction": self.direction,
            "team": [pkmn.save_pkmn() for pkmn in self.team],
            "inventory": self.Inventory.save_inventory(),
            "pokedollars": self.pokedollars,
            "npcsEncounter": self.npcsEncountered,
            "trainersDefeated": self.trainersDefeated,
            "collectedItems": self.collectedItems
        }

    def load_player(self, data):
        self.position = pygame.Vector2(data["position"][0], data["position"][1])
        self.direction = data["direction"]
        self.team.clear()
        for d in data["team"]:
            P = Pokemon(d["name"], d["level"])
            P.load_pokemon(d)
            self.team.append(P)
        Inv = Inventory()
        Inv.load_inventory(data["inventory"])
        self.Inventory = Inv
        self.pokedollars = data["pokedollars"]
        self.npcsEncountered = data["npcsEncounter"]
        self.trainersDefeated = data["trainersDefeated"]
        self.collectedItems = data["collectedItems"]
