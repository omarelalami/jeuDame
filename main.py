import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN
from game import Game

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
HIGH = (160, 190, 255)

NORTHWEST = "northwest"
NORTHEAST = "northeast"
SOUTHWEST = "southwest"
SOUTHEAST = "southeast"







def main():
    game = Game()
    game.setup()
    while True:
        game.event_loop()
        game.update()

if __name__ == "__main__":
    main()
