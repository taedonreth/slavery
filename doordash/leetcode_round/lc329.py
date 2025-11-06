# leetcode 329: longest increasing path in a matrix (hard)

"""
Given an m x n integers matrix, return the length of the longest increasing path in matrix.

From each cell, you can either move in four directions: left, right, up, or down. You may not move diagonally or move outside the boundary (i.e., wrap-around is not allowed).
"""

from typing import List


class Solution:
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        if not matrix:
            return 0

        rows, cols = len(matrix), len(matrix[0])
        cache = [[0] * cols for _ in range(rows)]
        DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

        # dfs
        def dfs(i: int, j: int) -> int:
            # we've already calculated this cell
            if cache[i][j]:
                return cache[i][j]

            best = 0
            for y, x in DIRECTIONS:
                dy, dx = i + y, j + x

                if 0 <= dy < rows and 0 <= dx < cols and matrix[i][j] < matrix[dy][dx]:
                    best = max(best, dfs(dy, dx))

            cache[i][j] = best + 1
            return cache[i][j]

        res = 0
        for row in range(rows):
            for col in range(cols):
                res = max(res, dfs(row, col))

        return res
