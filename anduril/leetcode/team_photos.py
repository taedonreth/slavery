"""
You are given two arrays of integers, `heights1` and `heights2`, representing the heights of players from two different teams.

You need to determine if it is possible to arrange both teams for a group photograph under the following conditions:

1. One entire team must stand **in front** of the other.
2. Every player in the front row must be **strictly shorter** than the player standing directly behind them.
3. Players **can be rearranged** freely within their own team.
4. The team with **fewer players must stand in the front**.
   - If both teams have the same number of players, **either team** can stand in the front.

Return `True` if such an arrangement is possible, and `False` otherwise.

---

Example 1:

Input: heights1 = [5, 8, 1, 3, 4], heights2 = [6, 9, 2, 7, 10]
Output: True
Explanation:
We can arrange team1 as [1, 3, 4, 5, 8] and team2 as [2, 6, 7, 9, 10].
Team1 stands in front, and every player in team1 is shorter than the player directly behind in team2.

---

Example 2:

Input: heights1 = [5, 4, 7], heights2 = [3, 6, 9]
Output: False
Explanation:
Team1 cannot all be shorter or all be taller than team2 after sorting.

---

Example 3:

Input: heights1 = [4, 5, 7], heights2 = [5, 6, 8]
Output: True
Explanation:
Both teams have equal size.
If team1 stands in front → [4, 5, 7] vs [5, 6, 8] → valid (strictly increasing).

---

Constraints:

- 1 <= len(heights1), len(heights2) <= 10⁴
- 1 <= heights1[i], heights2[i] <= 10⁹
"""

from typing import List


class Solution:
    def canTakePhoto(self, heights1: List[int], heights2: List[int]) -> bool:
        """
        Determine if two teams can be arranged for a photo with height constraints.
        
        Key Insight:
        - If we can arrange them, the optimal strategy is to sort both teams
        - Match shortest with shortest, 2nd shortest with 2nd shortest, etc.
        - This greedy approach gives the best chance of satisfaction
        
        Strategy:
        1. Sort both arrays
        2. Determine which team should be in front:
           - If different sizes: smaller team must be in front
           - If same size: try both configurations
        3. Check if all front players < corresponding back players
        
        Why sorting works:
        - If sorted[i] >= sorted[j] for any pairing, no rearrangement will help
        - Sorting gives the best "cushion" for each comparison
        
        Time: O(n log n + m log m) for sorting
        Space: O(n + m) for sorted arrays
        """
        # Sort both teams
        h1_sorted = sorted(heights1)
        h2_sorted = sorted(heights2)
        
        def can_arrange(front: List[int], back: List[int]) -> bool:
            """Check if front team can all be strictly shorter than back team.
            
            Uses two-pointer approach to optimally match front players with back players.
            Since back may have more players, we can skip some back players.
            
            Precondition: len(front) <= len(back) (guaranteed by caller)
            """
            i = 0  # Pointer for front team
            j = 0  # Pointer for back team
            
            # Try to match each person in front with someone in back
            while i < len(front) and j < len(back):
                if front[i] < back[j]:
                    # Found a valid match for front[i]
                    i += 1
                    j += 1
                else:
                    # front[i] >= back[j], try next person in back
                    j += 1
            
            # Check if we matched all front players
            return i == len(front)
        
        # Apply the size rule
        if len(h1_sorted) < len(h2_sorted):
            # Team 1 must be in front
            return can_arrange(h1_sorted, h2_sorted)
        elif len(h2_sorted) < len(h1_sorted):
            # Team 2 must be in front
            return can_arrange(h2_sorted, h1_sorted)
        else:
            # Equal size: either team can be in front, try both
            return can_arrange(h1_sorted, h2_sorted) or can_arrange(h2_sorted, h1_sorted)


if __name__ == "__main__":
    sol = Solution()

    # Example 1
    heights1 = [5, 8, 1, 3, 4]
    heights2 = [6, 9, 2, 7, 10]
    assert sol.canTakePhoto(heights1, heights2)

    # Example 2
    heights1 = [5, 4, 7]
    heights2 = [3, 6, 9]
    assert not sol.canTakePhoto(heights1, heights2)

    # Example 3
    heights1 = [4, 5, 7]
    heights2 = [5, 6, 8]
    assert sol.canTakePhoto(heights1, heights2)

    # Example 4: unequal lengths
    heights1 = [3, 4, 5]
    heights2 = [6, 7, 8, 9]
    assert sol.canTakePhoto(heights1, heights2)

    # Example 5: equal size but no valid arrangement
    heights1 = [6, 7, 8]
    heights2 = [5, 6, 9]
    assert not sol.canTakePhoto(heights1, heights2)

    heights1 = [2, 3, 4]
    heights2 = [1, 3, 4, 5]
    assert sol.canTakePhoto(heights1, heights2)

    print("✅ All test cases passed!")
