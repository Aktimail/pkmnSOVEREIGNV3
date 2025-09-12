import pygame

from settings import SETTINGS


class Screen:
    def __init__(self):
        self.display = pygame.display.set_mode(SETTINGS.DISPLAY_SIZE)

        self.clock = pygame.time.Clock()
        self.framerate = SETTINGS.FRAMERATE
        self.deltaTime = 0

    def update(self):
        pygame.display.flip()
        self.clock.tick(self.framerate)
        self.display.fill((0, 0, 0))
        self.deltaTime = self.clock.get_time()

    def get_size(self):
        return self.display.get_size()

    def get_rect(self):
        return self.display.get_rect()
