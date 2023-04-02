# Date: 3/30/2023
# Description:  Creates a 8x8 standard checkers board with 2 players. Players are able to move around board and capture
#               opponents pieces. Pieces can be upgraded to a "King" by making it to the opposite end of the board.
#               If a piece is able to be captured, the player must do so. The game is won when all the opponents pieces
#               are captured.

import pygame
from constants import *
from game import *

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")


def get_position_from_mouse(position):
    x, y = position
    row = y // SQUARE_SIZE
    column = x // SQUARE_SIZE
    return row, column


def main():
    """Sets up event loop to run the game"""
    clock = pygame.time.Clock()
    current_game = Game(WINDOW)
    run = True

    # runs until the game is quit
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                row, column = get_position_from_mouse(position)
                current_game.selected_piece(row, column)

        current_game.update()

    pygame.quit()


if __name__ == "__main__":
    main()
