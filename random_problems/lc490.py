# leetcode 490: the maze (medium)

from typing import List

"""
There is a ball in a maze with empty spaces (represented as 0) and walls (represented as 1). 
    The ball can go through the empty spaces by rolling up, down, left or right, but it won't stop rolling until hitting a wall. When the ball stops, it could choose the next direction.

Given the m x n maze, the ball's start position and the destination, where start = [startrow, startcol] and destination = [destinationrow, destinationcol], return true if the ball can stop at the destination, otherwise return false.

You may assume that the borders of the maze are all walls (see examples).
"""


class Solution:
    def hasPath(
        self, maze: List[List[int]], start: List[int], destination: List[int]
    ) -> bool:
        """
        dfs from starting position -> keep a visited set
            this dfs is difference because you need to continue in the initial
            direction until you hit a wall
            the way we deal with this is we try to repeat the direction
                if we cant, then choose a new one

            if we stop on destination, return true

        return false
        """
        visited = set()
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]

        def dfs(curr_pos):
            nonlocal directions
            if tuple(curr_pos) in visited:
                return False

            if curr_pos == tuple(destination):
                return True

            visited.add(tuple(curr_pos))

            for x, y in directions:
                dx, dy = curr_pos
                while (
                    0 <= dx + x < len(maze)
                    and 0 <= dy + y < len(maze[0])
                    and maze[dx + x][dy + y] == 0
                ):
                    dx += x
                    dy += y

                if dfs((dx, dy)):
                    return True

            return False

        return dfs(start)


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
    assert sol.hasPath(maze1, start1, dest1) == True

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
    assert sol.hasPath(maze2, start2, dest2) == False

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
    assert sol.hasPath(maze3, start3, dest3) == False

    print("All tests passed!")


if __name__ == "__main__":
    main()
