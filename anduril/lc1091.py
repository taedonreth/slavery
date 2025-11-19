# leetcode 1091: shortest path in a binary matrix (medium)

"""
Given an n x n binary matrix grid, return the length of the shortest clear path in the matrix. If there is no clear path, return -1.

A clear path in a binary matrix is a path from the top-left cell (i.e., (0, 0)) to the bottom-right cell (i.e., (n - 1, n - 1)) such that:

All the visited cells of the path are 0.
All the adjacent cells of the path are 8-directionally connected (i.e., they are different and they share an edge or a corner).
The length of a clear path is the number of visited cells of this path.

Example 1:
    Input: grid = [[0,1],[1,0]]
    Output: 2

Example 2:
    Input: grid = [[0,0,0],[1,1,0],[1,1,0]]
    Output: 4
    
Example 3:
    Input: grid = [[1,0,0],[1,1,0],[1,1,0]]
    Output: -1

Constraints:
    n == grid.length
    n == grid[i].length
    1 <= n <= 100
    grid[i][j] is 0 or 1
"""

from typing import List
from collections import deque

class Solution:
    def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
        """
        BFS for shortest path
        """
        num_rows, num_cols = len(grid), len(grid[0])

        # edge cases
        if grid[0][0] == 1 or grid[num_rows - 1][num_cols - 1] == 1:
            return -1

        DIRECTIONS = [(-1, 0), (1, 0), (-1, -1), (-1, 1), (1, 1), (1, -1), (0, 1), (0, -1)]
        queue = deque()
        queue.append((0, 0))
        steps = 1

        while queue:
            for _ in range(len(queue)):
                curr_row, curr_col = queue.popleft()
                if curr_row == num_rows - 1 and curr_col == num_cols - 1:
                    return steps

                for dy, dx in DIRECTIONS:
                    new_row, new_col = curr_row + dy, curr_col + dx
                    if 0 <= new_row < num_rows and 0 <= new_col < num_cols and grid[new_row][new_col] == 0:
                        grid[new_row][new_col] = 1
                        queue.append((new_row, new_col))
                        
            steps += 1

        return -1


if __name__ == "__main__":
    sol = Solution()

    assert sol.shortestPathBinaryMatrix([[0,1],[1,0]]) == 2
    assert sol.shortestPathBinaryMatrix([[0,0,0],[1,1,0],[1,1,0]]) == 4
    assert sol.shortestPathBinaryMatrix([[1,0,0],[1,1,0],[1,1,0]]) == -1