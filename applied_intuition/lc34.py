# leetcode 34: find first and last position of element in sorted array

from typing import List

class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        """
        input: nums = [5,7,7,8,8,10], target = 8
        output: [3,4]

        sorted so the value will be in a continuous interval
        O(log n) time so binary search to find indexs of target

        binary search:
        we need to find a range, not a specific value, so go until left <= right
        if we land on a value lower than target, left = mid + 1
        otherwise, right = mid - 1

        """ 

        if not nums:
            return [-1, -1]
        
        # First binary search - find leftmost occurrence
        left, right = 0, len(nums) - 1
        first = -1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == target:
                first = mid
                right = mid - 1  # Keep searching left
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        if first == -1:  # Target not found
            return [-1, -1]
        
        # Second binary search - find rightmost occurrence
        left, right = 0, len(nums) - 1
        last = -1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == target:
                last = mid
                left = mid + 1  # Keep searching right
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return [first, last]
        
        
def main():
    sol = Solution()

    # Example 1
    assert sol.searchRange([5,7,7,8,8,10], 8) == [3,4]

    # Example 2
    assert sol.searchRange([5,7,7,8,8,10], 6) == [-1,-1]

    # Example 3
    assert sol.searchRange([], 0) == [-1,-1]

    # Extra edge cases
    assert sol.searchRange([1], 1) == [0,0]           # single element, matches
    assert sol.searchRange([1], 2) == [-1,-1]         # single element, no match
    assert sol.searchRange([2,2,2,2,2], 2) == [0,4]   # all elements same
    assert sol.searchRange([1,2,3,4,5], 1) == [0,0]   # target at start
    assert sol.searchRange([1,2,3,4,5], 5) == [4,4]   # target at end

    print("All test cases passed!")

if __name__ == "__main__":
    main()
