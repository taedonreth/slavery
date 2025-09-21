# leetcode 845: longest mountain in array (medium)

from typing import List


class Solution:
    """
    You may recall that an array arr is a mountain array if and only if:
        arr.length >= 3
        There exists some index i (0-indexed) with 0 < i < arr.length - 1 such that:
        arr[0] < arr[1] < ... < arr[i - 1] < arr[i]
        arr[i] > arr[i + 1] > ... > arr[arr.length - 1]
    """

    def longestMountain(self, arr: List[int]) -> int:
        # Given an integer array arr, return the length of the longest subarray, which is a mountain. Return 0 if there is no mountain subarray.

        # no mountains if len(arr) < 3
        if len(arr) < 3:
            return 0

        # mountain can exist
        max_mountain_len = 0

        # loop to find mountain len, store it in curr_mountain_len
        # update max_mountain_len as we iterate
        # sliding window - at each index, find uphill -> find peak -> find downhill -> store length
        i = 0
        while i < len(arr):
            base = i
            if base + 1 < len(arr) and arr[base + 1] > arr[base]:
                while i + 1 < len(arr) and arr[i + 1] > arr[i]:
                    i += 1

                if i + 1 < len(arr) and arr[i + 1] < arr[i]:
                    while i + 1 < len(arr) and arr[i + 1] < arr[i]:
                        i += 1
                        curr_mountain_len = i - base + 1
                    max_mountain_len = max(curr_mountain_len, max_mountain_len)
                else:
                    i += 1
            else:
                i += 1

        return max_mountain_len


def main():
    sol = Solution()

    # Example 1
    arr1 = [2, 1, 4, 7, 3, 2, 5]
    assert sol.longestMountain(arr1) == 5  # [1,4,7,3,2]

    # Example 2
    arr2 = [2, 2, 2]
    assert sol.longestMountain(arr2) == 0  # no mountain

    # Extra Tests
    arr3 = [1, 2, 3, 4, 5, 4, 3, 2, 1]
    assert sol.longestMountain(arr3) == 9  # whole array is a mountain

    arr4 = [1, 3, 2]
    assert sol.longestMountain(arr4) == 3  # smallest valid mountain

    arr5 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert sol.longestMountain(arr5) == 0  # strictly increasing, no mountain

    print("All test cases passed!")


if __name__ == "__main__":
    main()
