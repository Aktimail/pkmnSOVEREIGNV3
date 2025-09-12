import pygame

from settings import SETTINGS
from data import DATA
from tool import Tool


class Entity(pygame.sprite.Sprite):
    def __init__(self, screen, name, x, y):
        super().__init__()
        self.Screen = screen
        self.dbSymbol = None
        self.name = name
        self.position = pygame.math.Vector2(x, y)

        self.spritesheet = None
        self.image = None
        self.rect = None
        self.shadow = pygame.image.load("../assets/graphics/spritesheets/shadow.png")

        self.team = []
        self.worldCompo = None
        self.Opponent = None
        self.battle_choice = None
        self.publicData = {}

        self.direction = "down"
        self.stepProgression = 0
        self.speed = SETTINGS.WALK_SPEED
        self.facingTile = pygame.Rect(0, 0, 16, 16)
        self.lastTile = None

        self.spriteIdx = 0
        self.animCycle = 0

        self.hitbox = pygame.Rect(0, 0, 16, 16)

        self.pokedollars = 0

        self.inMotion = False
        self.idle = False
        self.collision = False
        self.idleCounter = 0
        self.interaction = False

    def sprite_update(self):
        shadow = self.shadow.copy()
        spritesheet_img = shadow
        spritesheet_img.blit(pygame.image.load(self.spritesheet), (0, 0))
        self.image = Tool.split_entity_spritesheet(spritesheet_img)[self.direction][self.spriteIdx]
        self.rect = self.image.get_rect()
        self.hitbox.topleft = self.position
        self.rect.midbottom = self.hitbox.midbottom

    def update(self):
        self.movement_update()
        self.idle_update()
        self.facing_tile_update()
        self.animation_cycle()
        self.sprite_update()

    def idle_update(self):
        if not self.inMotion:
            self.idleCounter += 1
            if self.idleCounter >= 2:
                self.idle = True
        elif self.inMotion:
            self.idleCounter = 0
            self.idle = False

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
        if not self.idle:
            self.animCycle += 1
            if not self.animCycle % 8:
                self.spriteIdx += 1

            if self.spriteIdx > 3:
                self.spriteIdx = 0
            if self.animCycle >= 16:
                self.animCycle = 0

        elif self.idle:
            if self.spriteIdx % 2:
                self.spriteIdx += 1
                if self.spriteIdx > 3:
                    self.spriteIdx = 0

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

    def fight(self, move, target, context):
        self.get_active_pkmn().attack(move, target, context)

    def switch(self, pkmn):
        idx = self.team.index(pkmn)
        self.get_active_pkmn().boosts = {k: 0 for k in self.get_active_pkmn().boosts}
        self.team[0], self.team[idx] = self.team[idx], self.team[0]

    def lost(self):
        for pkmn in self.team:
            if not pkmn.is_ko():
                return False
        return True

    def get_active_pkmn(self):
        return self.team[0] if self.team else 0

    def get_back_world_comp(self):
        world_compo = []
        for name in self.worldCompo:
            for pkmn in self.team:
                if pkmn.name == name:
                    world_compo.append(pkmn)
                    break
        self.team = world_compo

    def is_aligned(self):
        if self.position.x % 16:
            return False
        if self.position.y % 16:
            return False
        return True
