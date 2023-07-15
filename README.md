# AI Checkers

Checkers game with an AI player for white.
Black starts the game.
GUI using pycharm.

Program validates all moves that a piece can make. If it is white's turn then only white pieces can move. 
Non-king white peieces can only move down and black can only move up. Kings can move in either direction.
When all pieces are captured the capturing player wins the game. 

Minimax algorithm for determining White's moves. Algorithim can look any amount of moves ahead, but depth is set at 3.
Considers all possible moves for White and counter moves from Black. Assumes that the human player will also make the best move available to them each turn. Determines best move avilable by what the game board 
can look like x (depth) moves ahead. Algorithm want's to maximize White pieces and minimzing Black pieces, while having kings be a priority.


Short video of the game being played: https://youtu.be/qmZYWzSe-lc

