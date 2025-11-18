# leetcode 827: making a large island (hard)

"""
You are given an n x n binary matrix grid. You are allowed to change at most one 0 to be 1.
Return the size of the largest island in grid after applying this operation.
An island is a 4-directionally connected group of 1s.

Example 1:
    Input: grid = [[1,0],[0,1]]
    Output: 3
    Explanation: Change one 0 to 1 and connect two 1s, then we get an island with area = 3.
    Example 2:

    Input: grid = [[1,1],[1,0]]
    Output: 4
    Explanation: Change the 0 to 1 and make the island bigger, only one island with area = 4.
    Example 3:

    Input: grid = [[1,1],[1,1]]
    Output: 4
    Explanation: Can't change any 0 to 1, only one island with area = 4.

Constraints:
    n == grid.length
    n == grid[i].length
    1 <= n <= 500
    grid[i][j] is either 0 or 1.
"""

from collections import defaultdict
from typing import List


class Solution:
    def largestIsland(self, grid: List[List[int]]) -> int:
        """
        go through grid, for each 1:
            assign each island a color
            keep track of islands and size using color

        edge cases:
            1 island only
                island is whole grid
                    return size of grid
                island is not whole grid
                    return size of island + 1
            no islands
                return 1

        go back through and test each 0 by trying to connect the islands around it
        """

        num_rows = len(grid)
        num_cols = len(grid[0])
        ISLAND_COLOR = 2
        island_sizes = defaultdict(int)
        # {color: size of island}
        DIRECTIONS = [(-1, 0), (1, 0), (0, 1), (0, -1)]

        def _dfs(row: int, col: int) -> int:
            stack = []
            stack.append((row, col))
            grid[row][col] = ISLAND_COLOR
            island_size = 1

            while stack:
                curr_row, curr_col = stack.pop()

                for dy, dx in DIRECTIONS:
                    new_row, new_col = curr_row + dy, curr_col + dx

                    if (
                        0 <= new_row < num_rows
                        and 0 <= new_col < num_cols
                        and grid[new_row][new_col] == 1
                    ):
                        grid[new_row][new_col] = ISLAND_COLOR
                        island_size += 1
                        stack.append((new_row, new_col))

            return island_size

        for row in range(num_rows):
            for col in range(num_cols):
                if grid[row][col] == 1:
                    island_sizes[ISLAND_COLOR] = _dfs(row, col)
                    ISLAND_COLOR += 1

        # one island only
        if len(island_sizes) == 1:
            # singular island, whole grid
            grid_size = num_rows * num_cols
            if island_sizes[ISLAND_COLOR - 1] == grid_size:
                return grid_size
            else:
                return island_sizes[ISLAND_COLOR - 1] + 1
        # no islands
        elif len(island_sizes) == 0:
            return 1

        largest_island = -float("inf")
        for row in range(num_rows):
            for col in range(num_cols):
                if grid[row][col] == 0:
                    # try to flip bit and test sizes for surround islands
                    curr_size = 1
                    neighbors = set()
                    # up
                    if 0 <= row - 1 < num_rows and grid[row - 1][col] > 1:
                        neighbors.add(grid[row - 1][col])
                    # down
                    if 0 <= row + 1 < num_rows and grid[row + 1][col] > 1:
                        neighbors.add(grid[row + 1][col])
                    # right
                    if 0 <= col + 1 < num_cols and grid[row][col + 1] > 1:
                        neighbors.add(grid[row][col + 1])
                    # left
                    if 0 <= col - 1 < num_cols and grid[row][col - 1] > 1:
                        neighbors.add(grid[row][col - 1])

                    for id in neighbors:
                        curr_size += island_sizes[id]

                    largest_island = max(largest_island, curr_size)

        return largest_island


if __name__ == "__main__":
    sol = Solution()

    # Example 1
    grid = [[1, 0], [0, 1]]
    assert sol.largestIsland(grid) == 3
    # Explanation: flipping any 0 connects both 1s -> island size = 3

    # Example 2
    grid = [[1, 1], [1, 0]]
    assert sol.largestIsland(grid) == 4
    # Explanation: flipping bottom-right 0 makes one full 2x2 island

    # Example 3
    grid = [[1, 1], [1, 1]]
    assert sol.largestIsland(grid) == 4
    # Explanation: already one full island; no gain from flipping

    # 1x1 grid (smallest possible)
    grid = [[0]]
    assert sol.largestIsland(grid) == 1
    # Explanation: flip the only cell -> single island

    grid = [[1]]
    assert sol.largestIsland(grid) == 1
    # Explanation: already all land, nothing to flip

    # No adjacent 1s
    grid = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    assert sol.largestIsland(grid) == 2
    # Explanation: flipping any adjacent 0 to center 1 -> island size = 2

    # Two separate islands
    grid = [[1, 0, 1], [0, 0, 0], [1, 0, 1]]
    assert sol.largestIsland(grid) == 3
    # Explanation: flipping center cell connects no more than 3 total cells

    # Mixed large case
    grid = [[1, 1, 0, 0], [1, 0, 0, 1], [0, 1, 1, 0], [0, 0, 0, 1]]
    # Possible large island by flipping (1,1) or (2,3)
    assert sol.largestIsland(grid) == 6

    # All water
    grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    assert sol.largestIsland(grid) == 1
    # Explanation: flip any 0 -> single island of size 1

    # Large connected area with one hole
    grid = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    assert sol.largestIsland(grid) == 9
    # Explanation: flipping the single 0 connects entire grid -> size 9

    print("✅ All largestIsland test cases passed successfully!")
