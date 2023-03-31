import pygame
from constants import *


class Piece:
    """Creates game pieces"""

    def __init__(self, row, column, piece_color):
        self._row = row
        self._column = column
        self._piece_color = piece_color
        self._king = True
        self._x_cord = 0
        self._y_cord = 0
        self.find_position()

        if piece_color == WHITE:
            self._direction = -1
        else:
            self._direction = 1

    def __repr__(self):
        return str(self._piece_color)

    def find_position(self):
        """Draws piece in middle of square"""
        self._x_cord = SQUARE_SIZE * self._column + SQUARE_SIZE * 0.5
        self._y_cord = SQUARE_SIZE * self._row + SQUARE_SIZE * 0.5

    def create_king(self):
        """Makes piece a king"""
        self._king = True

    def create_piece(self, window):
        """Creates a piece on a game board square"""
        radius = SQUARE_SIZE * 0.5 - PADDING
        pygame.draw.circle(window, BLACK, (self._x_cord, self._y_cord), radius + OUTLINE)
        pygame.draw.circle(window, self._piece_color, (self._x_cord, self._y_cord), radius)
        # if true add crown picture to piece
        if self._king:
            window.blit(CROWN, (self._x_cord - CROWN.get_width() * 0.5, self._y_cord - CROWN.get_height() * 0.5))

