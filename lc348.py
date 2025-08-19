from typing import List

"""
Example 1:

Input
["TicTacToe", "move", "move", "move", "move", "move", "move", "move"]
[[3], [0, 0, 1], [0, 2, 2], [2, 2, 1], [1, 1, 2], [2, 0, 1], [1, 0, 2], [2, 1, 1]]
Output
[null, 0, 0, 0, 0, 0, 0, 1]

Explanation
TicTacToe ticTacToe = new TicTacToe(3);
Assume that player 1 is "X" and player 2 is "O" in the board.
ticTacToe.move(0, 0, 1); // return 0 (no one wins)
|X| | |
| | | |    // Player 1 makes a move at (0, 0).
| | | |

ticTacToe.move(0, 2, 2); // return 0 (no one wins)
|X| |O|
| | | |    // Player 2 makes a move at (0, 2).
| | | |

ticTacToe.move(2, 2, 1); // return 0 (no one wins)
|X| |O|
| | | |    // Player 1 makes a move at (2, 2).
| | |X|

ticTacToe.move(1, 1, 2); // return 0 (no one wins)
|X| |O|
| |O| |    // Player 2 makes a move at (1, 1).
| | |X|

ticTacToe.move(2, 0, 1); // return 0 (no one wins)
|X| |O|
| |O| |    // Player 1 makes a move at (2, 0).
|X| |X|

ticTacToe.move(1, 0, 2); // return 0 (no one wins)
|X| |O|
|O|O| |    // Player 2 makes a move at (1, 0).
|X| |X|

ticTacToe.move(2, 1, 1); // return 1 (player 1 wins)
|X| |O|
|O|O| |    // Player 1 makes a move at (2, 1).
|X|X|X|
"""

"""
Assume the following rules are for the tic-tac-toe game on an n x n board between two players:

A move is guaranteed to be valid and is placed on an empty block.
Once a winning condition is reached, no more moves are allowed.
A player who succeeds in placing n of their marks in a horizontal, vertical, or diagonal row wins the game.
Implement the TicTacToe class:
"""


class TicTacToe:
    """
    TicTacToe(int n) Initializes the object the size of the board n.
    """

    def __init__(self, n: int):
        # data structure to represent the board will be matrix
        self.board = [[-1 for _ in range(n)] for _ in range(n)]

    """
    int move(int row, int col, int player) Indicates that the player with id player plays at the cell (row, col) of the board. The move is guaranteed to be a valid move, and the two players alternate in making moves. Return
    0 if there is no winner after the move,
    1 if player 1 is the winner after the move, or
    2 if player 2 is the winner after the move.
    """

    def move(self, row: int, col: int, player: int) -> int:
        # instead of placing X's and O's keep it simple and place 1's and 0's, representing the
        # player ID
        # this function will handle manipulation of the board, not checking wins
        self.board[row][col] = player
        return self.check_state(row, col, player)

    def check_state(self, row: int, col: int, player: int) -> int:
        # this function is responsible for returning a value based on the current state passed into
        # it - 0 for no winner, 1 for player 1 win, 2 for player 2 win
        # if win found, return the winning player, otherwise return 0
        # but how do we efficiently check for a win?
        # we could iterate using double for loop and check the conditions
        # if n = size of board, this is O(n^2)
        # is there a faster way?
        # we know what was the last move, we can check if that move caused any wins (not whole
        # board)

        # check row
        if self.check_row_win(row, player):
            return player

        # check col
        if self.check_col_win(col, player):
            return player

        # if on the diagonal, check
        if row == col:
            if self.check_diag_win(player):
                return player

        # if on the other diagonal, check
        if row + col == len(self.board) - 1:
            if self.check_opposite_diag_win(player):
                return player

        return 0

    def check_row_win(self, row, player):
        for col in range(len(self.board)):
            if self.board[row][col] != player:
                return False

        return True

    def check_col_win(self, col, player):
        for row in range(len(self.board)):
            if self.board[row][col] != player:
                return False

        return True

    # (0, 0), (1, 1), (2, 2)
    def check_diag_win(self, player):
        for i in range(len(self.board)):
            if self.board[i][i] != player:
                return False

        return True

    # (0, 2), (1, 1), (2, 0)
    def check_opposite_diag_win(self, player):
        for i in range(len(self.board)):
            if self.board[i][len(self.board) - i - 1] != player:
                return False

        return True


def main():
    # Your TicTacToe object will be instantiated and called as such:
    # obj = TicTacToe(n)
    # param_1 = obj.move(row,col,player)

    obj = TicTacToe(3)
    assert obj.move(0, 0, 1) == 0
    assert obj.move(0, 2, 2) == 0
    assert obj.move(2, 2, 1) == 0
    assert obj.move(1, 1, 2) == 0
    assert obj.move(2, 0, 1) == 0
    assert obj.move(1, 0, 2) == 0
    assert obj.move(2, 1, 1) == 1


if __name__ == "__main__":
    main()
