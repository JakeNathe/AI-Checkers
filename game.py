from constants import *
import pygame


class Game:
    """Updates display, validates moves, moves pieces and updates turn."""

    def __init__(self, window):
        self.window = window
        self.selected_piece = None
        self._board = GameBoard()
        self.current_turn = BLACK
        self.valid_moves = {}

    def winner(self):
        return self._board.winner()

    def get_board(self):
        return self._board

    def update(self):
        """Updates display"""
        self._board.draw_pieces(self.window)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def update_turn(self):
        """Changes player's turn"""
        self.valid_moves = {}
        if self.current_turn == BLACK:
            self.current_turn = WHITE
        else:
            self.current_turn = BLACK

    def draw_valid_moves(self, moves):
        """Displays selected pieces valid moves on the board"""
        for move in moves:
            row, column = move
            pygame.draw.circle(self.window, GREEN, (column * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 10)

    def select_piece(self, row, column):
        if self.selected_piece:
            result = self._move(row, column)
            if not result:
                self.selected_piece = None
                self.select_piece(row, column)

        piece = self._board.get_piece(row, column)
        if piece != 0 and piece.color == self.current_turn:
            self.selected_piece = piece
            self.valid_moves = self._board.get_valid_moves(piece)
            return True

        return False

    def _move(self, row, column):
        piece = self._board.get_piece(row, column)
        if self.selected_piece and piece == 0 and (row, column) in self.valid_moves:
            self._board.make_move(self.selected_piece, row, column)
            jumped = self.valid_moves[(row, column)]
            if jumped:
                self._board.remove_pieces(jumped)
            self.update_turn()
        else:
            return False

        return True

    def ai_move(self, board):
        self._board = board
        self.update_turn()


class GameBoard:
    """Creates the game board with pieces in the starting positions. Updates piece's location, removes pieces and
    checks for the winner."""

    def __init__(self):
        self._board = []
        self.fill_board()
        self.white_kings = 0
        self.black_kings = 0
        self.black_pieces = 12
        self.white_pieces = 12

    def evaluate(self):
        """Evaluates score of the board, for AI"""
        return self.white_pieces - self.black_pieces + (self.white_kings * 0.5 - self.black_kings * 0.5)

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

    def get_piece(self, row, column):
        """Return piece in specified square"""
        return self._board[row][column]

    def get_all_pieces(self, color):
        pieces = []
        for row in self._board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def make_move(self, piece, row, column):
        """Moves the piece on the board and checks if a king should be made. Returns piece's new location"""
        self._board[piece.row][piece.column], self._board[row][column] = self._board[row][column], self._board[piece.row][piece.column]
        piece.move_piece(row, column)

        if row == ROWS - 1 or row == 0:
            if piece.king is False:
                piece.create_king()
                if piece.color == WHITE:
                    self.white_kings += 1
                else:
                    self.black_kings += 1

    def remove_pieces(self, pieces):
        """Remove captured pieces form the board and from players piece number"""
        for piece in pieces:
            self._board[piece.row][piece.column] = 0
            if piece != 0:
                if piece.color == BLACK:
                    self.black_pieces -= 1
                else:
                    self.white_pieces -= 1

    def winner(self):
        """Returns winner when all pieces are captured. Displayed on the screen. (display not added yet)"""
        if self.black_pieces <= 0:
            return "White Wins!"
        elif self.white_pieces <= 0:
            return "Black Wins!"
        return None

    def get_valid_moves(self, piece):
        """Finds valid moves for a piece"""
        moves = {}
        left = piece.column - 1
        right = piece.column + 1
        row = piece.row

        if piece.color == BLACK or piece.king:
            moves.update(self._move_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._move_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._move_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._move_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

        return moves

    def _move_left(self, start, stop, step, color, left, jumped=[]):
        moves = {}
        last = []
        for x in range(start, stop, step):
            if left < 0:
                break

            current = self._board[x][left]
            if current == 0:
                if jumped and not last:
                    break
                elif jumped:
                    moves[(x, left)] = last + jumped
                else:
                    moves[(x, left)] = last

                if last:
                    if step == -1:
                        row = max(x - 3, -1)
                    else:
                        row = min(x + 3, ROWS)
                    moves.update(self._move_left(x + step, row, step, color, left - 1, jumped=last))
                    moves.update(self._move_right(x + step, row, step, color, left + 1, jumped=last))
                break

            elif current.color == color:
                break

            else:
                last = [current]

            left -= 1
        return moves

    def _move_right(self, start, stop, step, color, right, jumped=[]):
        moves = {}
        last = []
        for x in range(start, stop, step):
            if right >= COLUMNS:
                break

            current = self._board[x][right]
            if current == 0:
                if jumped and not last:
                    break
                elif jumped:
                    moves[(x, right)] = last + jumped
                else:
                    moves[(x, right)] = last

                if last:
                    if step == -1:
                        row = max(x - 3, -1)
                    else:
                        row = min(x + 3, ROWS)
                    moves.update(self._move_left(x + step, row, step, color, right - 1, jumped=last))
                    moves.update(self._move_right(x + step, row, step, color, right + 1, jumped=last))
                break

            elif current.color == color:
                break

            else:
                last = [current]

            right += 1
        return moves


class Piece:
    """Keeps track of each piece's location, color, and type. Creates king pieces."""

    def __init__(self, row, column, color):
        self.row = row
        self.column = column
        self.color = color
        self.king = False
        self.x_cord = 0
        self.y_cord = 0
        self.find_position()

    def __repr__(self):
        return str(self.color)

    def find_position(self):
        """Draws piece in middle of square"""
        self.x_cord = SQUARE_SIZE * self.column + SQUARE_SIZE // 2
        self.y_cord = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def move_piece(self, row, column):
        """Moves pieces to specified square on board"""
        self.row = row
        self.column = column
        self.find_position()

    def create_piece(self, window):
        """Creates a piece on a game board square"""
        radius = SQUARE_SIZE // 2 - PADDING
        pygame.draw.circle(window, BLACK, (self.x_cord, self.y_cord), radius + OUTLINE)
        pygame.draw.circle(window, self.color, (self.x_cord, self.y_cord), radius)
        # if true add crown picture to piece
        if self.king:
            window.blit(CROWN, (self.x_cord - CROWN.get_width() // 2, self.y_cord - CROWN.get_height() // 2))

    def create_king(self):
        """Makes piece a king"""
        self.king = True
