# leetcode 207: course schedule (medium)

"""
There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai.

For example, the pair [0, 1], indicates that to take course 0 you have to first take course 1.
Return true if you can finish all courses. Otherwise, return false.



Example 1:

Input: numCourses = 2, prerequisites = [[1,0]]
Output: true
Explanation: There are a total of 2 courses to take.
To take course 1 you should have finished course 0. So it is possible.
Example 2:

Input: numCourses = 2, prerequisites = [[1,0],[0,1]]
Output: false
Explanation: There are a total of 2 courses to take.
To take course 1 you should have finished course 0, and to take course 0 you should also have finished course 1. So it is impossible.


Constraints:

1 <= numCourses <= 2000
0 <= prerequisites.length <= 5000
prerequisites[i].length == 2
0 <= ai, bi < numCourses
All the pairs prerequisites[i] are unique.
"""


class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        pass


if __name__ == "__main__":
    sol = Solution()

    # Example 1
    numCourses1 = 2
    prereq1 = [[1, 0]]
    assert sol.canFinish(numCourses1, prereq1) == True

    # Example 2
    numCourses2 = 2
    prereq2 = [[1, 0], [0, 1]]
    assert sol.canFinish(numCourses2, prereq2) == False

    # No prerequisites -> always possible
    numCourses3 = 5
    prereq3 = []
    assert sol.canFinish(numCourses3, prereq3) == True

    # Chain of dependencies, no cycle
    numCourses4 = 4
    prereq4 = [[1, 0], [2, 1], [3, 2]]
    assert sol.canFinish(numCourses4, prereq4) == True

    # Cycle in longer chain
    numCourses5 = 4
    prereq5 = [[1, 0], [2, 1], [0, 2]]
    assert sol.canFinish(numCourses5, prereq5) == False

    # Disconnected components, no cycle
    numCourses6 = 6
    prereq6 = [[1, 0], [3, 2], [5, 4]]
    assert sol.canFinish(numCourses6, prereq6) == True

    # Disconnected components, one has a cycle
    numCourses7 = 6
    prereq7 = [[1, 0], [3, 2], [5, 4], [4, 5]]
    assert sol.canFinish(numCourses7, prereq7) == False

    # Self dependency
    numCourses8 = 3
    prereq8 = [[0, 0]]
    assert sol.canFinish(numCourses8, prereq8) == False

    # Large linear chain (stress test)
    numCourses9 = 1000
    prereq9 = [[i + 1, i] for i in range(999)]
    assert sol.canFinish(numCourses9, prereq9) == True

    print("✅ All test cases passed!")
