import pygame


class Controller:
    def __init__(self):
        self.keybinds = {
            "up": pygame.K_z,
            "down": pygame.K_s,
            "left": pygame.K_q,
            "right": pygame.K_d,
            "run": pygame.K_LSHIFT,
            "bike": pygame.K_b,
            "interact": pygame.K_SPACE,
            "menu": pygame.K_ESCAPE
        }
