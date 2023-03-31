# Date: 3/30/2023
# Description:  Creates a 8x8 standard checkers board with 2 players. Players are able to move around board and capture
#               opponents pieces. Pieces can be upgraded to a "King" by making it to the opposite end of the board.
#               If a piece is able to be captured, the player must do so. The game is won when all the opponents pieces
#               are captured.

import pygame
from constants import *
from board import *

FPS = 60
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")


def main():
    """Sets up event loop to run the game"""
    run = True
    clock = pygame.time.Clock()
    board = Board()

    # runs until the game is quit
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

        board.draw(WINDOW)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()


class OutOfTurn(Exception):
    """Exception if a player tries to make a move when it is not their turn"""
    pass


class InvalidSquare(Exception):
    """Exception if a player tries to move to an invalid square"""
    pass


class InvalidPlayer(Exception):
    """Exception if a player's name does not match a player in the current game"""
    pass


class InvalidColor(Exception):
    """Exception if a player's name does not match a player in the current game"""
    pass