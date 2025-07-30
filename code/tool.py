import pygame
import random


class Tool:
    @staticmethod
    def split_entity_spritesheet(spritesheet):
        all_images = {"down": [],
                      "left": [],
                      "right": [],
                      "up": []
                      }
        width = spritesheet.get_width() // 4
        height = spritesheet.get_height() // 4
        for j, k in enumerate(all_images.keys()):
            for i in range(4):
                all_images[k].append(spritesheet.subsurface(pygame.Rect(i * width, j * height, width, height)))
        return all_images

    @staticmethod
    def split_anim_spritesheet(spritesheet, nb_frames):
        frames = []
        frame_width = spritesheet.get_width() // nb_frames
        frame_height = spritesheet.get_height()
        for i in range(nb_frames):
            frames.append(spritesheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height)))
        return frames

    @staticmethod
    def split_rect(rect, subrect_width=16, subrect_height=16):
        all_rect = []
        nb_vert_split = rect.width // subrect_width
        nb_horizon_split = rect.height // subrect_height
        for i in range(nb_vert_split):
            x = rect.x + i * 16
            for j in range(nb_horizon_split):
                y = rect.y + j * 16
                all_rect.append(pygame.Rect(x, y, subrect_width, subrect_height))
        return all_rect

    @staticmethod
    def blit_tiers(surface, color, resolution=None):
        if resolution:
            width = resolution[0]
            height = resolution[1]
        else:
            width = surface.get_width()
            height = surface.get_height()

        pygame.draw.rect(surface, color, pygame.Rect(width / 3, 0, 2, height))
        pygame.draw.rect(surface, color, pygame.Rect((width / 3) * 2, 0, 2, height))
        pygame.draw.rect(surface, color, pygame.Rect(0, height / 3, width, 2))
        pygame.draw.rect(surface, color, pygame.Rect(0, (height / 3) * 2, width, 2))

    @staticmethod
    def wild_pkmn_picker(tab: dict):
        n = random.random()
        p = 0
        for i in range(len(tab)):
            if p <= n < p + tab[i]["probability"]:
                return tab[i]
            p += tab[i]["probability"]
        return tab[0]
