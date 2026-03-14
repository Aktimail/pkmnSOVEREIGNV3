import pytmx
import pyscroll

import pygame

from worldEngine import WorldEngine
from worldEnv import WorldEnv
from map import Map
from dialogManager import DialogManager
from animationManager import AnimationManager
from npc import NPC
from item import Item
from tool import Tool


class WorldManager:
    def __init__(self, screen, keyboard, controller, player):
        self.Screen = screen
        self.DialogManager = DialogManager(screen, keyboard, controller)
        self.AnimationManager = AnimationManager()
        self.Player = player

        self.Env = WorldEnv()
        self.Engine = WorldEngine(player, self.Env)
        self.Map = None

        self.switchGameStateQuery = False

    def switch_map(self, map_dbsymbol):
        self.Map = Map(map_dbsymbol)
        self.Map.TmxData = pytmx.load_pygame(f"../assets/maps/{map_dbsymbol}.tmx")

        map_data = pyscroll.data.TiledMapData(self.Map.TmxData)
        self.Map.MapLayer = pyscroll.BufferedRenderer(map_data, self.Screen.display.get_size())
        self.Map.MapLayer.zoom = self.Map.TmxData.zoom
        for layer in self.Map.TmxData.layers:
            if layer.name == "entityLayer":
                self.Env.entityLayer = self.Map.TmxData.layers.index(layer)
                break
        self.Map.Group = pyscroll.PyscrollGroup(map_layer=self.Map.MapLayer, default_layer=self.Env.entityLayer)

        self.init_object()
        self.init_dynamics_tiles()
        self.Map.add_entity(self.Env, self.Player)

        if self.Env.gate:
            for spawn in self.Env.spawns:
                if spawn["map"] == self.Env.gate["destination"] and spawn["port"] == self.Env.gate["port"]:
                    self.Player.position = spawn["position"]
                    self.Player.move()

        if not self.Map.TmxData.bike:
            if self.Player.bike:
                self.Player.switch_bike()

    def init_object(self):
        self.Env.clear()

        for obj in self.Map.TmxData.objects:
            if obj.type == "collision":
                subrects = Tool.split_rect(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
                for rect in subrects:
                    self.Env.collisions.append(rect)

            elif obj.type == "spawn":
                self.Env.spawns.append({"position": pygame.Vector2(obj.x, obj.y),
                                        "map": obj.map,
                                        "port": obj.port
                                        })

            elif obj.type == "switch":
                self.Env.switches.append({"rect": pygame.Rect(obj.x, obj.y, obj.width, obj.height),
                                          "destination": obj.destination,
                                          "port": obj.port
                                          })

            elif obj.type == "npc":
                self.Map.add_entity(self.Env, NPC(self.Screen, obj.name, obj.x, obj.y))

            elif obj.type == "npcPath":
                for npc in self.Env.npcs:
                    if npc.dbSymbol == obj.npc_dbsymbol:
                        npc.checkpoints[obj.checkpoint] = pygame.Rect(obj.x, obj.y, 16, 16)

            elif obj.type == "item":
                worldId = str(obj.dbSymbol) + str(int(obj.x)) + str(int(obj.y)) + str(self.Map.dbSymbol)
                if worldId not in self.Player.collectedItems:
                    self.Env.items.append({"position": pygame.Vector2(obj.x, obj.y),
                                           "shown": obj.shown,
                                           "worldId": worldId,
                                           "item": Item(obj.dbSymbol)})
                    if obj.shown:
                        self.Map.add_dynamic_tile(self.Env, "pokeball", obj.x, obj.y, layer=self.Env.entityLayer - 1)
                        self.Env.collisions.append(pygame.Rect(obj.x, obj.y, 16, 16))

            elif obj.type == "wildPkmn":
                self.Env.wildPkmnSpawn.append({"rect": pygame.Rect(obj.x, obj.y, obj.width, obj.height),
                                               "adress": obj.adress})

            elif obj.type == "tileType":
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                for subrect in Tool.split_rect(rect):
                    if obj.tileType in self.Env.tilesTypes:
                        self.Env.tilesTypes[obj.tileType].append(subrect)
                    else:
                        self.Env.tilesTypes[obj.tileType] = [subrect]

    def init_dynamics_tiles(self):
        if "water" in self.Env.tilesTypes:
            for rect in self.Env.tilesTypes["water"]:
                self.Map.add_dynamic_tile(self.Env, "water", rect.x, rect.y, layer=0)
                self.Env.collisions.append(rect)
        if "flower" in self.Env.tilesTypes:
            for rect in self.Env.tilesTypes["flower"]:
                self.Map.add_dynamic_tile(self.Env, "flower", rect.x, rect.y, layer=self.Env.entityLayer - 1)
        if "grass" in self.Env.tilesTypes:
            for rect in self.Env.tilesTypes["grass"]:
                self.Map.add_dynamic_tile(self.Env, "grass", rect.x, rect.y, layer=self.Env.entityLayer - 1)
        if "bridge" in self.Env.tilesTypes:
            for rect in self.Env.tilesTypes["bridge"]:
                if rect in self.Env.collisions:
                    self.Env.collisions.remove(rect)

    def update(self):
        self.Map.render(self.Screen)

        if self.DialogManager.reading:
            self.DialogManager.update()
            return

        if self.Env.destination:
            self.switch_map(self.Env.destination)
            self.Env.destination = None

        self.Engine.check_collisions()
        self.Engine.check_ext_interaction()
        self.Engine.check_npc_interaction(self.DialogManager)
        self.Engine.check_item_interaction(self.Map, self.DialogManager)
        self.Engine.check_tile_interaction(self.DialogManager)
        self.Engine.check_wild_pkmn(self.Map)
        self.Engine.check_shaking_grass(self.Map)
        self.Engine.check_switch()
        self.Engine.check_bike(self.Map, self.DialogManager)

        self.Map.update(self.Player)

    def save_map(self):
        return {
            "dbSymbol": self.Map.dbSymbol,
        }

    def load_map(self, data):
        self.switch_map(data["dbSymbol"])

    def map_to_screen_pos(self, position):
        return self.Map.MapLayer.translate_point((position.x, position.y - 32))
