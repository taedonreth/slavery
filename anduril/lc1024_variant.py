"""
You are given a list of intervals that represent available coverage segments on a number line.
Each interval is given as [starti, endi] and represents a segment that can cover the range between starti and endi, inclusive.

Your goal is to cover a given **target interval [start, end]** using the **minimum number of intervals**.
Intervals can overlap, and you can use parts of them freely.

Return the minimum number of intervals needed to completely cover [start, end].
If it is impossible to cover the entire target range, return -1.

---

Example 1:

Input: intervals = [[0,2],[4,6],[8,10],[1,9],[1,5],[5,9]], target = [0, 10]
Output: 3
Explanation: We take intervals [0,2], [8,10], [1,9]; a total of 3 intervals.
We can reconstruct [0,10] by combining [0,2], [2,8], and [8,10].

Example 2:

Input: intervals = [[3,5],[4,8],[9,11],[8,10],[5,9]], target = [3,10]
Output: 3
Explanation:
We can take [3,5], [5,9], [8,10].
They together cover [3,10].

Example 3:

Input: intervals = [[0,4],[2,6],[5,8],[7,10]], target = [3,9]
Output: 2
Explanation:
We can take [2,6] and [5,8] to cover [3,9].

Example 4:

Input: intervals = [[0,1],[1,2]], target = [3,5]
Output: -1
Explanation:
All intervals are before the target range, so coverage is impossible.

---

Constraints:

- 1 <= intervals.length <= 10⁵
- 0 <= starti <= endi <= 10⁹
- intervals are sorted by starti in non-decreasing order
- 0 <= start < end <= 10⁹
"""

from typing import List


class Solution:
    def intervalStitching(self, intervals: List[List[int]], target: List[int]) -> int:
        """
        Greedy approach to find minimum number of intervals to cover target range.
        
        Strategy:
        1. Sort intervals by start time
        2. At each step, find all intervals that can extend our current coverage
        3. Among those, pick the one that reaches the furthest
        4. Repeat until we cover the target end or determine it's impossible
        
        Time: O(n log n) for sorting + O(n) for traversal = O(n log n)
        Space: O(1) if we don't count sorting space
        """
        # Sort by start time (problem says sorted, but let's be safe)
        intervals.sort()
        
        start, end = target[0], target[1]
        current_end = start  # Tracks how far we've covered so far
        count = 0  # Number of intervals used
        i = 0  # Pointer to current interval
        n = len(intervals)
        
        while current_end < end:
            max_reach = current_end  # Furthest we can reach in this step
            
            # Look at all intervals that can connect to our current coverage
            # (i.e., intervals that start at or before current_end)
            while i < n and intervals[i][0] <= current_end:
                # Among these intervals, track the one that extends furthest
                max_reach = max(max_reach, intervals[i][1])
                i += 1
            
            # If we couldn't extend our coverage, it's impossible
            if max_reach == current_end:
                return -1
            
            # Update our coverage and increment count
            current_end = max_reach
            count += 1
        
        return count


if __name__ == "__main__":
    sol = Solution()

    # Example 1
    intervals1 = [[0, 2], [4, 6], [8, 10], [1, 9], [1, 5], [5, 9]]
    target1 = [0, 10]
    assert sol.intervalStitching(intervals1, target1) == 3

    # Example 2
    intervals2 = [[3, 5], [4, 8], [9, 11], [8, 10], [5, 9]]
    target2 = [3, 10]
    assert sol.intervalStitching(intervals2, target2) == 3

    # Example 3
    intervals3 = [[0, 4], [2, 6], [5, 8], [7, 10]]
    target3 = [3, 9]
    assert sol.intervalStitching(intervals3, target3) == 3

    # Example 4
    intervals4 = [[0, 1], [1, 2]]
    target4 = [3, 5]
    assert sol.intervalStitching(intervals4, target4) == -1

    # Example 5: exact overlap
    intervals5 = [[3, 4], [4, 5], [5, 6]]
    target5 = [3, 6]
    assert sol.intervalStitching(intervals5, target5) == 3

    # Example 6: already covered
    intervals6 = [[2, 10]]
    target6 = [3, 9]
    assert sol.intervalStitching(intervals6, target6) == 1

    # Example 7: partial overlaps, sorted input
    intervals7 = [[1, 4], [3, 5], [4, 7], [6, 9], [8, 10]]
    target7 = [3, 10]
    assert sol.intervalStitching(intervals7, target7) == 4

    print("✅ All test cases passed!")
