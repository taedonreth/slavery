# leetcode 200: number of islands (medium)

"""
Gven an m x n 2D binary grid which represents a map of '1's (land) and '0's (water), return the number of islands.
An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the grid are all surrounded by water.


Example 1:

Input: grid = [
  ["1","1","1","1","0"],
  ["1","1","0","1","0"],
  ["1","1","0","0","0"],
  ["0","0","0","0","0"]
]
Output: 1
Example 2:

Input: grid = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]
Output: 3


Constraints:

m == grid.length
n == grid[i].length
1 <= m, n <= 300
grid[i][j] is '0' or '1'.
"""

from typing import List


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        """
        basic dfs with a running counter to keep track of islands
            change grid in place once a cell has been visited
        """
        num_islands = 0

        def dfs(row: int, col: int) -> int:
            stack = []
            stack.append((row, col))
            DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            grid[row][col] = "0"

            while stack:
                curr_row, curr_col = stack.pop()
                for dy, dx in DIRECTIONS:
                    new_row, new_col = curr_row + dy, curr_col + dx

                    if (
                        0 <= new_row < len(grid)
                        and 0 <= new_col < len(grid[0])
                        and grid[new_row][new_col] == "1"
                    ):
                        grid[new_row][new_col] = "0"
                        stack.append((new_row, new_col))

        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if grid[row][col] == "1":
                    num_islands += 1
                    dfs(row, col)

        return num_islands


if __name__ == "__main__":
    sol = Solution()

    # Example 1
    grid1 = [
        ["1", "1", "1", "1", "0"],
        ["1", "1", "0", "1", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "0", "0", "0"],
    ]
    assert sol.numIslands(grid1) == 1

    # Example 2
    grid2 = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"],
    ]
    assert sol.numIslands(grid2) == 3

    # Single cell island
    grid3 = [["1"]]
    assert sol.numIslands(grid3) == 1

    # Single cell water
    grid4 = [["0"]]
    assert sol.numIslands(grid4) == 0

    # Disconnected small islands
    grid5 = [
        ["1", "0", "1", "0", "1"],
        ["0", "1", "0", "1", "0"],
        ["1", "0", "1", "0", "1"],
    ]
    assert sol.numIslands(grid5) == 8

    # Large connected block
    grid6 = [["1", "1", "1"], ["1", "1", "1"], ["1", "1", "1"]]
    assert sol.numIslands(grid6) == 1

    # Checkerboard pattern
    grid7 = [
        ["1", "0", "1", "0"],
        ["0", "1", "0", "1"],
        ["1", "0", "1", "0"],
        ["0", "1", "0", "1"],
    ]
    assert sol.numIslands(grid7) == 8

    # Empty row edge case
    grid8 = [[]]
    assert sol.numIslands(grid8) == 0

    print("✅ All test cases passed!")
