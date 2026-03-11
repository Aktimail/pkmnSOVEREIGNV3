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

    def render_dialog(self, dialog, x, y):
        for idx, line in enumerate(dialog.text[dialog.txt_idx]):
            if dialog.line_idx == idx:
                z = dialog.txt_gap if dialog.line_idx else 0
                text = dialog.font.render(line[:int(dialog.txt_progression)], True, dialog.txt_color)
                self.Screen.display.blit(text, (x, y + z))
            elif dialog.line_idx > idx >= dialog.line_idx - 1:
                text = dialog.font.render(line, True, dialog.txt_color)
                self.Screen.display.blit(text, (x, y))

        dialog.txt_progression += dialog.txt_spd
        if dialog.txt_progression >= len(dialog.text[dialog.txt_idx][dialog.line_idx]):
            dialog.writing = False
            if dialog.line_idx < len(dialog.text[dialog.txt_idx]) - 1 and dialog.line_idx < 1:
                dialog.txt_progression = 0
                dialog.line_idx += 1
