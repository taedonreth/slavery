# leetcode 289: game of life (medium)

"""
According to Wikipedia's article: "The Game of Life, also known simply as Life, is a cellular automaton devised by the British mathematician John Horton Conway in 1970."

The board is made up of an m x n grid of cells, where each cell has an initial state: live (represented by a 1) or dead (represented by a 0). Each cell interacts with its eight neighbors (horizontal, vertical, diagonal) using the following four rules (taken from the above Wikipedia article):

Any live cell with fewer than two live neighbors dies as if caused by under-population.
Any live cell with two or three live neighbors lives on to the next generation.
Any live cell with more than three live neighbors dies, as if by over-population.
Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.
The next state of the board is determined by applying the above rules simultaneously to every cell in the current state of the m x n grid board. In this process, births and deaths occur simultaneously.

Given the current state of the board, update the board to reflect its next state.

Note that you do not need to return anything.



Example 1:
    Input: board = [[0,1,0],
                    [0,0,1],
                    [1,1,1],
                    [0,0,0]]
    Output: [[0,0,0],
             [1,0,1],
             [0,1,1],
             [0,1,0]]

Example 2:
    Input: board = [[1,1],
                    [1,0]]
    Output: [[1,1],
             [1,1]]


Constraints:

m == board.length
n == board[i].length
1 <= m, n <= 25
board[i][j] is 0 or 1.


Follow up:

Could you solve it in-place? Remember that the board needs to be updated simultaneously: You cannot update some cells first and then use their updated values to update other cells.
In this question, we represent the board using a 2D array. In principle, the board is infinite, which would cause problems when the active area encroaches upon the border of the array (i.e., live cells reach the border). How would you address these problems?
"""

from typing import List


class Solution:
    def gameOfLife(self, board: List[List[int]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """

        """
        two passes
            first pass
                count neighbors
                change in place:
                    if original cell was alive
                        if < 2 or > 3 neighbors alive, change original to dead (mark with -1)
                    else if 3 neighbors alive, change original to alive (mark with 2)

            second pass
                if 2, change to 1
                if -1, change to 0
        """
        if not board or not board[0]:
            return

        num_rows, num_cols = len(board), len(board[0])

        def _count_live_neighbors(row: int, col: int) -> int:
            count = 0
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = row + dr, col + dc
                    if (
                        0 <= nr < num_rows
                        and 0 <= nc < num_cols
                        and abs(board[nr][nc]) == 1
                    ):
                        count += 1

            return count

        for row in range(num_rows):
            for col in range(num_cols):
                live_neighbors = _count_live_neighbors(row, col)

                if board[row][col] == 1 and (live_neighbors < 2 or live_neighbors > 3):
                    board[row][col] = -1
                elif board[row][col] == 0 and (live_neighbors == 3):
                    board[row][col] = 2

        for row in range(num_rows):
            for col in range(num_cols):
                if board[row][col] > 0:
                    board[row][col] = 1
                else:
                    board[row][col] = 0


if __name__ == "__main__":
    s = Solution()

    # Example 1
    board1 = [[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]]
    expected1 = [[0, 0, 0], [1, 0, 1], [0, 1, 1], [0, 1, 0]]
    s.gameOfLife(board1)
    assert board1 == expected1

    # Example 2
    board2 = [[1, 1], [1, 0]]
    expected2 = [[1, 1], [1, 1]]
    s.gameOfLife(board2)
    assert board2 == expected2

    # All dead cells stay dead
    board3 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    expected3 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    s.gameOfLife(board3)
    assert board3 == expected3

    # Single live cell dies (underpopulation)
    board4 = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    expected4 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    s.gameOfLife(board4)
    assert board4 == expected4

    # Stable configuration (block)
    board5 = [[1, 1], [1, 1]]
    expected5 = [[1, 1], [1, 1]]
    s.gameOfLife(board5)
    assert board5 == expected5

    # Oscillator (blinker pattern)
    board6 = [[0, 1, 0], [0, 1, 0], [0, 1, 0]]
    expected6 = [[0, 0, 0], [1, 1, 1], [0, 0, 0]]
    s.gameOfLife(board6)
    assert board6 == expected6

    # Another generation of blinker (back to vertical)
    s.gameOfLife(board6)
    expected6b = [[0, 1, 0], [0, 1, 0], [0, 1, 0]]
    assert board6 == expected6b

    # Edge case: 1x1 dead cell
    board7 = [[0]]
    expected7 = [[0]]
    s.gameOfLife(board7)
    assert board7 == expected7

    # Edge case: 1x1 live cell
    board8 = [[1]]
    expected8 = [[0]]
    s.gameOfLife(board8)
    assert board8 == expected8

    # Small 2x3 horizontal line (should oscillate)
    board9 = [[1, 1, 1], [0, 0, 0]]
    expected9 = [[0, 1, 0], [0, 1, 0]]
    s.gameOfLife(board9)
    assert board9 == expected9

    print("✅ All test cases passed!")
