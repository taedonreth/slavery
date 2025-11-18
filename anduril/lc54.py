# leetcode 54: spiral matrix (medium)

"""
Given an m x n matrix, return all elements of the matrix in spiral order.

 

Example 1:


Input: matrix = [[1,2,3],
                 [4,5,6],
                 [7,8,9]]
Output: [1,2,3,6,9,8,7,4,5]
Example 2:


Input: matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
Output: [1,2,3,4,8,12,11,10,9,5,6,7]


Constraints:

m == matrix.length
n == matrix[i].length
1 <= m, n <= 10
-100 <= matrix[i][j] <= 100
"""

from typing import List

class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        """
        top right bottom left pointers
        move it in and keep going until top hits the bottom
        """
        top, left = 0, 0
        right, bottom = len(matrix[0]) - 1, len(matrix) - 1
        res = []

        while top <= bottom:
            # move pointers and add to res
            for i in range(left, right + 1):
                res.append(matrix[top][i])
            top += 1
            for j in range(top, bottom + 1):
                res.append(matrix[j][right])
            right -= 1
            if bottom >= top:
                for k in range(right, left - 1, -1):
                    res.append(matrix[bottom][k])
                bottom -= 1
            if right >= left:
                for h in range(bottom, top - 1, -1):
                    res.append(matrix[h][left])
                left += 1

        return res



if __name__ == "__main__":
    sol = Solution()

    # Example tests
    assert sol.spiralOrder([[1,2,3],[4,5,6],[7,8,9]]) == [1,2,3,6,9,8,7,4,5]
    assert sol.spiralOrder([[1,2,3,4],[5,6,7,8],[9,10,11,12]]) == [1,2,3,4,8,12,11,10,9,5,6,7]

    # Edge cases
    # 1x1
    assert sol.spiralOrder([[5]]) == [5]

    # 1xN
    assert sol.spiralOrder([[1,2,3,4]]) == [1,2,3,4]

    # Nx1
    assert sol.spiralOrder([[1],[2],[3]]) == [1,2,3]

    # Rectangular more tall
    assert sol.spiralOrder([[1,2],[3,4],[5,6]]) == [1,2,4,6,5,3]

    # Rectangular more wide
    assert sol.spiralOrder([[1,2,3],[4,5,6]]) == [1,2,3,6,5,4]

    print("All tests passed!")