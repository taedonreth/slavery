# leetcode 55: jump game (medium)
from typing import List


class Solution:
    """
    You are given an integer array nums. You are initially positioned at the array's first index, and each element in the
        array represents your maximum jump length at that position.
    Return true if you can reach the last index, or false otherwise.
    """

    def canJump(self, nums: List[int]) -> bool:
        """
        brute: try every combination?
        optimization: greedy or dp
            try taking the maximum number of jumps you can
            keep track of furthest index you can reach
                keep adding to this as you iterate

            if you reach an index beyond the running furthest
                return false because you can't make it to the end

            if furthest >= len(nums)
                return true

            return false
        """
        max_idx = 0
        for i in range(len(nums)):
            if i > max_idx:
                return False

            max_idx = max(max_idx, i + nums[i])

        if max_idx >= len(nums) - 1:
            return True

        return False


def main():
    sol = Solution()

    # Example 1
    nums = [2, 3, 1, 1, 4]
    assert sol.canJump(nums) == True

    # Example 2
    nums = [3, 2, 1, 0, 4]
    assert sol.canJump(nums) == False

    # Extra test: single element (already at last index)
    nums = [0]
    assert sol.canJump(nums) == True

    # Extra test: can just barely reach the end
    nums = [2, 0, 0]
    assert sol.canJump(nums) == True

    # Extra test: stuck before the last index
    nums = [2, 0, 1, 0, 0]
    assert sol.canJump(nums) == False

    print("All tests passed!")


if __name__ == "__main__":
    main()
