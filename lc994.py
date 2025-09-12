# leetcode 994: rotting oranges (medium)

from typing import List
from collections import deque


class Solution:
    """
    You are given an m x n grid where each cell can have one of three values:

    0 representing an empty cell,
    1 representing a fresh orange, or
    2 representing a rotten orange.
    Every minute, any fresh orange that is 4-directionally adjacent to a rotten orange becomes rotten.

    Return the minimum number of minutes that must elapse until no cell has a fresh orange. If this is impossible, return -1.
    """

    def orangesRotting(self, grid: List[List[int]]) -> int:
        """
        bfs with multiple starts each cell with a 2
        keep count of minutes
        double for loop to count number of fresh oranges
        each time bfs reaches a fresh orange, decrement total num of oranges
        return minutes if numoranges == 0 else -1
        """
        minutes = 0
        num_fresh = 0
        q = deque()

        # count total num of oranges at first
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if grid[row][col] == 1:
                    num_fresh += 1
                if grid[row][col] == 2:
                    q.append((row, col))

        if num_fresh == 0:
            return 0

        if len(q) == 0:
            return -1

        # dictionary for possible directions we can go
        DIRECTIONS = [(-1, 0), (1, 0), (0, 1), (0, -1)]

        # bfs with multiple sources to simulate rotting oranges
        while q:
            for _ in range(len(q)):
                curr_row, curr_col = q.popleft()
                for direction in DIRECTIONS:
                    new_row = curr_row + direction[0]
                    new_col = curr_col + direction[1]

                    # in bounds and fresh orange
                    if (
                        new_row >= 0
                        and new_row < len(grid)
                        and new_col >= 0
                        and new_col < len(grid[0])
                    ) and grid[new_row][new_col] == 1:
                        q.append((new_row, new_col))
                        grid[new_row][new_col] = 2
                        num_fresh -= 1
            if q:
                minutes += 1

        return minutes if num_fresh == 0 else -1


def main():
    sol = Solution()

    # Example 1
    assert sol.orangesRotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]]) == 4

    # Example 2
    assert sol.orangesRotting([[2, 1, 1], [0, 1, 1], [1, 0, 1]]) == -1

    # Example 3
    assert sol.orangesRotting([[0, 2]]) == 0

    print("All tests passed!")


if __name__ == "__main__":
    main()
