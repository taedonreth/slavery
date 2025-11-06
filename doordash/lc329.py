# leetcode 329: longest increasing path in a matrix (hard)

"""
Given an m x n integers matrix, return the length of the longest increasing path in matrix.

From each cell, you can either move in four directions: left, right, up, or down. You may not move diagonally or move outside the boundary (i.e., wrap-around is not allowed).

Input: matrix = [[9,9,4],
                 [6,6,8],
                 [2,1,1]]
Output: 4
Explanation: The longest increasing path is [1, 2, 6, 9].
"""

from typing import List


class Solution:
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        """
        brute force: starting at each cell, move as many times as possible, return max increasing moves
        """

        pass


if __name__ == "__main__":
    pass
