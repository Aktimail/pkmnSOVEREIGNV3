import pygame

from tool import Tool


class DynamicTile(pygame.sprite.Sprite):
    def __init__(self, spritesheet, nb_frames, hitbox, x, y):
        super().__init__()
        self.spritesheet = pygame.image.load(f"../assets/graphics/dynamicTiles/{spritesheet}.png")
        self.nb_frames = nb_frames
        self.position = pygame.Vector2(x, y)
        self.image = Tool.split_anim_spritesheet(self.spritesheet, self.nb_frames)[0]
        self.rect = self.image.get_rect()
        self.hitbox = self.rect if hitbox else None

    def sprite_update(self):
        self.image = Tool.split_anim_spritesheet(self.spritesheet, self.nb_frames)[0]
        self.rect = self.image.get_rect()
        self.hitbox.topleft = self.position
        self.rect.midbottom = self.hitbox.midbottom

    def update(self):
        self.sprite_update()
