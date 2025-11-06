# leetcode 1838: frequency of the most frequent element (medium)

from typing import List

class Solution:
    def maxFrequency(self, nums: List[int], k: int) -> int:
        # Step 1: Sort the array
        nums.sort()

        left = 0
        right = 0 # Initialize right pointer
        current_sum = 0
        max_length = 0

        # Use a while loop to expand the window
        while right < len(nums):
            current_sum += nums[right]
            window_length = right - left + 1

            # Calculate the cost to make all elements in the window equal to the largest
            cost = (window_length * nums[right]) - current_sum

            # If the cost is too high, shrink the window from the left
            if cost > k:
                current_sum -= nums[left]
                left += 1

            # The current window is the longest we've seen so far
            max_length = right - left + 1
            
            # Manually increment the right pointer
            right += 1

        return max_length