# Checkers
Checkers game with pygame GUI

Black pieces start the game. When a player clicks on a piece, and it is their turn, 
the squares that are valid moves for the piece are displayed with a green dot.

The player then is only allowed to click on a square which is a valid move and the gameboard is updated.
If this was a non-capturing move, the player's turn ends. 

If this was a capturing move and the same piece is able to complete an additional capture, 
then the turn will not change yet and the new valid capture moves are updated with green dots on the gameboard. 
Once no more capture moves are availabe for this piece, the player's turn will end. 

If a piece moves to the opposite end of the board, it is updated to a king piece and displayed with a 
crown on top of the checker. This piece now has valid moves going in both directions of the gameboard.

A video of the program running: 
