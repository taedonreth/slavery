# leetcode 46: permutations (medium)

from typing import List


class Solution:
    # Given an array nums of distinct integers, return all the possible permutations. You can return the answer in any order.
    def permute(self, nums: List[int]) -> List[List[int]]:
        """
        backtracking
        need to recurse and backtrack to try the new combinations
        """

        # backtrack function that builds all permutations of a list given a current list
        def backtrack(curr: List[int]) -> None:
            if len(curr) == len(nums):
                res.append(curr[:])
                return

            for num in nums:
                if num not in curr:
                    curr.append(num)
                    backtrack(curr)
                    curr.pop()

        res = []
        backtrack([])
        return res


def main():
    sol = Solution()

    # Example 1
    nums1 = [1, 2, 3]
    result1 = sol.permute(nums1)
    expected1 = [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    assert set(tuple(p) for p in result1) == set(tuple(p) for p in expected1)

    # Example 2
    nums2 = [0, 1]
    result2 = sol.permute(nums2)
    expected2 = [[0, 1], [1, 0]]
    assert set(tuple(p) for p in result2) == set(tuple(p) for p in expected2)

    # Example 3
    nums3 = [1]
    result3 = sol.permute(nums3)
    expected3 = [[1]]
    assert set(tuple(p) for p in result3) == set(tuple(p) for p in expected3)

    # Extra test
    nums4 = [1, 2]
    result4 = sol.permute(nums4)
    expected4 = [[1, 2], [2, 1]]
    assert set(tuple(p) for p in result4) == set(tuple(p) for p in expected4)

    print("All test cases passed!")


if __name__ == "__main__":
    main()
