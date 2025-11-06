"""
A DashMart is a warehouse run by DoorDash that houses items found in convenience stores, grocery stores, and restaurants. We have a city with open roads, blocked-off roads, and DashMarts.

City planners want you to identify how far a location is from its closest DashMart.

You can only travel over open roads (up, down, left, right). Locations are given in [row, col] format.

Example 1:

Given a grid where:

'O' represents an open road that you can travel over in any direction (up, down, left, or right).
'X' represents a blocked road that you cannot travel through.
'D' represents a DashMart.
The grid is provided as a 2D array, and a list of locations is provided where each location is a pair [row, col].

[
  ['X', 'O', 'O', 'D', 'O', 'O', 'X', 'O', 'X'], #0
  ['X', 'O', 'X', 'X', 'X', 'O', 'X', 'O', 'X'], #1
  ['O', 'O', 'O', 'D', 'X', 'X', 'O', 'X', 'O'], #2
  ['O', 'O', 'D', 'O', 'D', 'O', 'O', 'O', 'X'], #3
  ['O', 'O', 'O', 'O', 'O', 'X', 'O', 'O', 'X'], #4
  ['X', 'O', 'X', 'O', 'O', 'O', 'O', 'X', 'X'], #5
]

List of pairs `[row, col]` for locations:
[
  [200, 200],
  [1, 4],
  [0, 3],
  [5, 8],
  [1, 8],
  [5, 5],
]
Your task is to return the distance for each location from the closest DashMart.

Provided:

city: char[][]
locations: int[][]
Return:

answer: int[]
"""

from collections import deque


def dashmart_distances(city, locations):
    if not city:
        return [-1] * len(locations)

    rows, cols = len(city), len(city[0])
    dist = [[-1] * cols for _ in range(rows)]
    queue = deque()

    # Step 1: add all DashMarts as starting points
    for r in range(rows):
        for c in range(cols):
            if city[r][c] == "D":
                dist[r][c] = 0
                queue.append((r, c))

    # Directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Step 2: BFS
    while queue:
        r, c = queue.popleft()
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if (
                0 <= nr < rows
                and 0 <= nc < cols
                and city[nr][nc] == "O"
                and dist[nr][nc] == -1
            ):
                dist[nr][nc] = dist[r][c] + 1
                queue.append((nr, nc))

    # Step 3: answer queries
    answer = []
    for r, c in locations:
        if 0 <= r < rows and 0 <= c < cols:
            answer.append(dist[r][c])
        else:
            answer.append(-1)
    return answer


"""
time: O(n * m) BFS
space: O(n * m + k (length of locations))
"""
