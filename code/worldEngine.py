import json
import random

import pygame
import pytmx
import pyscroll

from dataManager import DataManager
from pokemon import Pokemon
from dialogManager import DialogManager
from animationManager import AnimationManager
from map import Map
from npc import NPC
from item import Item
from dynamicTile import DynamicTile
from wildOpponent import WildOpponent
from trainerOpponent import TrainerOpponent
from tool import Tool


class WorldEngine:
    def __init__(self, screen, keyboard, controller, player):
        self.Screen = screen
        self.DialogManager = DialogManager(screen, keyboard, controller)
        self.AnimationManager = AnimationManager()
        self.Player = player

        self.Map = None

        self.tilesTypes = {}
        self.dynamicsTiles = []

        self.gridMap = {}
        self.collisions = []
        self.spawns = []
        self.switches = []
        self.npcs = []
        self.items = []
        self.wildPkmnSpawn = []
        self.gate = None

        self.switchGameStateQuery = False

        self.entityLayer = 0

    def switch_map(self, map_dbsymbol):
        self.Map = Map(map_dbsymbol)
        self.Map.TmxData = pytmx.load_pygame(f"../assets/maps/{map_dbsymbol}.tmx")

        map_data = pyscroll.data.TiledMapData(self.Map.TmxData)
        self.Map.MapLayer = pyscroll.BufferedRenderer(map_data, self.Screen.display.get_size())
        self.Map.MapLayer.zoom = self.Map.TmxData.zoom
        for layer in self.Map.TmxData.layers:
            if layer.name == "entityLayer":
                self.entityLayer = self.Map.TmxData.layers.index(layer)
                break
        self.Map.Group = pyscroll.PyscrollGroup(map_layer=self.Map.MapLayer, default_layer=self.entityLayer)

        self.init_object()
        self.init_dynamics_tiles()
        self.add_entity(self.Player)

        if self.gate:
            for spawn in self.spawns:
                if spawn["map"] == self.gate["destination"] and spawn["port"] == self.gate["port"]:
                    self.Player.position = spawn["position"]
                    self.Player.move()

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
        self.check_shaking_grass()
        self.check_switch()
        self.check_bike()

        self.Map.update(self.Player)

    def init_object(self):
        self.tilesTypes.clear()
        self.dynamicsTiles.clear()
        self.collisions.clear()
        self.spawns.clear()
        self.switches.clear()
        self.npcs.clear()
        self.items.clear()
        self.wildPkmnSpawn.clear()
        DataManager.ENTITIES_DESTINATIONS.clear()

        for obj in self.Map.TmxData.objects:
            if obj.type == "collision":
                subrects = Tool.split_rect(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
                for rect in subrects:
                    self.collisions.append(rect)

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
                worldId = str(obj.dbSymbol) + str(int(obj.x)) + str(int(obj.y)) + str(self.Map.dbSymbol)
                if worldId not in self.Player.collectedItems:
                    self.items.append({"position": pygame.Vector2(obj.x, obj.y),
                                       "shown": obj.shown,
                                       "worldId": worldId,
                                       "item": Item(obj.dbSymbol)})
                    if obj.shown:
                        self.add_dynamic_tile("pokeball", obj.x, obj.y, layer=self.entityLayer-1)
                        self.collisions.append(pygame.Rect(obj.x, obj.y, 16, 16))

            elif obj.type == "wildPkmn":
                self.wildPkmnSpawn.append({"rect": pygame.Rect(obj.x, obj.y, obj.width, obj.height),
                                           "adress": obj.adress})

            elif obj.type == "tileType":
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                for subrect in Tool.split_rect(rect):
                    if obj.tileType in self.tilesTypes:
                        self.tilesTypes[obj.tileType].append(subrect)
                    else:
                        self.tilesTypes[obj.tileType] = [subrect]

    def init_dynamics_tiles(self):
        if "water" in self.tilesTypes:
            for rect in self.tilesTypes["water"]:
                self.add_dynamic_tile("water", rect.x, rect.y, layer=0)
                self.collisions.append(rect)
        if "flower" in self.tilesTypes:
            for rect in self.tilesTypes["flower"]:
                self.add_dynamic_tile("flower", rect.x, rect.y, layer=self.entityLayer-1)
        if "grass" in self.tilesTypes:
            for rect in self.tilesTypes["grass"]:
                self.add_dynamic_tile("grass", rect.x, rect.y, layer=self.entityLayer-1)
        if "bridge" in self.tilesTypes:
            for rect in self.tilesTypes["bridge"]:
                if rect in self.collisions:
                    self.collisions.remove(rect)

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

            for collision in self.collisions:
                if npc.facingTile.colliderect(collision):
                    npc.collision = True

    def check_switch(self):
        for switch in self.switches:
            if self.Player.hitbox.colliderect(switch["rect"]):
                if self.Player.stepProgression >= 12 and self.Player.facingTile.colliderect(switch["rect"]):
                    self.gate = switch
                    self.switch_map(switch["destination"])

    def check_player_interaction(self):
        if self.Player.interaction and not self.Player.inMotion:

            for npc in self.npcs:
                if self.Player.facingTile == npc.hitbox:
                    npc.facing_entity(self.Player)
                    self.Player.npcsEncountered.append(npc.dbSymbol)
                    self.DialogManager.open_dialog(self.Player, npc.dbSymbol,
                                                   context={
                                                       "spkname": npc.name,
                                                       "spklead": npc.get_active_pkmn().name if npc.get_active_pkmn()
                                                       else 0
                                                   })

                    if npc.team and npc.dbSymbol not in self.Player.trainersDefeated:
                        self.Player.Opponent = TrainerOpponent(npc)
                        self.switchGameStateQuery = True

            for item in self.items:
                spot = self.Player.facingTile if item["shown"] else self.Player.hitbox
                if spot.topleft == item["position"]:
                    self.items.remove(item)
                    if item["shown"]:
                        for collision in self.collisions:
                            if collision.topleft == item["position"]:
                                self.collisions.remove(collision)
                        for tile in self.dynamicsTiles:
                            if item["position"] == tile.position:
                                self.remove_dynamic_tile(tile)

                    self.Player.Inventory.add_item(item["item"])
                    self.Player.collectedItems.append(item["worldId"])

                    self.DialogManager.open_dialog(self.Player, "item",
                                                   context={
                                                       "itemname": item["item"].dbSymbol
                                                   })

            for tile in self.dynamicsTiles:
                if tile.dbSymbol == "water":
                    if self.Player.facingTile == tile.rect:
                        if tile.rect in self.collisions:
                            self.DialogManager.open_dialog(self.Player, "water")

    def check_ext_interaction(self):
        if not self.Player.inMotion:
            for npc in self.npcs:
                if npc.scanRange and npc.dbSymbol not in self.Player.npcsEncountered:
                    if npc.scanRect.colliderect(self.Player.hitbox):
                        if not self.check_obstacle(self.Player.hitbox, npc.hitbox):
                            self.Player.interaction = True
                            self.Player.facing_entity(npc)
                            if not npc.facingTile == self.Player.hitbox:
                                npc.move()
                            else:
                                npc.interaction = True

    def check_shaking_grass(self):
        if "grass" in self.tilesTypes:
            for rect in self.tilesTypes["grass"]:
                if self.Player.hitbox.colliderect(rect):
                    self.add_dynamic_tile("grassShaking", rect.x, rect.y, layer=self.entityLayer+1)

            for tile in self.dynamicsTiles:
                if tile.dbSymbol == "grassShaking":
                    if not self.Player.hitbox.colliderect(tile):
                        self.remove_dynamic_tile(tile)

                    elif tile.position.y < self.Player.hitbox.y:
                        self.Map.Group.change_layer(tile, self.entityLayer-1)

    def check_wild_pkmn(self):
        if not self.Player.inMotion and not self.Player.idle:
            for spawn in self.wildPkmnSpawn:
                if self.Player.hitbox.colliderect(spawn["rect"]):
                    wild_pkmn_data = json.load(open(f"../assets/data/wildPkmn/{self.Map.dbSymbol}.json"))
                    spawn_data = wild_pkmn_data[spawn["adress"]]
                    if random.random() < spawn_data["probability"]:
                        self.Player.reset_move()
                        self.Player.Keyboard.keys.clear()
                        pokemon = Tool.wild_pkmn_picker(spawn_data["pokemon"])
                        name = pokemon["name"]
                        lvl = random.randint(pokemon["lvl"][0], pokemon["lvl"][1])
                        self.Player.Opponent = WildOpponent(Pokemon(name, lvl))
                        self.switchGameStateQuery = True

    def check_bike(self):
        if self.Player.bike:
            if not self.Map.TmxData.bike:
                self.Player.switch_bike()
                self.DialogManager.open_dialog(self.Player, "bike")

    def add_entity(self, entity):
        if entity in self.Map.Group:
            return
        self.Map.Group.add(entity)
        self.Map.Group.change_layer(entity, self.entityLayer)
        entity.reset_move()
        if type(entity) is NPC:
            self.npcs.append(entity)

    def add_dynamic_tile(self, dbsymbol, x, y, layer=None):
        tile = DynamicTile(dbsymbol, x, y)
        if tile in self.Map.Group:
            return
        layer = self.entityLayer if layer is None else layer
        self.Map.Group.add(tile)
        self.Map.Group.change_layer(tile, layer)
        self.dynamicsTiles.append(tile)

    def remove_dynamic_tile(self, tile):
        self.Map.Group.remove(tile)
        self.dynamicsTiles.remove(tile)

    def check_obstacle(self, hitboxa, hitboxb):
        road = pygame.Rect.union(hitboxa, hitboxb)
        for collision in self.collisions:
            if collision.colliderect(road):
                return True
        return False

    def map_to_screen_pos(self, position):
        return self.Map.MapLayer.translate_point((position.x, position.y - 32))

    def save_map(self):
        return {
            "dbSymbol": self.Map.dbSymbol,
        }

    def load_map(self, data):
        self.switch_map(data["dbSymbol"])
