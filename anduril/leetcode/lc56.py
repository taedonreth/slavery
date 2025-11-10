# leetcode 56: merge intervals (medium)

"""
Given an array of intervals where intervals[i] = [starti, endi], merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.



Example 1:

Input: intervals = [[1,3],[2,6],[8,10],[15,18]]
Output: [[1,6],[8,10],[15,18]]
Explanation: Since intervals [1,3] and [2,6] overlap, merge them into [1,6].
Example 2:

Input: intervals = [[1,4],[4,5]]
Output: [[1,5]]
Explanation: Intervals [1,4] and [4,5] are considered overlapping.
Example 3:

Input: intervals = [[4,7],[1,4]]
Output: [[1,7]]
Explanation: Intervals [1,4] and [4,7] are considered overlapping.


Constraints:

1 <= intervals.length <= 104
intervals[i].length == 2
0 <= starti <= endi <= 104
"""

from typing import List


class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        """
        keep track of result interval that includes all intervals we've currently seen (merged already)
        keep track of our current interval and the interval and reference result arr[-1] to see most recent interval
        sort intervals
            see if it overlaps with our previous interval
                if so, merge it into the last interval in res arr
                else, just add it as it is into res arr

        how do we know if it overlaps?
            if the start of our candidate interval is less than or equal to the last interval in res
        how do we merge?
            edit the end num of last interval in res to be max of current end num of last interval in res and end of candidate interval
        """

        intervals.sort(key=lambda x: x[0])
        res = [intervals[0]]

        for interval in intervals[1:]:
            if interval[0] <= res[-1][1]:
                res[-1][1] = max(res[-1][1], interval[1])
            else:
                res.append(interval)

        return res


if __name__ == "__main__":
    s = Solution()

    # Example 1
    intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]
    assert s.merge(intervals) == [[1, 6], [8, 10], [15, 18]]

    # Example 2
    intervals = [[1, 4], [4, 5]]
    assert s.merge(intervals) == [[1, 5]]

    # Example 3
    intervals = [[4, 7], [1, 4]]
    assert s.merge(intervals) == [[1, 7]]

    # Edge case: single interval
    intervals = [[1, 2]]
    assert s.merge(intervals) == [[1, 2]]

    # Edge case: all intervals disjoint
    intervals = [[1, 2], [3, 4], [5, 6]]
    assert s.merge(intervals) == [[1, 2], [3, 4], [5, 6]]

    # Edge case: all intervals overlapping into one
    intervals = [[1, 3], [2, 4], [3, 5], [4, 6]]
    assert s.merge(intervals) == [[1, 6]]

    # Edge case: unsorted input
    intervals = [[5, 10], [1, 3], [2, 6], [15, 18]]
    assert s.merge(intervals) == [[1, 10], [15, 18]]

    # Edge case: nested intervals
    intervals = [[1, 10], [2, 3], [4, 8], [9, 10]]
    assert s.merge(intervals) == [[1, 10]]

    # Edge case: touching intervals at boundaries
    intervals = [[1, 2], [2, 3], [3, 4], [4, 5]]
    assert s.merge(intervals) == [[1, 5]]

    # Large but simple case
    intervals = [[i, i + 1] for i in range(0, 10000, 2)]  # disjoint intervals
    expected = [[i, i + 1] for i in range(0, 10000, 2)]
    assert s.merge(intervals) == expected

    print("✅ All test cases passed!")
