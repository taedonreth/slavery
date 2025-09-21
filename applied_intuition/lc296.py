# leetcode 296: best meeting point (hard)

from typing import List

class Solution:
    def minTotalDistance(self, grid: List[List[int]]) -> int:
        """
        mathematical proof: min distance is median
        closest col is median col between the houses
        closest row is the median row between houses

        ** HAS TO BE IN SORTED ORDER TO GET RIGHT MEDIAN **

        function to get row indicies of all houses
        function to get col indicies of all houses
        calculate median of both

        given coordinate: [median row, median col]
        calculate distance from each house coordiante to this coordiate
        this operation can also be broken up into rows then columns

        return distance
        """

        rows = self.getRows(grid)
        cols = self.getCols(grid)

        median_row_idx = rows[len(rows) // 2]
        median_col_idx = cols[len(cols) // 2]

        # calculate distance between median row and row coords
        row_dist = 0
        for val in rows:
            row_dist += abs(val - median_row_idx)

        # calculate distance between median col and col coords
        col_dist = 0
        for val in cols:
            col_dist += abs(val - median_col_idx)

        return row_dist + col_dist


    def getRows(self, grid: List[List[int]]) -> List[int]:
        # iterate in order of rows
        res = []
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if grid[row][col] == 1:
                    res.append(row)

        return res

    def getCols(self, grid: List[List[int]]) -> List[int]:
        # iterate in order of cols
        res = []
        for col in range(len(grid[0])):
            for row in range(len(grid)):
                if grid[row][col] == 1:
                    res.append(col)

        return res

def main():
    sol = Solution()

    # Example 1
    grid1 = [[1,0,0,0,1],
             [0,0,0,0,0],
             [0,0,1,0,0]]
    assert sol.minTotalDistance(grid1) == 6

    # Example 2
    grid2 = [[1,1]]
    assert sol.minTotalDistance(grid2) == 1

    # Extra: single house, no movement needed
    grid3 = [[0,0,0],
             [0,1,0],
             [0,0,0]]
    assert sol.minTotalDistance(grid3) == 0

    # Extra: houses in a line
    grid4 = [[1,0,0,0,1,0,1]]
    # median col = 3, distances = 3+1+2 = 6
    assert sol.minTotalDistance(grid4) == 6

    print("All test cases passed!")


if __name__ == "__main__":
    main()