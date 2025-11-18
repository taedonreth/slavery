# leetcode 475: heaters (medium)

"""
Winter is coming! During the contest, your first job is to design a standard heater with a fixed warm radius to warm all the houses.

Every house can be warmed, as long as the house is within the heater's warm radius range. 

Given the positions of houses and heaters on a horizontal line, return the minimum radius standard of heaters so that those heaters could cover all houses.

Notice that all the heaters follow your radius standard, and the warm radius will be the same.

 

Example 1:

Input: houses = [1,2,3], heaters = [2]
Output: 1
Explanation: The only heater was placed in the position 2, and if we use the radius 1 standard, then all the houses can be warmed.
Example 2:

Input: houses = [1,2,3,4], heaters = [1,4]
Output: 1
Explanation: The two heaters were placed at positions 1 and 4. We need to use a radius 1 standard, then all the houses can be warmed.
Example 3:

Input: houses = [1,5], heaters = [2]
Output: 3
 

Constraints:

1 <= houses.length, heaters.length <= 3 * 104
1 <= houses[i], heaters[i] <= 109
"""

from typing import List

class Solution:

    def find_leftmost_heater_gte(self, heaters_sorted: List[int], house: int) -> int:
        """
        Binary search to find the leftmost heater >= home.
        """
        left = 0
        right = len(heaters_sorted) - 1
        candidate = len(heaters_sorted)
        
        while left <= right:
            mid = (left + right) // 2
            
            if heaters_sorted[mid] >= house:
                candidate = mid
                # But there might be a smaller index that also works
                right = mid - 1
            else:
                left = mid + 1
        
        return candidate

    def findRadius(self, houses: List[int], heaters: List[int]) -> int:

        heaters_sorted = sorted(heaters)
        max_min_distance = 0
        
        # For each house, find its nearest heater using binary search
        for house in houses:
            # Find the leftmost heater >= house
            idx = self.find_leftmost_heater_gte(heaters_sorted, house)
            
            min_distance = float('inf')
            
            # Check the tower just before idx (largest tower < crossing)
            if idx > 0:
                distance = abs(house - heaters_sorted[idx - 1])
                min_distance = min(min_distance, distance)
            
            # Check the tower at idx (smallest tower >= crossing)
            if idx < len(heaters_sorted):
                distance = abs(house - heaters_sorted[idx])
                min_distance = min(min_distance, distance)
            
            # Track the maximum of these minimum distances
            max_min_distance = max(max_min_distance, min_distance)
        
        return max_min_distance


if __name__ == "__main__":
    s = Solution()

    # Example 1
    houses = [1,2,3]
    heaters = [2]
    assert s.findRadius(houses, heaters) == 1, "Example 1 failed"

    # Example 2
    houses = [1,2,3,4]
    heaters = [1,4]
    assert s.findRadius(houses, heaters) == 1, "Example 2 failed"

    # Example 3
    houses = [1,5]
    heaters = [2]
    assert s.findRadius(houses, heaters) == 3, "Example 3 failed"

    # Additional custom tests

    # Single house & single heater, same position
    houses = [10]
    heaters = [10]
    assert s.findRadius(houses, heaters) == 0, "Single same pos test failed"

    # House left of all heaters
    houses = [1, 2, 3]
    heaters = [10]
    # nearest for house 1 → distance 9
    assert s.findRadius(houses, heaters) == 9, "Left side distance test failed"

    # House right of all heaters
    houses = [20, 30]
    heaters = [5]
    # nearest for 30 → distance 25
    assert s.findRadius(houses, heaters) == 25, "Right side distance test failed"

    # Mixed positions
    houses = [1, 4, 8, 12]
    heaters = [2, 9]
    # distances: 1→1, 4→2, 8→1, 12→3 → answer = 3
    assert s.findRadius(houses, heaters) == 3, "Mixed test failed"

    print("All tests passed!")