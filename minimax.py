from copy import deepcopy
import pygame
from constants import WHITE, BLACK


def minimax(position, depth, max_player):
    """Receives position: current board position, depth: tree depth, max_player: bool. 1 max value, 0 min value."""
    if depth == 0 or position.winner():
        return position.evaluate(), position

    # finds the best move for the piece based on if you want to min or max value
    if max_player:
        max_eval = float('-inf')
        best_move = None
        for move in get_all_moves(position, WHITE):
            cur_eval = minimax(move, depth - 1, False)[0]  # don't care about best move
            max_eval = max(max_eval, cur_eval)
            if max_eval == cur_eval:
                best_move = move
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in get_all_moves(position, BLACK):
            cur_eval = minimax(move, depth - 1, True)[0]  # don't care about best move
            min_eval = min(min_eval, cur_eval)
            if min_eval == cur_eval:
                best_move = move
        return min_eval, best_move


def get_all_moves(board, color):
    """Returns all possible moves for a piece"""
    moves = []
    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, jumped in valid_moves.items():
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.column)
            new_board = sim_move(temp_piece, move, temp_board, jumped)
            moves.append(new_board)
    return moves


def sim_move(piece, move, board, jumped):
    """Simulates a possible move on the board"""
    board.make_move(piece, move[0], move[1])
    if jumped:
        board.remove_pieces(jumped)

    return board
