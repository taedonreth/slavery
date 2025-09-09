# leetcode 162: find peak element (medium)

from typing import List

"""
A peak element is an element that is strictly greater than its neighbors.
You may imagine that nums[-1] = nums[n] = -∞. In other words, an element is always considered to be strictly greater than a neighbor that is outside the array.
"""


class Solution:
    # Given a 0-indexed integer array nums, find a peak element, and return its index.
    # If the array contains multiple peaks, return the index to any of the peaks. (first peak)
    # You must write an algorithm that runs in O(log n) time.
    def findPeakElement(self, nums: List[int]) -> int:
        """
        O(n) solution: iterate through and track i, i-1 and i + 1
            return i if nums[i] > nums[i] - 1 and nums[i] > nums[i] + 1

        note: adjacent elements cannot be the same, outside of arrays are -infinity
            this means we are guaranteed to have a peak in each half of nums

        O(log n) solution: how do we find a peak looking at half the elements?
            binary search
            test middle element
            if it is greater than the one to the right
                we are in a downhill slope, so bs left half
            if it is less than the one to the right
                we are in a uphill slope, so bs right half
            # we will eventually converge on the peak in either case because we
            # we find an index where it is no longer downhill/uphill
        """
        left, right = 0, len(nums) - 1
        while left < right:
            mid = (right + left) // 2
            if nums[mid] > nums[mid + 1]:
                right = mid
            else:
                left = mid + 1

        return left


def main():
    s = Solution()

    # Example 1
    nums = [1, 2, 3, 1]
    assert s.findPeakElement(nums) == 2  # peak at index 2

    # Example 2
    nums = [1, 2, 1, 3, 5, 6, 4]
    res = s.findPeakElement(nums)
    assert res in [1, 5]  # valid peaks are at index 1 (2) or index 5 (6)

    print("All tests passed!")


if __name__ == "__main__":
    main()
