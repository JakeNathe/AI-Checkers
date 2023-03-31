import pygame
from constants import *
from gamePieces import Piece


class Board:
    """Represents and updates the game board. Keeps track of winner and current turn."""

    def __init__(self):
        self._board = []
        # self.draw_board()
        self.setup_pieces()
        self._players = []
        self._current_turn = "Black"  # black always goes first
        self._selected_piece = None
        self._winner = None

    def draw_board(self, window):
        """Sets up board with correct colors"""
        window.fill(GREY)
        for row in range(ROWS):
            for column in range(row % 2, COLUMNS, 2):
                pygame.draw.rect(window, TAN, (row * SQUARE_SIZE, column * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def setup_pieces(self):
        """Sets all pieces in the starting positions"""
        # creates 8 rows in 2d array
        for row in range(ROWS):
            self._board.append([])

        # sets white checkers starting places in rows 0-2
        for row in range(0, 3):
            for column in range(0, COLUMNS):
                if (column % 2 != 0 and row % 2 == 0) or (column % 2 == 0 and row % 2 != 0):
                    self._board[row].append(Piece(row, column, WHITE))
                else:
                    self._board[row].append(0)

        # sets empty places in rows 3-4
        for row in range(3, 5):
            for column in range(0, COLUMNS):
                self._board[row].append(0)

        # sets black checkers starting places in rows 5-7
        for row in range(5, ROWS):
            for column in range(0, COLUMNS):
                if (column % 2 == 0 and row % 2 != 0) or (column % 2 != 0 and row % 2 == 0):
                    self._board[row].append(Piece(row, column, BLACK))
                else:
                    self._board[row].append(0)

    def draw(self, window):
        """Draws board by calling draw_board method"""
        self.draw_board(window)

        for row in range(ROWS):
            for column in range(COLUMNS):
                piece = self._board[row][column]
                if piece != 0:
                    piece.create_piece(window)
