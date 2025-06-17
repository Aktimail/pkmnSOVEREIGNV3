import json
import random

import pygame
import pytmx
import pyscroll

from pokemon import Pokemon
from dialogManager import DialogManager
from animationManager import AnimationManager
from map import Map
from npc import NPC
from item import Item
from dynamicTile import DynamicTile
from data import DATA
from tool import Tool


class WorldEngine:
    def __init__(self, screen, keyboard, controller, player):
        self.Screen = screen
        self.DialogManager = DialogManager(screen, keyboard, controller)
        self.AnimationManager = AnimationManager()
        self.Player = player

        self.Map = None

        self.tilesTypes = {
            "grass": [],
            "water": [],
        }
        self.dynamicTiles = []

        self.collisions = []
        self.spawns = []
        self.switches = []
        self.npcs = []
        self.items = []
        self.collectedItems = []
        self.wildPkmnSpawn = []
        self.gate = None

        self.switch_game_state_query = False

    def switch_map(self, map_dbsymbol):
        self.Map = Map(map_dbsymbol)
        self.Map.TmxData = pytmx.load_pygame(f"../assets/maps/{map_dbsymbol}.tmx")

        map_data = pyscroll.data.TiledMapData(self.Map.TmxData)
        self.Map.MapLayer = pyscroll.BufferedRenderer(map_data, self.Screen.display.get_size())
        self.Map.MapLayer.zoom = self.Map.TmxData.zoom

        entity_layer = 50
        self.Map.Group = pyscroll.PyscrollGroup(map_layer=self.Map.MapLayer, default_layer=entity_layer)

        self.init_object()
        self.add_entity(self.Player)

        if self.gate:
            for spawn in self.spawns:
                if spawn["map"] == self.gate["destination"] and spawn["port"] == self.gate["port"]:
                    self.Player.position = spawn["position"]

        if not self.Map.TmxData.bike:
            if self.Player.bike:
                self.Player.switch_bike()

    def update(self):
        self.Map.render(self.Screen)

        if self.DialogManager.reading:
            self.DialogManager.update()
            return

        self.check_collisions()
        self.check_ext_interaction()
        self.check_player_interaction()
        self.check_wild_pkmn()
        self.check_switch()
        self.check_bike()

        self.Map.update(self.Player)

    def init_object(self):
        for type in self.tilesTypes:
            self.tilesTypes[type].clear()
        self.dynamicTiles.clear()
        self.collisions.clear()
        self.spawns.clear()
        self.switches.clear()
        self.npcs.clear()
        self.items.clear()
        self.wildPkmnSpawn.clear()
        DATA.ENTITIES_DESTINATIONS.clear()

        for obj in self.Map.TmxData.objects:
            if obj.type == "collision":
                self.collisions.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

            elif obj.type == "spawn":
                self.spawns.append({"position": pygame.Vector2(obj.x, obj.y),
                                    "map": obj.map,
                                    "port": obj.port
                                    })

            elif obj.type == "switch":
                self.switches.append({"rect": pygame.Rect(obj.x, obj.y, obj.width, obj.height),
                                      "destination": obj.destination,
                                      "port": obj.port
                                      })

            elif obj.type == "npc":
                self.add_entity(NPC(self.Screen, obj.name, obj.x, obj.y))

            elif obj.type == "npcPath":
                for npc in self.npcs:
                    if npc.dbSymbol == obj.npc_dbsymbol:
                        npc.checkpoints[obj.checkpoint] = pygame.Rect(obj.x, obj.y, 16, 16)

            elif obj.type == "item":
                if obj.worldId not in self.collectedItems:
                    self.items.append({"position": pygame.Vector2(obj.x, obj.y),
                                       "shown": obj.shown,
                                       "worldId": obj.worldId,
                                       "item": Item(obj.name)})
                    if obj.shown:
                        self.add_dynamic_tile(DynamicTile("pokeball", 1, True, obj.x, obj.y))
                        self.collisions.append(pygame.Rect(obj.x, obj.y, 16, 16))

            elif obj.type == "wildPkmn":
                self.wildPkmnSpawn.append({"rect": pygame.Rect(obj.x, obj.y, obj.width, obj.height),
                                           "adress": obj.adress})

            elif obj.type == "tileType":
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                for subrect in Tool.split_rect(rect):
                    self.tilesTypes[obj.tileType].append(subrect)

    def check_collisions(self):
        self.Player.collision = False

        for collision in self.collisions:
            if self.Player.facingTile.colliderect(collision):
                self.Player.collision = True

        for npc in self.npcs:
            npc.collision = False
            if self.Player.facingTile.colliderect(npc.hitbox):
                self.Player.collision = True
            if npc.facingTile.colliderect(self.Player.hitbox):
                npc.collision = True

    def check_switch(self):
        for switch in self.switches:
            if self.Player.hitbox.colliderect(switch["rect"]):
                if self.Player.stepProgression >= 12:
                    self.gate = switch
                    self.switch_map(switch["destination"])

    def check_player_interaction(self):
        if self.Player.interaction and not self.Player.inMotion:

            for npc in self.npcs:
                if self.Player.facingTile == npc.hitbox:
                    npc.facing_entity(self.Player)
                    npc.interaction = True
                    self.Player.npcs_encountered.append(npc.dbSymbol)
                    self.DialogManager.open_dialog(self.Player, npc.dbSymbol, npc)

                    if npc.team and npc.dbSymbol not in self.Player.trainers_defeated:
                        self.Player.Opponent = npc
                        self.switch_game_state_query = True

            for item in self.items:
                spot = self.Player.facingTile if item["shown"] else self.Player.hitbox
                if spot.topleft == item["position"]:
                    self.items.remove(item)
                    if item["shown"]:
                        for collision in self.collisions:
                            if collision.topleft == item["position"]:
                                self.collisions.remove(collision)
                        for tile in self.dynamicTiles:
                            if item["position"] == tile.position:
                                self.remove_dynamic_tile(tile)
                                print("a")

                    self.Player.Inventory.add_item(item["item"])
                    self.collectedItems.append(item["worldId"])

                    self.DialogManager.open_dialog(self.Player, "item", item=item["item"])

    def check_ext_interaction(self):
        if not self.Player.inMotion:
            for npc in self.npcs:
                if npc.scanRange and npc.dbSymbol not in self.Player.npcs_encountered:
                    if npc.scanRect.colliderect(self.Player.hitbox):
                        if not self.check_obstacle(self.Player.hitbox, npc.hitbox):
                            self.Player.interaction = True
                            self.Player.facing_entity(npc)
                            if not npc.facingTile == self.Player.hitbox:
                                npc.move()

    def check_wild_pkmn(self):
        for spawn in self.wildPkmnSpawn:
            if self.Player.hitbox.colliderect(spawn["rect"]):
                spawn_data = json.load(open(f"../assets/data/wildPkmn/{self.Map.dbSymbol}.json"))
                spawn_data = spawn_data[spawn["adress"]]
                if random.random() < spawn_data["probability"]:
                    pokemon = Tool.random_picker(spawn_data["pokemon"])
                    name = pokemon["name"]
                    lvl = random.randint(pokemon["lvl"][0], pokemon["lvl"][1])
                    self.Player.Opponent = Pokemon(name, lvl)
                    self.switch_game_state_query = True

    def check_bike(self):
        if self.Player.bike:
            if not self.Map.TmxData.bike:
                self.Player.switch_bike()
                self.DialogManager.open_dialog(self.Player, "bike")

    def add_entity(self, entity):
        self.Map.Group.add(entity)
        entity.reset_move()
        if type(entity) is NPC:
            self.npcs.append(entity)

    def add_dynamic_tile(self, tile):
        self.Map.Group.add(tile)
        self.dynamicTiles.append(tile)

    def remove_dynamic_tile(self, tile):
        self.Map.Group.remove(tile)
        self.dynamicTiles.remove(tile)

    def check_obstacle(self, hitboxa, hitboxb):
        road = pygame.Rect.union(hitboxa, hitboxb)
        for collision in self.collisions:
            if collision.colliderect(road):
                return True
        return False

    def map_to_screen_pos(self, position):
        return self.Map.MapLayer.translate_point((position.x, position.y - 32))
