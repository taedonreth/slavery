# leetcode 54: merge intervals  (medium)

from typing import List


class Solution:
    """
    Given an array of intervals where intervals[i] = [starti, endi], merge all overlapping intervals,
        and return an array of the non-overlapping intervals that cover all the intervals in the input.
    """

    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        """
        sort intervals by starting value
        iterate through intervals
        for each interval
            check if it overlaps with previous interval in result
            if it does
                expand last merged to accomodate it
            if it doesnt
                add it to result
        """
        if not intervals:
            return []

        intervals.sort(key=lambda x: x[0])
        result = [intervals[0]]

        for i in range(1, len(intervals)):
            current_interval = intervals[i]
            last_merged = result[-1]

            # current interval overlaps with the last merged interval
            if last_merged[1] >= current_interval[0]:
                last_merged[1] = max(last_merged[1], current_interval[1])
            else:
                result.append(current_interval)

        return result


def main():
    sol = Solution()
    # Example 1
    intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]
    expected = [[1, 6], [8, 10], [15, 18]]
    assert sol.merge(intervals) == expected

    # Example 2
    intervals = [[1, 4], [4, 5]]
    expected = [[1, 5]]
    assert sol.merge(intervals) == expected

    # Example 3
    intervals = [[4, 7], [1, 4]]
    expected = [[1, 7]]
    assert sol.merge(intervals) == expected

    print("All test cases passed!")


if __name__ == "__main__":
    main()
