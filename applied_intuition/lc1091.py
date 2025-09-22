# leetcode 1091: shortest path in binary matrix (medium)

from typing import List
from collections import deque

class Solution:
    def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
        """
        BFS starting from top (0, 0)
        level order bfs
        increase step size until you reach the bottom left
        if we reach bottom left, return length
        otherwise return -1
        """
        if grid[0][0] == 1 or grid[len(grid) - 1][len(grid) - 1] == 1:
            return -1

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]
        steps = 1
        q = deque()
        q.append((0, 0))
        grid[0][0] = 1
        while q:
            for _ in range(len(q)):
                r, c = q.popleft()
                if r == len(grid) - 1 and c == len(grid) - 1:
                    return steps
                for dx, dy in directions:
                    new_row, new_col = r + dx, c + dy
                    if 0 <= new_row < len(grid) and 0 <= new_col < len(grid) and grid[new_row][new_col] == 0:
                        grid[new_row][new_col] = 1
                        q.append((new_row, new_col))

            steps += 1


        return -1