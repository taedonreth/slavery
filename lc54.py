# leetcode 54: spiral matrix (medium)

from typing import List


class Solution:
    # Given an m x n matrix, return all elements of the matrix in spiral order.
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        """
        4 pointers, one for each wall
        move pointers inward
        while all elements haven't been added:
            follow top pointer until you hit right wall
                move top pointer down one (row + 1)
            follow right pointer until you hit bottom wall
                move right pointer left (col - 1)
            follow bottom pointer until you hit left wall
                move bottom pointer up (row - 1)
            follow left pointer until you hit top wall
                move left pointer right (col + 1)
        """
        res = []
        top_ptr = 0
        right_ptr = len(matrix[0]) - 1
        bottom_ptr = len(matrix) - 1
        left_ptr = 0
        while len(res) < (len(matrix) * len(matrix[0])):
            for i in range(left_ptr, right_ptr + 1):
                res.append(matrix[top_ptr][i])
            top_ptr += 1
            for j in range(top_ptr, bottom_ptr + 1):
                res.append(matrix[j][right_ptr])
            right_ptr -= 1
            if bottom_ptr >= top_ptr:
                for k in range(right_ptr, left_ptr - 1, -1):
                    res.append(matrix[bottom_ptr][k])
                bottom_ptr -= 1
            if left_ptr <= right_ptr:
                for x in range(bottom_ptr, top_ptr - 1, -1):
                    res.append(matrix[x][left_ptr])
                left_ptr += 1

        return res


def main():
    s = Solution()

    # Example 1
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    expected = [1, 2, 3, 6, 9, 8, 7, 4, 5]
    assert s.spiralOrder(matrix) == expected

    # Example 2
    matrix = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
    expected = [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
    assert s.spiralOrder(matrix) == expected

    print("All tests passed!")


if __name__ == "__main__":
    main()
