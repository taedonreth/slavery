# leetcode 286: walls and gates (medium)

"""
You are given an m x n grid rooms initialized with these three possible values.
    -1 A wall or an obstacle.
    0 A gate.
    INF Infinity means an empty room. We use the value 231 - 1 = 2147483647 to represent INF as you may assume that the distance to a gate is less than 2147483647.

Fill each empty room with the distance to its nearest gate. If it is impossible to reach a gate, it should be filled with INF.
"""

from collections import deque
from typing import List


class Solution:
    def wallsAndGates(self, rooms: List[List[int]]) -> None:
        """
        Do not return anything, modify rooms in-place instead.

        thought process:
            iterate through rooms
                for each gate, run level order bfs
                track distances in place
                only change to new distance if it is cheaper

        Input: rooms = [[2147483647,-1,0,2147483647],[2147483647,2147483647,2147483647,-1],[2147483647,-1,2147483647,-1],[0,-1,2147483647,2147483647]]
        Output: [[3,-1,0,1],[2,2,1,-1],[1,-1,2,-1],[0,-1,3,4]]
        """

        num_rows = len(rooms)
        num_cols = len(rooms[0])

        for row in range(num_rows):
            for col in range(num_cols):
                # gate here, so start bfs
                if rooms[row][col] == 0:
                    self._bfs(rooms, row, col)

    def _bfs(self, rooms: List[List[int]], row: int, col: int) -> None:
        q = deque()
        q.append((row, col))
        # 1 = visited, 0 = not visited
        visited = [[0] * len(rooms[0]) for _ in range(len(rooms))]
        visited[row][col] = 1

        steps = 1
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]

        while q:
            for _ in range(len(q)):
                curr_row, curr_col = q.popleft()

                for dy, dx in directions:
                    new_row, new_col = curr_row + dy, curr_col + dx

                    # validate new position
                    if (
                        0 <= new_row < len(rooms)
                        and 0 <= new_col < len(rooms[0])
                        and (
                            rooms[new_row][new_col] != 0
                            and rooms[new_row][new_col] != -1
                        )
                        and visited[new_row][new_col] == 0
                    ):
                        rooms[new_row][new_col] = min(rooms[new_row][new_col], steps)
                        visited[new_row][new_col] = 1
                        q.append((new_row, new_col))

            steps += 1


if __name__ == "__main__":
    rooms = [
        [2147483647, -1, 0, 2147483647],
        [2147483647, 2147483647, 2147483647, -1],
        [2147483647, -1, 2147483647, -1],
        [0, -1, 2147483647, 2147483647],
    ]
    sol = Solution()
    sol.wallsAndGates(rooms)
    print(rooms)

    rooms = [[-1]]
    sol.wallsAndGates(rooms)
    print(rooms)

# [[3,-1,0,1],[2,2,1,-1],[1,-1,2,-1],[0,-1,3,4]]



"""
optimal solution:

    def wallsAndGates(self, rooms: List[List[int]]) -> None:
        """
        Multi-source BFS solution
        Time: O(m * n)
        Space: O(m * n)
        """
        if not rooms or not rooms[0]:
            return
        
        rows, cols = len(rooms), len(rooms[0])
        q = deque()

        # Initialize queue with all gates
        for r in range(rows):
            for c in range(cols):
                if rooms[r][c] == 0:
                    q.append((r, c))

        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]

        # BFS from all gates simultaneously
        while q:
            r, c = q.popleft()
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                # Skip walls or already visited cells
                if 0 <= nr < rows and 0 <= nc < cols and rooms[nr][nc] == 2147483647:
                    rooms[nr][nc] = rooms[r][c] + 1
                    q.append((nr, nc))
"""
