# Description:  ........

import pygame
from constants import *
from game import *

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

        if current_game.winner() is not None:
            print(current_game.winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                row, column = get_position_from_mouse(position)
                current_game.select_piece(row, column)

            current_game.update()

    pygame.quit()


if __name__ == "__main__":
    main()
