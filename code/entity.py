import pygame

from settings import SETTINGS
from data import DATA
from tool import Tool


class Entity(pygame.sprite.Sprite):
    def __init__(self, screen, name, x, y):
        super().__init__()
        self.Screen = screen
        self.name = name
        self.dbSymbol = None
        self.position = pygame.math.Vector2(x, y)

        self.spritesheet = None
        self.image = None
        self.rect = None

        self.team = []
        self.worldCompo = None
        self.Opponent = None
        self.battle_choice = None

        self.direction = "down"
        self.stepProgression = 0
        self.speed = SETTINGS.WALK_SPEED
        self.facingTile = pygame.Rect(0, 0, 16, 16)
        self.lastTile = None

        self.spriteIdx = 0
        self.animCycle = 0

        self.hitbox = pygame.Rect(0, 0, 16, 16)

        self.pokedollars = 0

        self.collision = False
        self.freeze = False
        self.inMotion = False
        self.wasInMotion = False
        self.justMoved = False
        self.interaction = False
        self.alert = False
        self.chasing = False

    def sprite_update(self):
        spritesheet_img = pygame.image.load(self.spritesheet)
        self.image = Tool.split_spritesheet(spritesheet_img)[self.direction][self.spriteIdx]
        self.rect = self.image.get_rect()
        self.hitbox.topleft = self.position
        self.rect.midbottom = self.hitbox.midbottom

    def update(self):
        if self.chasing:
            self.move()
        self.movement_update()
        self.facing_tile_update()
        self.animation_cycle()
        self.sprite_update()
        self.check_just_moved()

    def check_just_moved(self):
        self.justMoved = self.wasInMotion and not self.inMotion
        self.wasInMotion = self.inMotion

    def reset_move(self):
        self.inMotion = False
        self.stepProgression = 0
        while self.position.x % 16:
            self.position.x -= 1
        while self.position.y % 16:
            self.position.y -= 1

    def move(self, direction=None):
        if direction is None:
            direction = self.direction
        if not self.interaction and not self.inMotion:
            if self.direction == direction:
                if not self.collision:
                    if self.grid_check():
                        self.inMotion = True
            else:
                self.direction = direction

    def movement_update(self):
        if self.inMotion:
            self.stepProgression += self.speed
            if self.direction == "left":
                self.position.x -= self.speed
            elif self.direction == "right":
                self.position.x += self.speed
            elif self.direction == "up":
                self.position.y -= self.speed
            elif self.direction == "down":
                self.position.y += self.speed

            if self.stepProgression >= 16:
                self.stepProgression = 0
                self.inMotion = False

    def animation_cycle(self):
        if self.inMotion:
            self.freeze = False
            self.animCycle += 1
            if not self.animCycle % 8:
                self.spriteIdx += 1

            if self.spriteIdx > 3:
                self.spriteIdx = 0
            if self.animCycle >= 16:
                self.animCycle = 0

        if not self.inMotion:
            if self.freeze:
                if self.spriteIdx % 2:
                    self.spriteIdx += 1
                    if self.spriteIdx > 3:
                        self.spriteIdx = 0
            self.freeze = True

    def facing_tile_update(self):
        if not self.inMotion:
            self.facingTile.topleft = self.position
            if self.direction == "left":
                self.facingTile.x -= 16
            if self.direction == "right":
                self.facingTile.x += 16
            if self.direction == "up":
                self.facingTile.y -= 16
            if self.direction == "down":
                self.facingTile.y += 16

    def facing_entity(self, entity):
        if not self.inMotion:
            direction = self.direction
            if entity.position.x - self.position.x > 0:
                self.direction = "right"
            if entity.position.x - self.position.x < 0:
                self.direction = "left"
            if entity.position.y - self.position.y > 0:
                self.direction = "down"
            if entity.position.y - self.position.y < 0:
                self.direction = "up"

            if self.direction == direction:
                return True
            return False

    def grid_check(self):
        if not (self.facingTile.x, self.facingTile.y) in DATA.ENTITIES_DESTINATIONS.values():
            DATA.ENTITIES_DESTINATIONS[self.dbSymbol] = (self.facingTile.x, self.facingTile.y)
            return True
        return False

    def fight(self, move, battle_data):
        self.get_lead().attack(move, battle_data)

    def switch(self, i):
        self.get_lead().boost = {"atk": 0, "defe": 0, "aspe": 0, "dspe": 0, "spd": 0, "acc": 0, "eva": 0}
        self.team[0], self.team[i] = self.team[i], self.team[0]

    def lost(self):
        for pkmn in self.team:
            if not pkmn.is_ko():
                return False
        return True

    def get_lead(self):
        return self.team[0]

    def get_back_world_comp(self):
        world_compo = []
        for name in self.worldCompo:
            for pkmn in self.team:
                if pkmn.name == name:
                    world_compo.append(pkmn)
                    break
        return world_compo

    def is_aligned(self):
        if self.position.x % 16:
            return False
        if self.position.y % 16:
            return False
        return True