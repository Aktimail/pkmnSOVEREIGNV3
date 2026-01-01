import json
import pygame

from tool import Tool


class DynamicTile(pygame.sprite.Sprite):
    def __init__(self, dbsymbol, x, y):
        super().__init__()
        self.dbSymbol = dbsymbol
        data = json.load(open(f"../assets/data/dynamicsTiles/{dbsymbol}.json"))
        self.nbFrames = data["nbFrames"]
        self.framesDuration = data["framesDuration"]
        if type(self.framesDuration) is int:
            self.framesDuration = [self.framesDuration for _ in range(self.nbFrames)]
        self.frameIdx = 0
        self.loop = data["loop"]

        self.spritesheet = pygame.image.load(f"../assets/graphics/dynamicTiles/{dbsymbol}.png")
        self.position = pygame.Vector2(x, y)
        self.image = Tool.split_anim_spritesheet(self.spritesheet, self.nbFrames)[self.frameIdx]
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position

        self.counter = 0

    def sprite_update(self):
        self.image = Tool.split_anim_spritesheet(self.spritesheet, self.nbFrames)[self.frameIdx]

        if self.nbFrames > 1:
            self.counter += 1
            if self.counter >= self.framesDuration[self.frameIdx]:
                self.frameIdx += 1
                self.counter = 0
                if self.frameIdx >= self.nbFrames:
                    if self.loop:
                        self.frameIdx = 0
                    elif not self.loop:
                        self.frameIdx -= 1

    def update(self):
        self.sprite_update()
