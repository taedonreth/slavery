from typing import List

"""
You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed. All houses at this place are arranged in a circle. That means the first house is the neighbor of the last one. Meanwhile, adjacent houses have a security system connected, and it will automatically contact the police if two adjacent houses were broken into on the same night.
"""


class Solution:
    def rob(self, nums: List[int]) -> int:
        """
        Given an integer array nums representing the amount of money of each house, return the maximum amount of money you can rob tonight without alerting the police.
        """
        """
        either rob nums[0] and nums[-2] or nums[1] and nums[-1] then change bounds depending on
        which yields more continue with house robber 1?
        """
        n = len(nums)

        if n == 0:
            return 0
        elif n == 1:
            return nums[0]
        elif n == 2:
            return max(nums[0], nums[1])

        # case where you rob nums[0] (include first one, exclude last)
        first = [0] * n
        first[0] = nums[0]
        first[1] = nums[0]
        for i in range(2, n - 1):
            first[i] = max(nums[i] + first[i - 2], first[i - 1])

        # case where you rob nums[1] (exclude first, include last
        second = [0] * n
        second[1] = nums[1]
        for i in range(2, n):
            second[i] = max(nums[i] + second[i - 2], second[i - 1])

        return max(first[-2], second[-1])


def main():

    obj = Solution()
    assert obj.rob([2, 3, 2]) == 3
    assert obj.rob([1, 2, 3, 1]) == 4
    assert obj.rob([1, 2, 3]) == 3


# [1, 2, 3, 4, 5, 6, 7, 8, 9]
# [1, 2, 3, 4, 5]
if __name__ == "__main__":
    main()
