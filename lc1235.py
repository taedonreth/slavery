# leetcode 1235: maximum profit in job scheduling

from typing import List

"""
We have n jobs, where every job is scheduled to be done from startTime[i] to endTime[i], obtaining a profit of profit[i].
You're given the startTime, endTime and profit arrays, return the maximum profit you can take such 
    that there are no two jobs in the subset with overlapping time range.
If you choose a job that ends at time X you will be able to start another job that starts at time X.
"""


class Solution:
    def jobScheduling(
        self, startTime: List[int], endTime: List[int], profit: List[int]
    ) -> int:
        """
        dp for sure
        sort by start time
        2d matrix
            row = start time
            col = end time
            kk
        """
        pass


def main():
    s = Solution()

    # Example 1
    startTime = [1, 2, 3, 3]
    endTime = [3, 4, 5, 6]
    profit = [50, 10, 40, 70]
    expected = 120
    assert s.jobScheduling(startTime, endTime, profit) == expected

    # Example 2
    startTime = [1, 2, 3, 4, 6]
    endTime = [3, 5, 10, 6, 9]
    profit = [20, 20, 100, 70, 60]
    expected = 150
    assert s.jobScheduling(startTime, endTime, profit) == expected

    # Example 3
    startTime = [1, 1, 1]
    endTime = [2, 3, 4]
    profit = [5, 6, 4]
    expected = 6
    assert s.jobScheduling(startTime, endTime, profit) == expected

    print("All test cases passed!")


if __name__ == "__main__":
    main()
