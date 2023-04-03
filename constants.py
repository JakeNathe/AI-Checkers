import pygame

WIDTH = 800
HEIGHT = 800
ROWS = 8
COLUMNS = 8
SQUARE_SIZE = WIDTH//COLUMNS
PADDING = 13
OUTLINE = 3
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (85, 80, 85)
GREEN = (135, 255, 0)
TAN = (190, 160, 120)
BROWN = (92, 64, 51)

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
CROWN = pygame.transform.scale(pygame.image.load('crown.png'), (44.5, 25.6))

