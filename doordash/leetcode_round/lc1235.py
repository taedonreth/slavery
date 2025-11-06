# leetcode 1235: maxinum profit in job scheduling (hard)

"""
We have n jobs, where every job is scheduled to be done from startTime[i] to endTime[i], obtaining a profit of profit[i].

You're given the startTime, endTime and profit arrays, return the maximum profit you can take such that there are no two jobs in the subset with overlapping time range.

If you choose a job that ends at time X you will be able to start another job that starts at time X.
"""

from typing import List


class Solution:
    def jobScheduling(
        self, startTime: List[int], endTime: List[int], profit: List[int]
    ) -> int:
        n = len(startTime)

        # Combine job details and sort by start time
        jobs = sorted(zip(startTime, endTime, profit))
        startTime = [job[0] for job in jobs]  # sorted start times

        # Memo array: memo[i] = max profit from job i to end
        memo = [0] * n

        # Binary search to find next non-conflicting job
        def binarySearch(target):
            left, right = 0, n - 1
            result = n  # default if no job starts >= target

            while left <= right:
                mid = (left + right) // 2
                if startTime[mid] >= target:
                    result = mid  # potential answer
                    right = mid - 1  # keep searching left to find first
                else:
                    left = mid + 1  # move right

            return result

        # Build DP from the end to the start
        for position in range(n - 1, -1, -1):
            # Current job profit
            nextIndex = binarySearch(jobs[position][1])
            if nextIndex != n:
                currProfit = jobs[position][2] + memo[nextIndex]
            else:
                currProfit = jobs[position][2]

            # Maximum profit from position to end
            if position == n - 1:
                memo[position] = currProfit
            else:
                memo[position] = max(currProfit, memo[position + 1])

        return memo[0]


def jobScheduling(
    self, startTime: list[int], endTime: list[int], profit: list[int]
) -> int:
    # Binary search to find next non-conflicting job
    def binarySearch(target):
        left, right = 0, n - 1
        result = n  # default if no job starts >= target

        while left <= right:
            mid = (left + right) // 2
            if startTime[mid] >= target:
                result = mid  # potential answer
                right = mid - 1  # keep searching left to find first
            else:
                left = mid + 1  # move right

        return result

    # Combine and sort jobs by start time
    jobs = sorted(zip(startTime, endTime, profit))
    starts = [job[0] for job in jobs]
    n = len(jobs)

    # Initialize memoization array
    memo = [-1] * (n + 1)

    def findMaxProfit(position: int) -> int:
        # Base case: no more jobs left
        if position == n:
            return 0

        # Already computed → return from memo
        if memo[position] != -1:
            return memo[position]

        # Option 1: skip current job
        skip = findMaxProfit(position + 1)

        # Option 2: take current job → add its profit + next valid job
        next_index = binarySearch(jobs[position][1])
        take = jobs[position][2] + findMaxProfit(next_index)

        # Store and return best option
        memo[position] = max(skip, take)
        return memo[position]

    return findMaxProfit(0)


"""
time: O(n log n)
space: O(n)
"""
