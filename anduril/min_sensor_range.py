"""
You are building a simplified border security system. 
There are detection towers placed along a 1D border line, and several known border crossing locations. 
Each tower can detect crossings within a certain range `r`. 
That means if a tower is located at position `t`, it can detect any crossing within the interval `[t - r, t + r]`.

Your task is to find the **minimum detection range `r`** such that **every border crossing** can be detected by at least one tower.

Formally:
- You are given two integer arrays:
  - `crossings` representing the positions of known border crossings.
  - `towers` representing the positions of detection towers.

Return the minimum integer `r` such that every crossing lies within at least one tower’s range.

---

Example 1:

Input: crossings = [1, 2, 3, 4, 6, 10, 12], towers = [1, 4, 6]
Output: 6
Explanation:
With r = 6, the coverage is:
- Tower at 1 covers [-5, 7]
- Tower at 4 covers [-2, 10]
- Tower at 6 covers [0, 12]
All crossings are covered.
If r = 5, crossing 12 would not be detected.

Example 2:

Input: crossings = [2, 5, 9], towers = [4]
Output: 5
Explanation:
The single tower at 4 must cover up to crossing 9 → range at least 5.

Example 3:

Input: crossings = [1, 10], towers = [5]
Output: 5
Explanation:
Tower 5 must detect both 1 and 10 → r = max(5-1, 10-5) = 5.

Example 4:

Input: crossings = [1, 2, 3], towers = [10]
Output: 9
Explanation:
The only tower is too far — it must cover all crossings from 1 to 3, requiring r ≥ 9.

---

Constraints:

- 1 <= crossings.length, towers.length <= 10⁵  
- 0 <= crossings[i], towers[i] <= 10⁹  
- All values in `crossings` and `towers` are unique  
- The arrays are not necessarily sorted
"""


from typing import List


class Solution:
    def find_leftmost_tower_gte(self, towers_sorted: List[int], crossing: int) -> int:
        """
        Binary search to find the leftmost tower >= crossing.
        
        Returns the index of the leftmost tower >= crossing,
        or len(towers_sorted) if no such tower exists.
        
        Pattern: Find leftmost element satisfying a condition
        """
        left = 0
        right = len(towers_sorted) - 1
        candidate = len(towers_sorted)  # Default: no tower >= crossing found
        
        while left <= right:
            mid = (left + right) // 2
            
            if towers_sorted[mid] >= crossing:
                # This tower satisfies our condition
                candidate = mid
                # But there might be a smaller index that also works
                right = mid - 1
            else:
                # towers_sorted[mid] < crossing
                # We need to look further right
                left = mid + 1
        
        return candidate
    
    def minSensorRange(self, crossings: List[int], towers: List[int]) -> int:
        """
        Find minimum detection range r such that all crossings are covered.
        
        Key Insight:
        - For each crossing, we need at least one tower within range r
        - The minimum range needed for a crossing = distance to its nearest tower
        - To cover ALL crossings, r must be the maximum of these minimum distances
        
        Optimization Strategy:
        1. Sort the towers array
        2. For each crossing, use binary search to find closest tower
        3. Check both the tower at/before and after the crossing position
        4. The answer is the maximum of all minimum distances
        
        Why binary search works:
        - Once towers are sorted, the closest tower to a crossing must be
          either the largest tower ≤ crossing, or the smallest tower > crossing
        - We can find these in O(log T) time using binary search
        
        Time: O(T log T + C log T) = O((C + T) log T)
        Space: O(T) for sorting (or O(log T) if sorting in-place)
        """
        # Sort towers for binary search
        towers_sorted = sorted(towers)
        max_min_distance = 0
        
        # For each crossing, find its nearest tower using binary search
        for crossing in crossings:
            # Find the leftmost tower >= crossing
            idx = self.find_leftmost_tower_gte(towers_sorted, crossing)
            
            min_distance = float('inf')
            
            # Check the tower just before idx (largest tower < crossing)
            if idx > 0:
                distance = abs(crossing - towers_sorted[idx - 1])
                min_distance = min(min_distance, distance)
            
            # Check the tower at idx (smallest tower >= crossing)
            if idx < len(towers_sorted):
                distance = abs(crossing - towers_sorted[idx])
                min_distance = min(min_distance, distance)
            
            # Track the maximum of these minimum distances
            max_min_distance = max(max_min_distance, min_distance)
        
        return max_min_distance


if __name__ == "__main__":
    sol = Solution()

    # Example 1
    crossings1 = [1, 2, 3, 4, 6, 10, 12]
    towers1 = [1, 4, 6]
    assert sol.minSensorRange(crossings1, towers1) == 6

    # Example 2
    crossings2 = [2, 5, 9]
    towers2 = [4]
    assert sol.minSensorRange(crossings2, towers2) == 5

    # Example 3
    crossings3 = [1, 10]
    towers3 = [5]
    assert sol.minSensorRange(crossings3, towers3) == 5

    # Example 4
    crossings4 = [1, 2, 3]
    towers4 = [10]
    assert sol.minSensorRange(crossings4, towers4) == 9

    # Edge case: exact overlap
    crossings5 = [5, 6, 7]
    towers5 = [6]
    assert sol.minSensorRange(crossings5, towers5) == 1

    # Edge case: interleaved positions
    crossings6 = [1, 8, 15]
    towers6 = [3, 10]
    assert sol.minSensorRange(crossings6, towers6) == 5

    print("✅ All test cases passed!")

