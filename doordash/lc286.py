# leetcode 286: walls and gates (medium)

"""
You are given an m x n grid rooms initialized with these three possible values.

-1 A wall or an obstacle.
0 A gate.
INF Infinity means an empty room. We use the value 231 - 1 = 2147483647 to represent INF as you may assume that the distance to a gate is less than 2147483647.
Fill each empty room with the distance to its nearest gate. If it is impossible to reach a gate, it should be filled with INF.
"""

from typing import List
from collections import deque


class Solution:
    EMPTY = 2**31 - 1  # same as Integer.MAX_VALUE
    GATE = 0
    DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    """
    basically just run BFS from each gate simeuoltaneously
    """

    def wallsAndGates(self, rooms: List[List[int]]) -> None:
        if not rooms or not rooms[0]:
            return

        m, n = len(rooms), len(rooms[0])
        q = deque()

        # Enqueue all gates
        for row in range(m):
            for col in range(n):
                if rooms[row][col] == self.GATE:
                    q.append((row, col))

        # Multi-source BFS
        while q:
            row, col = q.popleft()
            for dr, dc in self.DIRECTIONS:
                r, c = row + dr, col + dc
                if 0 <= r < m and 0 <= c < n and rooms[r][c] == self.EMPTY:
                    rooms[r][c] = rooms[row][col] + 1
                    q.append((r, c))
