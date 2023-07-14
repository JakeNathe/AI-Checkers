# Description:  ........

import pygame
from constants import *
from game import *
from minimax import minimax

pygame.display.set_caption("Checkers by Jake Nathe")


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

        # # creates AI move for White
        # if current_game.current_turn == WHITE:
        #     value, new_board = minimax(current_game.get_board(), 3, WHITE)
        #     current_game.ai_move(new_board)

        if current_game.winner():
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
