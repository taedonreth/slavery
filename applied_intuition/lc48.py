# leetcode 48: rotate image (medium)

from typing import List

class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """

        """
        thoughts:
        is there a math trick where i can reflect?
        if we transpose it and then reverse it then its rotated 90 degrees

        Input: matrix = [[1,2,3],
                        [4,5,6],
                        [7,8,9]]
        transpose: matrix = [[1, 4, 7],
                             [2, 5, 8],
                             [3, 6, 9]]
        reverse rows: matrix = [[7, 4, 1],
                            [8, 5, 2],
                            [9, 6, 3]]
        Output: [[7,4,1],
                [8,5,2],
                [9,6,3]]

        rotation 90 degrees = transpose + reverse rows

        helper functions:
            how do we transpose
                (0, 0) -> (0, 0)
                (0, 1) -> (1, 0)
                (0, 2) -> (2, 0)
                (1, 0) -> (0, 1)
                flip rows n cols
            how do we reverse
                for each row in the grid
                    row = row.reverse()
        """

        return self.reverse(self.transpose(matrix))

    def transpose(self, matrix: List[List[int]]) -> List[List[int]]:
        for row in range(len(matrix)):
            for col in range(row + 1, len(matrix)):
                matrix[row][col], matrix[col][row] = matrix[col][row], matrix[row][col]
        return matrix

    def reverse(self, matrix: List[List[int]]) -> List[List[int]]:
        for row in matrix:
            row.reverse()

        return matrix