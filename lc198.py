from typing import List

"""
You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed, the only constraint stopping you from robbing each of them is that adjacent houses have security systems connected and it will automatically contact the police if two adjacent houses were broken into on the same night.

Given an integer array nums representing the amount of money of each house, return the maximum amount of money you can rob tonight without alerting the police.
"""


class Solution
    def rob(self, nums: List[int]) -> int:
        # edge case
        if len(nums) == 0:
            return 0
        if len(nums) == 1:
            return nums[0]

        # keep track of rolling sums
        dp = [0] * (len(nums))

        # dp base cases
        dp[0] = nums[0]
        dp[1] = max(nums[0], nums[1])

        # dp = [1, 2, 0, 0]
        for i in range(2, len(nums)):
            # at each index, we need to find the max profit up until that index
            # which means taking the max of the combinations of robbing/not robbing
            # for each index, take the max of dp[i-2] + house[i] and dp[i-1]
            dp[i] = max(nums[i] + dp[i - 2], dp[i - 1])

        return dp[-1]


def main():
    obj = Solution()
    assert obj.rob([1, 2, 3, 1]) == 4
    assert obj.rob([2, 7, 9, 3, 1]) == 12


if __name__ == "__main__":
    main()
