import json
import random

import pygame

from tool import Tool


class WorldEngine:
    def __init__(self, player, env):
        self.Player = player
        self.Env = env

    def check_collisions(self):
        self.Player.collision = False

        for collision in self.Env.collisions:
            if self.Player.facingTile.colliderect(collision):
                self.Player.collision = True

        for npc in self.Env.npcs:
            npc.collision = False
            if self.Player.facingTile.colliderect(npc.hitbox):
                self.Player.collision = True
            if npc.facingTile.colliderect(self.Player.hitbox):
                npc.collision = True

            for collision in self.Env.collisions:
                if npc.facingTile.colliderect(collision):
                    npc.collision = True

    def check_switch(self):
        for switch in self.Env.switches:
            if self.Player.hitbox.colliderect(switch["rect"]):
                if self.Player.stepProgression >= 12 and self.Player.facingTile.colliderect(switch["rect"]):
                    self.Env.gate = switch
                    self.Env.detination = switch["destination"]

    def check_npc_interaction(self, msgbox):
        if self.Player.interaction and self.Player.idle:
            for npc in self.Env.npcs:
                if self.Player.facingTile == npc.hitbox:
                    npc.facing_entity(self.Player)
                    self.Player.npcsEncountered.append(npc.dbSymbol)
                    msgbox.open_dialog(self.Player, npc.dialogDbSymbol, speaker=npc)

                    if npc.team and npc.dbSymbol not in self.Player.trainersDefeated:
                        self.switchGameStateQuery = True

    def check_item_interaction(self, map, msgbox):
        if self.Player.interaction and not self.Player.inMotion:
            for item in self.Env.items:
                spot = self.Player.facingTile if item["shown"] else self.Player.hitbox
                if spot.topleft == item["position"]:
                    self.Env.items.remove(item)
                    if item["shown"]:
                        for collision in self.Env.collisions:
                            if collision.topleft == item["position"]:
                                self.Env.collisions.remove(collision)
                        for tile in self.Env.dynamicsTiles:
                            if item["position"] == tile.position:
                                map.remove_dynamic_tile(self.Env, tile)

                    self.Player.Inventory.add_item(item["item"])
                    self.Player.collectedItems.append(item["worldId"])

                    msgbox.open_dialog(self.Player, "itemFound", item=item["item"])

    def check_tile_interaction(self, msgbox):
        if self.Player.interaction and not self.Player.inMotion:
            for tile in self.Env.dynamicsTiles:
                if tile.dbSymbol == "water":
                    if self.Player.facingTile == tile.rect:
                        if tile.rect in self.Env.collisions:
                            msgbox.open_dialog(self.Player, "water")

    def check_ext_interaction(self):
        if not self.Player.inMotion:
            for npc in self.Env.npcs:
                if npc.scanRange and npc.dbSymbol not in self.Player.npcsEncountered:
                    if npc.scanRect.colliderect(self.Player.hitbox):
                        if not self.check_obstacle(self.Player.hitbox, npc.hitbox):
                            self.Player.interaction = True
                            self.Player.facing_entity(npc)
                            if not npc.facingTile == self.Player.hitbox:
                                npc.move()
                            else:
                                npc.interaction = True

    def check_shaking_grass(self, map):
        if "grass" in self.Env.tilesTypes:
            for rect in self.Env.tilesTypes["grass"]:
                if self.Player.hitbox.colliderect(rect):
                    map.add_dynamic_tile(self.Env, "grassShaking", rect.x, rect.y, layer=self.Env.entityLayer+1)

            for tile in self.Env.dynamicsTiles:
                if tile.dbSymbol == "grassShaking":
                    if not self.Player.hitbox.colliderect(tile):
                        map.remove_dynamic_tile(self.Env, tile)

                    elif tile.position.y < self.Player.hitbox.y:
                        map.Group.change_layer(tile, self.Env.entityLayer-1)

    def check_wild_pkmn(self, map):
        if not self.Player.inMotion and not self.Player.idle:
            for spawn in self.Env.wildPkmnSpawn:
                if self.Player.hitbox.colliderect(spawn["rect"]):
                    wild_pkmn_data = json.load(open(f"../assets/data/wildPkmn/{map.dbSymbol}.json"))
                    spawn_data = wild_pkmn_data[spawn["adress"]]
                    if random.random() < spawn_data["probability"]:
                        self.Player.reset_move()
                        self.Player.Keyboard.keys.clear()
                        pokemon = Tool.wild_pkmn_picker(spawn_data["pokemon"])
                        name = pokemon["name"]
                        lvl = random.randint(pokemon["lvl"][0], pokemon["lvl"][1])
                        self.switchGameStateQuery = True

    def check_bike(self, map, msgbox):
        if self.Player.bike:
            if not map.TmxData.bike:
                self.Player.switch_bike()
                msgbox.open_dialog(self.Player, "bike")

    def check_obstacle(self, hitboxa, hitboxb):
        road = pygame.Rect.union(hitboxa, hitboxb)
        for collision in self.Env.collisions:
            if collision.colliderect(road):
                return True
        return False
