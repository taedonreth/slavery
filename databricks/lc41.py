# leetcode 41: first missing positive (hard)

from typing import List


class Solution:
    """
    Given an unsorted integer array nums. Return the smallest positive integer that is not present in nums.
    You must implement an algorithm that runs in O(n) time and uses O(1) auxiliary space.
    """

    def firstMissingPositive(self, nums: List[int]) -> int:
        """
        obvious brute force is to iterate from 1 to len(nums) + 1
        if a number isn't in nums, return that number

        optimization:
            answer has to be between 1 and len(nums) + 1
            we can use indices to represent possible values and
            rearrange the array on first pass

            second pass to go through array
                return i + 1 if we see a gap at i

            return len(nums) + 1
        """

        i = 0
        while i < len(nums):
            correct_index = nums[i] - 1
            if 1 <= nums[i] <= len(nums) and nums[i] != nums[correct_index]:
                # swap
                nums[i], nums[correct_index] = nums[correct_index], nums[i]
            else:
                i += 1

        for i in range(len(nums)):
            if nums[i] != i + 1:
                return i + 1

        return len(nums) + 1


def main():
    sol = Solution()

    # Example cases
    assert sol.firstMissingPositive([1, 2, 0]) == 3
    assert sol.firstMissingPositive([3, 4, -1, 1]) == 2
    assert sol.firstMissingPositive([7, 8, 9, 11, 12]) == 1

    # Extra cases
    assert sol.firstMissingPositive([1, 2, 3]) == 4  # all consecutive → next one
    assert sol.firstMissingPositive([0]) == 1  # single non-positive
    assert sol.firstMissingPositive([-5, -10, -1]) == 1  # all negatives
    assert sol.firstMissingPositive([2, 2, 2, 2]) == 1  # duplicate 2s
    assert sol.firstMissingPositive([1]) == 2  # smallest case, already has 1
    assert sol.firstMissingPositive([2]) == 1  # smallest case, missing 1

    print("All tests passed!")


if __name__ == "__main__":
    main()
