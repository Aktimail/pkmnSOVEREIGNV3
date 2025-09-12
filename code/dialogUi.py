import pygame

from settings import SETTINGS


class DialogUi:
    def __init__(self, screen):
        self.Screen = screen

    def render_box(self):
        panel_pos = (100, 550)
        panel_size = (SETTINGS.DISPLAY_SIZE[0] - 200, 150)

        panel = pygame.image.load("../assets/graphics/dialogs/dialog_box.png")
        panel = pygame.transform.scale(panel, panel_size)

        self.Screen.display.blit(panel, panel_pos)

    def render_skip_icon(self):
        icon = pygame.image.load("../assets/graphics/dialogs/skip_icon.png")
        self.Screen.display.blit(icon, (0, 0))
