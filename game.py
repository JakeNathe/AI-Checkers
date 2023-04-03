import pygame
from constants import *


class Game:
    """Updates display, validates moves, moves pieces and updates turn."""
    # used to keep track of how many moves a player has made in a turn. If the first move is a capturing move,
    # any additional moves must also be capturing moves, or the turn changes.
    move_num = 0

    def __init__(self, window):
        self._window = window
        self._selected_piece = None
        self._board = GameBoard()
        self._current_turn = BLACK
        self._valid_moves = []  # list of tuples (row, column)
        self._winner = None

    def update(self):
        """Updates display"""
        self._board.draw_pieces(self._window)
        self.draw_valid_moves(self._valid_moves)
        pygame.display.update()

    def selected_piece(self, row, column):
        """Confirms the location is valid and gives list of valid moves. valid moves are tuples (row, column)"""
        # try to move selected piece. If invalid location unselect piece and call again
        if self._selected_piece:
            move = self._move_square(row, column)
            if not move:
                self._selected_piece = None
                self.selected_piece(row, column)

        piece = self._board.get_checker_details(row, column)
        # finds valid moves for the piece
        if piece != 0 and piece.get_piece_color() == self._current_turn:
            self._selected_piece = piece
            if self.move_num == 0:
                self._valid_moves = self.get_valid_moves(piece, False)
            else:
                self._valid_moves = self.get_valid_moves(piece, True)
            return True

        return False

    def _move_square(self, row, column):
        """Called by selected_piece method. Moves the selected piece"""
        start_location = self._selected_piece
        start_row = start_location.get_row()
        start_column = start_location.get_column()
        piece = self._board.get_checker_details(row, column)
        start_kings = self._board.get_kings(start_location.get_piece_color())

        if self._selected_piece and piece == 0 and (row, column) in self._valid_moves:
            new_location = self._board.make_move(self._selected_piece, row, column)
            # updates piece to new position to check for additional capture moves
            new_row = new_location[0]
            new_column = new_location[1]
            piece = self._board.get_checker_details(new_row, new_column)

            capture = False  # changed to true if capture was made during current turn
            # tests if piece was captured, and removes if it was
            if abs(start_row - new_row) == 2 and abs(start_column - new_column) == 2:
                enemy_row = (start_row + new_row) // 2
                enemy_column = (start_column + new_column) // 2
                enemy_piece = self._board.get_checker_details(enemy_row, enemy_column)
                self._board.remove_piece(enemy_piece)
                self.move_num += 1
                capture = True

        else:
            return False

        # making a king ends piece's turn
        end_kings = self._board.get_kings(start_location.get_piece_color())
        if end_kings > start_kings:
            self.update_turn()
            return True

        # extends turn if a second capture can be made by the same piece
        if capture and self.test_captures(piece):
            self._valid_moves = []
            return True
        else:
            self.update_turn()
            return True

    def update_turn(self):
        """Changes player's turn"""
        self._valid_moves = []
        self.move_num = 0
        if self._current_turn == BLACK:
            self._current_turn = WHITE
        else:
            self._current_turn = BLACK

    def get_valid_moves(self, piece, captures_only):
        """Finds possible non-capturing and capturing moves for a piece"""
        moves = []
        row = piece.get_row()
        column = piece.get_column()
        piece_color = piece.get_piece_color()

        if not captures_only:
            # non-capturing moves
            # black checker can only move towards row 0
            if piece_color == BLACK or piece.test_king():
                # adds move locations moving northeast if on the board
                if ((row - 1) >= 0) and ((column + 1) < COLUMNS):
                    # check if new ending space is empty to move to
                    if self._board.get_checker_details((row - 1), (column + 1)) == 0:
                        moves.extend([(row - 1, column + 1)])

                # reset
                row = piece.get_row()
                column = piece.get_column()

                # adds move locations moving northwest if on the board
                if ((row - 1) >= 0) and ((column - 1) >= 0):
                    # check if new ending space is empty to move to
                    if self._board.get_checker_details((row - 1), (column - 1)) == 0:
                        moves.extend([(row - 1, column - 1)])
                # reset
                row = piece.get_row()
                column = piece.get_column()

            # white checker can only move towards row 7
            if piece_color == WHITE or piece.test_king():
                # adds move locations moving southeast if on the board
                if ((row + 1) < ROWS) and ((column + 1) < COLUMNS):
                    # check if new ending space is empty to move to
                    if self._board.get_checker_details((row + 1), (column + 1)) == 0:
                        moves.extend([(row + 1, column + 1)])
                # reset
                row = piece.get_row()
                column = piece.get_column()

                # adds move locations moving southwest if on the board
                if ((row + 1) < ROWS) and ((column - 1) >= 0):
                    # check if new ending space is empty to move to
                    if self._board.get_checker_details((row + 1), (column - 1)) == 0:
                        # must be an enemy piece to capture in square between the current square and valid move square
                        moves.extend([(row + 1, column - 1)])
                # reset
                row = piece.get_row()
                column = piece.get_column()

    # capturing moves
        # black checker can only move towards row 0
        if piece_color == BLACK or piece.test_king():
            # adds move locations moving northeast if on the board
            if ((row - 2) >= 0) and ((column + 2) < COLUMNS):
                # check if new ending space is empty to move to
                if self._board.get_checker_details((row - 2), (column + 2)) == 0:
                    # tests for enemy piece
                    validate = self._board.get_checker_details((row - 1), (column + 1))
                    if validate != 0 and validate.get_piece_color() != piece_color:
                        moves.extend([(row - 2, column + 2)])
            # reset
            row = piece.get_row()
            column = piece.get_column()

            # adds move locations moving northwest if on the board
            if ((row - 2) >= 0) and ((column - 2) >= 0):
                # check if new ending space is empty to move to
                if self._board.get_checker_details((row - 2), (column - 2)) == 0:
                    # tests for enemy piece
                    validate = self._board.get_checker_details((row - 1), (column - 1))
                    if validate != 0 and validate.get_piece_color() != piece_color:
                        moves.extend([(row - 2, column - 2)])
            # reset
            row = piece.get_row()
            column = piece.get_column()

        # white checker can only move towards row 7
        if piece_color == WHITE or piece.test_king():
            # adds move locations moving southeast if on the board
            if ((row + 2) < ROWS) and ((column + 2) < COLUMNS):
                # check if new ending space is empty to move to
                if self._board.get_checker_details((row + 2), (column + 2)) == 0:
                    # tests for enemy piece
                    validate = self._board.get_checker_details((row + 1), (column + 1))
                    if validate != 0 and validate.get_piece_color() != piece_color:
                        moves.extend([(row + 2, column + 2)])
            # reset
            row = piece.get_row()
            column = piece.get_column()

            # adds move locations moving southwest if on the board
            if ((row + 2) < ROWS) and ((column - 2) >= 0):
                # check if new ending space is empty to move to
                if self._board.get_checker_details((row + 2), (column - 2)) == 0:
                    # tests for enemy piece
                    validate = self._board.get_checker_details((row + 1), (column - 1))
                    if validate != 0 and validate.get_piece_color() != piece_color:
                        moves.extend([(row + 2, column - 2)])

        return moves

    def test_captures(self, piece):
        """Finds capturing moves for a piece. Used to test if player's turn should continue after capturing 1+ pieces"""
        capture_squares = []
        row = piece.get_row()
        column = piece.get_column()
        piece_color = piece.get_piece_color()

        # black checker can only move towards row 0
        if piece_color == BLACK or piece.test_king():
            # adds move locations moving northeast if on the board
            if ((row - 2) >= 0) and ((column + 2) < COLUMNS):
                # check if new ending space is empty to move to
                if self._board.get_checker_details((row - 2), (column + 2)) == 0:
                    # tests for enemy piece
                    validate = self._board.get_checker_details((row - 1), (column + 1))
                    if validate != 0 and validate.get_piece_color() != piece_color:
                        capture_squares.extend([(row - 2, column + 2)])
            # reset
            row = piece.get_row()
            column = piece.get_column()

            # adds move locations moving northwest if on the board
            if ((row - 2) >= 0) and ((column - 2) >= 0):
                # check if new ending space is empty to move to
                if self._board.get_checker_details((row - 2), (column - 2)) == 0:
                    # tests for enemy piece
                    validate = self._board.get_checker_details((row - 1), (column - 1))
                    if validate != 0 and validate.get_piece_color() != piece_color:
                        capture_squares.extend([(row - 2, column - 2)])
            # reset
            row = piece.get_row()
            column = piece.get_column()

        # white checker can only move towards row 7
        if piece_color == WHITE or piece.test_king():
            # adds move locations moving southeast if on the board
            if ((row + 2) < ROWS) and ((column + 2) < COLUMNS):
                # check if new ending space is empty to move to
                if self._board.get_checker_details((row + 2), (column + 2)) == 0:
                    # tests for enemy piece
                    validate = self._board.get_checker_details((row + 1), (column + 1))
                    if validate != 0 and validate.get_piece_color() != piece_color:
                        capture_squares.extend([(row + 2, column + 2)])
            # reset
            row = piece.get_row()
            column = piece.get_column()

            # adds move locations moving southwest if on the board
            if ((row + 2) < ROWS) and ((column - 2) >= 0):
                # check if new ending space is empty to move to
                if self._board.get_checker_details((row + 2), (column - 2)) == 0:
                    # tests for enemy piece
                    validate = self._board.get_checker_details((row + 1), (column - 1))
                    if validate != 0 and validate.get_piece_color() != piece_color:
                        capture_squares.extend([(row + 2, column - 2)])

        if capture_squares:
            return True
        else:
            return False

    def draw_valid_moves(self, moves):
        """Displays selected pieces valid moves on the board"""
        for move in moves:
            row = move[0]
            column = move[1]
            pygame.draw.circle(self._window, GREEN, (column * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 10)


class GameBoard:
    """Creates the game board with pieces in the starting positions. Updates piece's location, removes pieces and
    checks for the winner."""

    def __init__(self):
        self._board = []
        self.fill_board()
        self._white_kings = 0
        self._black_kings = 0
        self._black_pieces = 12
        self._white_pieces = 12

    def get_kings(self, player):
        """Returns players king count"""
        if player == BLACK:
            return self._black_kings
        else:
            return self._white_kings

    def get_pieces(self, player):
        """Returns players piece count"""
        if player == BLACK:
            return self._black_pieces
        else:
            return self._white_pieces

    def draw_board(self, window):
        """Sets up board with correct colors"""
        window.fill(GREY)
        for row in range(ROWS):
            for column in range(row % 2, COLUMNS, 2):
                pygame.draw.rect(window, TAN, (row * SQUARE_SIZE, column * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def fill_board(self):
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

    def draw_pieces(self, window):
        """Draws game pieces"""

        self.draw_board(window)

        for row in range(ROWS):
            for column in range(COLUMNS):
                piece = self._board[row][column]
                if piece != 0:
                    piece.create_piece(window)

    def make_move(self, piece, row, column):
        """Moves the piece on the board and checks if a king should be made. Returns piece's new location"""

        self._board[row][column] = self._board[piece.get_row()][piece.get_column()]
        self._board[piece.get_row()][piece.get_column()] = 0
        piece.move_piece(row, column)

        if piece.get_piece_color() == BLACK and row == 0:
            piece.create_king()
            self._black_kings += 1

        if piece.get_piece_color() == WHITE and row == ROWS - 1:
            piece.create_king()
            self._white_kings += 1

        new_location = (row, column)
        return new_location

    def get_checker_details(self, row, column):
        """Returns checker detail in the specified square"""
        return self._board[row][column]

    def remove_piece(self, piece):
        """Remove captured piece form the board and from players piece number"""
        self._board[piece.get_row()][piece.get_column()] = 0

        if piece.get_piece_color() == BLACK:
            self._black_pieces -= 1
        else:
            self._white_pieces -= 1

    def winner(self):
        """Returns winner when all pieces are captured. Displayed on the screen."""
        if self._black_pieces == 0:
            return "White Wins!"
        elif self._white_pieces == 0:
            return "Black Wins!"
        else:
            return None


class Piece:
    """Keeps track of each piece's location, color, and type. Creates king pieces."""

    def __init__(self, row, column, piece_color):
        self._row = row
        self._column = column
        self._piece_color = piece_color
        self._king = False
        self._x_cord = 0
        self._y_cord = 0
        self.find_position()

    def __repr__(self):
        return str(self._piece_color)

    def get_piece_color(self):
        return self._piece_color

    def find_position(self):
        """Draws piece in middle of square"""
        self._x_cord = SQUARE_SIZE * self._column + SQUARE_SIZE // 2
        self._y_cord = SQUARE_SIZE * self._row + SQUARE_SIZE // 2

    def get_row(self):
        return self._row

    def get_column(self):
        return self._column

    def get_x(self):
        return self._x_cord

    def get_y(self):
        return self._y_cord

    def test_king(self):
        return self._king

    def create_king(self):
        """Makes piece a king"""
        self._king = True

    def move_piece(self, row, column):
        """Moves pieces to specified square on board"""
        self._row = row
        self._column = column
        self.find_position()

    def create_piece(self, window):
        """Creates a piece on a game board square"""
        radius = SQUARE_SIZE // 2 - PADDING
        pygame.draw.circle(window, BLACK, (self._x_cord, self._y_cord), radius + OUTLINE)
        pygame.draw.circle(window, self._piece_color, (self._x_cord, self._y_cord), radius)
        # if true add crown picture to piece
        if self._king:
            window.blit(CROWN, (self._x_cord - CROWN.get_width() // 2, self._y_cord - CROWN.get_height() // 2))
