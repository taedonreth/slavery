# leetcode 827: making a large island (hard)

"""
You are given an n x n binary matrix grid. You are allowed to change at most one 0 to be 1.
Return the size of the largest island in grid after applying this operation.
An island is a 4-directionally connected group of 1s.
"""

from typing import List


class Solution:
    def largestIsland(self, grid: List[List[int]]) -> int:
        """
        Input: grid = [[1,0],[0,1]]
        Output: 3
        Explanation: Change one 0 to 1 and connect two 1s, then we get an island with area = 3.

        connectivity, so dfs
        brute force:
            we could go through every 0, flip it to a 1, and run dfs and see the largest island

        optimization:
            run dfs from every 1, caluclate island size and assign color in map

            go through grid again
                for each 0, see if flipping it would connect 2
                    if it does, add sizes
                    keep track of max size

        edge cases:
            no islands
                return 1
            one island and not the whole grid
                return size of island + 1
            one island, whole grid
                return size of island
        """

        # explore islands -> assign id
        def dfs(row: int, col: int) -> int:
            stack = []
            stack.append((row, col))
            island_size = 1
            grid[row][col] = ISLAND_ID

            while stack:
                curr_row, curr_col = stack.pop()

                for dy, dx in DIRECTIONS:
                    new_row, new_col = curr_row + dy, curr_col + dx

                    if (
                        0 <= new_row < num_rows
                        and 0 <= new_col < num_cols
                        and grid[new_row][new_col] == 1
                    ):
                        grid[new_row][new_col] = ISLAND_ID
                        island_size += 1
                        stack.append((new_row, new_col))

            return island_size

        # keep track of islands and their size
        color_map = {}
        ISLAND_ID = 2
        DIRECTIONS = [(-1, 0), (1, 0), (0, 1), (0, -1)]

        num_rows = len(grid)
        num_cols = len(grid[0])

        # get starting island sizes
        for row in range(num_rows):
            for col in range(num_cols):
                if grid[row][col] == 1:
                    color_map[ISLAND_ID] = dfs(row, col)
                    ISLAND_ID += 1

        # edge cases
        # no islands
        if not color_map:
            return 1

        # only 1 island
        if len(color_map) == 1:
            grid_size = num_rows * num_cols
            # 1 island and whole grid
            if color_map[ISLAND_ID - 1] == grid_size:
                return grid_size
            # 1 island and not whole grid
            else:
                return color_map[ISLAND_ID - 1] + 1

        max_size = 1

        # simulate flipping: test each side for each 0
        for row in range(num_rows):
            for col in range(num_cols):
                if grid[row][col] == 0:
                    current_size = 1
                    neighbors = set()

                    # check if island in each direction -> if so, add their size to current_size
                    # up
                    if 0 <= row - 1 < num_rows and grid[row - 1][col] > 1:
                        neighbors.add(grid[row - 1][col])

                    # down
                    if 0 <= row + 1 < num_rows and grid[row + 1][col] > 1:
                        neighbors.add(grid[row + 1][col])

                    # left
                    if 0 <= col - 1 < num_cols and grid[row][col - 1] > 1:
                        neighbors.add(grid[row][col - 1])

                    # right
                    if 0 <= col + 1 < num_cols and grid[row][col + 1] > 1:
                        neighbors.add(grid[row][col + 1])

                    # add neighbor sizes to current_size
                    for id in neighbors:
                        current_size += color_map[id]

                    max_size = max(max_size, current_size)

        return max_size


"""
time: O(n^2)
space: O(n^2)
"""


if __name__ == "__main__":
    sol = Solution()
    inpu = [[1, 1], [1, 1]]
    print(sol.largestIsland(inpu))
