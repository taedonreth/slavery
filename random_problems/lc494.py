# leetcode 494: target sum (medium)

"""
You are given an integer array nums and an integer target.

You want to build an expression out of nums by adding one of the symbols '+' and '-' before each integer in nums and then concatenate all the integers.

For example, if nums = [2, 1], you can add a '+' before 2 and a '-' before 1 and concatenate them to build the expression "+2-1".
Return the number of different expressions that you can build, which evaluates to target.
"""


class Solution:
    def findTargetSumWays(self, nums, target):
        pass


def main():
    solution = Solution()

    # Test Example 1
    nums1 = [1, 1, 1, 1, 1]
    target1 = 3
    expected1 = 5
    result1 = solution.findTargetSumWays(nums1, target1)
    assert (
        result1 == expected1
    ), f"Example 1 failed: expected {expected1}, got {result1}"
    print(f"✓ Example 1 passed: nums={nums1}, target={target1} -> {result1}")

    # Test Example 2
    nums2 = [1]
    target2 = 1
    expected2 = 1
    result2 = solution.findTargetSumWays(nums2, target2)
    assert (
        result2 == expected2
    ), f"Example 2 failed: expected {expected2}, got {result2}"
    print(f"✓ Example 2 passed: nums={nums2}, target={target2} -> {result2}")

    print("All test cases passed!")


if __name__ == "__main__":
    main()
