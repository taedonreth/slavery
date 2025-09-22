# leetcode 529: minesweeper (medium)

from typing import List

class Solution:
    def updateBoard(self, board: List[List[str]], click: List[int]) -> List[List[str]]:
        """Input: board = [["E","E","E","E","E"],
                            ["E","E","M","E","E"],
                            ["E","E","E","E","E"],
                            ["E","E","E","E","E"]], click = [3,0]

            Output: [["B","1","E","1","B"],
                    ["B","1","M","1","B"],
                    ["B","1","1","1","B"],
                    ["B","B","B","B","B"]]

        dfs starting from click spot?
        explore neighboring cells
            if its "M", make it X and return current state
            if its E and no bombs adjacent, make it B and continue recursing
            if its E and >= 1 bomb adjacent, change it to respective number and return

        return board
        """

        def count_adjacent_mines(row: int, col: int) -> int:
            count = 0
            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                if 0 <= nr < len(board) and 0 <= nc < len(board[0]) and board[nr][nc] == 'M':
                    count += 1
            return count

        directions = [(-1,-1), (-1,0), (-1,1),
                (0,-1),          (0,1),
                (1,-1),  (1,0),  (1,1)]
        
        stack = [tuple(click)]

        while stack:
            row, col = stack.pop()

            if board[row][col] == "M":
                board[row][col] = "X"
                return board

            if board[row][col] == "E":
                mines = count_adjacent_mines(row, col)

                # mines near
                if mines > 0:
                    board[row][col] = str(mines)

                # no mines, keep recursing
                else:
                    board[row][col] = "B"
                    for dr, dc in directions:
                        new_row, new_col = row + dr, col + dc
                        # check bounds
                        if 0 <= new_row < len(board) and 0 <= new_col < len(board[0]) and board[new_row][new_col] == "E":
                            stack.append((new_row, new_col))

        return board