# leetcode 435: non-overlapping intervals (medium)

from typing import List

"""
Given an array of intervals intervals where intervals[i] = [starti, endi], return the minimum number of intervals you need 
    to remove to make the rest of the intervals non-overlapping.

Note that intervals which only touch at a point are non-overlapping. For example, [1, 2] and [2, 3] are non-overlapping.
"""


class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        """
        sort by start time
        start with intervals[0] in temp
        keep overlapping count
        iterate from 1 to len intervals
            if intervals[i] overlaps with temp[-1] at all
                expand temp[-1]
                if intervals[i] overlaps but not at a point
                    increment overlapping count
            else:
                add intervals[i] temp

        return overlapping count
        """

        # [[1, 2], [1, 3], [2, 3], [3, 4]]
        intervals.sort(key=lambda x: x[1])
        temp = [intervals[0]]
        overlapping_count = 0

        for i in range(1, len(intervals)):
            if intervals[i][0] < temp[-1][1]:
                overlapping_count += 1
            else:
                temp.append(intervals[i])

        return overlapping_count


def main():
    sol = Solution()
    # Test Example 1
    intervals1 = [[1, 2], [2, 3], [3, 4], [1, 3]]
    expected1 = 1
    result1 = sol.eraseOverlapIntervals(intervals1)
    assert (
        result1 == expected1
    ), f"Example 1 failed: expected {expected1}, got {result1}"
    print(f"✓ Example 1 passed: {intervals1} -> {result1}")

    # Test Example 2
    intervals2 = [[1, 2], [1, 2], [1, 2]]
    expected2 = 2
    result2 = sol.eraseOverlapIntervals(intervals2)
    assert (
        result2 == expected2
    ), f"Example 2 failed: expected {expected2}, got {result2}"
    print(f"✓ Example 2 passed: {intervals2} -> {result2}")

    # Test Example 3
    intervals3 = [[1, 2], [2, 3]]
    expected3 = 0
    result3 = sol.eraseOverlapIntervals(intervals3)
    assert (
        result3 == expected3
    ), f"Example 3 failed: expected {expected3}, got {result3}"
    print(f"✓ Example 3 passed: {intervals3} -> {result3}")

    print("All test cases passed!")


if __name__ == "__main__":
    main()
