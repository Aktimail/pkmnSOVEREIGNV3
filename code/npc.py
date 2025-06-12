import pygame
import json

from entity import Entity
from pokemon import Pokemon


class NPC(Entity):
    def __init__(self, screen, dbsymbol, x, y):
        super().__init__(screen, dbsymbol, x, y)
        data = json.load(open(f"../assets/data/npcs/{dbsymbol}.json"))

        self.dbSymbol = data["dbsymbol"]
        self.name = data["name"]
        self.klass = data["klass"]

        self.spritesheet = f"../assets/graphics/spritesheets/{data["spritesheet"]}.png"
        self.sprite_update()

        if "team" in data:
            self.team = self.init_team(data["team"])

        self.direction = data["direction"]

        self.scanRange = data["scan"] if "scan" in data else None
        self.scanRect = pygame.Rect(0, 0, 0, 0)

        self.checkpoints = {1: pygame.Rect(self.position.x, self.position.y, 16, 16)}
        self.checkpointIdx = 1

    @staticmethod
    def init_team(team):
        convert_team = []
        for pkmn in team:
            if "mod" in pkmn:
                convert_team.append(Pokemon(pkmn["name"], pkmn["lvl"], mod=pkmn["mod"]))
            else:
                convert_team.append(Pokemon(pkmn["name"], pkmn["lvl"]))
        return convert_team

    def update(self):
        self.update_scan_rect()
        self.auto_move()
        super().update()

    def update_scan_rect(self):
        if self.scanRange:
            if self.direction == "up":
                self.scanRect = pygame.Rect(
                    self.position.x, self.position.y - 16 * self.scanRange, 16, 16 * self.scanRange)
            if self.direction == "down":
                self.scanRect = pygame.Rect(self.position.x, self.position.y + 16, 16, 16 * self.scanRange)
            if self.direction == "right":
                self.scanRect = pygame.Rect(self.position.x + 16, self.position.y, 16 * self.scanRange, 16)
            if self.direction == "left":
                self.scanRect = pygame.Rect(
                    self.position.x - 16 * self.scanRange, self.position.y, 16 * self.scanRange, 16)

    def auto_move(self):
        if not self.interaction and len(self.checkpoints) > 1:
            cc_idx = self.checkpointIdx
            nc_idx = self.checkpointIdx + 1

            if nc_idx > len(self.checkpoints):
                nc_idx = 1

            current_checkpoint = self.checkpoints[cc_idx]
            next_checkpoint = self.checkpoints[nc_idx]

            if current_checkpoint.y - next_checkpoint.y > 0:
                self.move("up")
            elif current_checkpoint.y - next_checkpoint.y < 0:
                self.move("down")
            elif current_checkpoint.x - next_checkpoint.x > 0:
                self.move("left")
            elif current_checkpoint.x - next_checkpoint.x < 0:
                self.move("right")

            if self.hitbox.colliderect(next_checkpoint):
                self.checkpointIdx = nc_idx
