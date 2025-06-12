import pygame

from game import Game

if __name__ == "__main__":
    pygame.init()

    G = Game()
    G.run()

    pygame.quit()
