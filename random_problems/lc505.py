# leetcode 505: the maze II (medium)

from typing import List

"""
There is a ball in a maze with empty spaces (represented as 0) and walls (represented as 1). The ball can go through the empty spaces by rolling up, down, left or right, but it won't stop rolling until hitting a wall. When the ball stops, it could choose the next direction.

Given the m x n maze, the ball's start position and the destination, where start = [startrow, startcol] and destination = [destinationrow, destinationcol], return the shortest distance for the ball to stop at the destination. If the ball cannot stop at destination, return -1.

The distance is the number of empty spaces traveled by the ball from the start position (excluded) to the destination (included).

You may assume that the borders of the maze are all walls (see examples).
"""


class Solution:
    def shortestDistance(
        self, maze: List[List[int]], start: List[int], destination: List[int]
    ) -> int:
        """
        same as the maze I, but shortest distance this time so bfs
        """
        pass


def main():
    sol = Solution()

    # Example 1
    maze1 = [
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0],
        [1, 1, 0, 1, 1],
        [0, 0, 0, 0, 0],
    ]
    start1 = [0, 4]
    dest1 = [4, 4]
    result1 = sol.shortestDistance(maze1, start1, dest1)
    print(f"Example 1: {result1}")
    assert result1 == 12

    # Example 2
    maze2 = [
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0],
        [1, 1, 0, 1, 1],
        [0, 0, 0, 0, 0],
    ]
    start2 = [0, 4]
    dest2 = [3, 2]
    result2 = sol.shortestDistance(maze2, start2, dest2)
    print(f"Example 2: {result2}")
    assert result2 == -1

    # Example 3
    maze3 = [
        [0, 0, 0, 0, 0],
        [1, 1, 0, 0, 1],
        [0, 0, 0, 0, 0],
        [0, 1, 0, 0, 1],
        [0, 1, 0, 0, 0],
    ]
    start3 = [4, 3]
    dest3 = [0, 1]
    result3 = sol.shortestDistance(maze3, start3, dest3)
    print(f"Example 3: {result3}")
    assert result3 == -1

    # Additional test case - simple path
    maze4 = [
        [0, 0, 0, 0, 0],
        [1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1],
        [0, 0, 0, 0, 0],
    ]
    start4 = [0, 0]
    dest4 = [2, 4]
    result4 = sol.shortestDistance(maze4, start4, dest4)
    print(f"Example 4: {result4}")

    print("All tests passed!")


if __name__ == "__main__":
    main()
