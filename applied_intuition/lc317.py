# leetcode 317: shortest distance from all buildings (hard)

from typing import List
from collections import deque

class Solution:
    def shortestDistance(self, grid: List[List[int]]) -> int:
        """
        bfs with cost of each edge being 1
        initialize a distance matrix to keep track of cumulative distance from each house to that cell

        iterate through the grid
            start bfs at each house

        bfs details:
            bfs will be level order, meaning we need to keep track of what level/distance we are from curr house
            queue for bfs order
            keep track of steps (distance from current house to cell)
            iterate through possible directions
                how do we optimize by:
                    1. visiting cells that are able to be reached from other houses only
                    2. not initializing a new visited grid for each run of bfs

                    we can keep this information by mutating original grid
                    each time we see a cell from a run of bfs, subtract 1 from its value
                    if we see it again on the same run, we know we saw it becuase the value changed
                    for subsequent runs, we know to only explore cells with certain values 
                        cells that can be reached by other houses

        # time: run bfs for each house O(k * m * n)
        # space: dist matrix, O(m * n)
                        
        """
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        num_rows = len(grid)
        num_cols = len(grid[0])
        distance = [[0] * num_cols for _ in range(num_rows)]
        EMPTY_LAND = 0

        # iterate through grid
        for row in range(num_rows):
            for col in range(num_cols):
                if grid[row][col] == 1:
                    min_distance = float('inf')

                    # bfs
                    q = deque()
                    q.append((row, col))
                    curr_steps = 1

                    while q:

                        # level processing
                        for _ in range(len(q)):
                            curr_row, curr_col = q.popleft()

                            for x, y in directions:
                                new_row, new_col = curr_row + x, curr_col + y

                                # check eligibility of this new cell
                                # which includes: in bounds, and right 'empty_land' value
                                if (0 <= new_row < num_rows and 0 <= new_col < num_cols and grid[new_row][new_col] == EMPTY_LAND):
                                    # update cell value in distance
                                    distance[new_row][new_col] += curr_steps

                                    # update the cell value in grid
                                    grid[new_row][new_col] -= 1
                                    q.append((new_row, new_col))
                                    min_distance = min(min_distance, distance[new_row][new_col])

                        curr_steps += 1
                    EMPTY_LAND -= 1

        return -1 if min_distance == float('inf') else min_distance


def main():
    sol = Solution()

    # Example 1
    grid1 = [[1,0,2,0,1],
             [0,0,0,0,0],
             [0,0,1,0,0]]
    assert sol.shortestDistance(grid1) == 7, "Test case 1 failed"

    # Example 2
    grid2 = [[1,0]]
    assert sol.shortestDistance(grid2) == 1, "Test case 2 failed"

    # Example 3
    grid3 = [[1]]
    assert sol.shortestDistance(grid3) == -1, "Test case 3 failed"

    print("All test cases passed!")

if __name__ == "__main__":
    main()