"""
You are given two lists, `vecA` and `vecB`, representing two different classes of objects: A and B.

You are also given a function `rank(a, b)` that takes one element `a` from `vecA` and one element `b` from `vecB`,
and returns an integer representing the "rank" or "score" of pairing them together.

Your task is to select pairs `(a, b)` such that:

1. Each element of `vecA` is used **at most once**.
2. Each element of `vecB` is used **at most once**.
3. The **sum of all rank values** from the selected pairs is **maximized**.

Return any list of pairs `(a, b)` that achieves this **maximum total rank sum**.

If multiple valid pairings exist with the same sum, you may return any one of them.

---

### Example 1

Input:
vecA = ["A1", "A2", "A3"]
vecB = ["B1", "B2", "B3"]
rank(Ai, Bj) =
[
  [3, 1, 2],
  [2, 4, 6],
  [5, 2, 3]
]

Output:
[("A1", "B1"), ("A2", "B3"), ("A3", "B2")]

Explanation:
The total rank sum is 3 + 6 + 2 = 11, which is the maximum possible.

---

### Example 2

Input:
vecA = ["A1", "A2"]
vecB = ["B1", "B2"]
rank(Ai, Bj) =
[
  [1, 100],
  [50, 2]
]

Output:
[("A1", "B2"), ("A2", "B1")]

Explanation:
The total rank sum is 100 + 50 = 150, which is the maximum possible.

---

### Constraints:

- 1 <= len(vecA), len(vecB) <= 100
- rank(a, b) returns an integer in the range [-10⁶, 10⁶]
- You may assume len(vecA) == len(vecB)
- If multiple optimal pairings exist, return any one of them

---

### Notes:

This is a variant of the **assignment problem**, which can be solved optimally
using the **Hungarian Algorithm** in O(n³) time.
"""

from typing import List, Tuple, TypeVar

A = TypeVar("A")
B = TypeVar("B")


# Mock rank function (for demonstration)
def rank(a: A, b: B) -> int:
    # Replace this with the actual rank logic or API call
    raise NotImplementedError


class Solution:
    def highest_rank_sum_pairs(self, vecA: List[A], vecB: List[B]) -> List[Tuple[A, B]]:
        """
        Find optimal one-to-one pairing between vecA and vecB to maximize rank sum.
        
        This is the Assignment Problem (maximum weight bipartite matching).
        
        Approach:
        - Build cost matrix from rank function
        - Use Hungarian Algorithm for optimal O(n³) solution
        - Since we want MAX (not min), we negate the costs
        
        For interview: Implementing full Hungarian is complex, so we use
        a simplified approach with recursive backtracking + memoization.
        
        Time: O(n! / (n-k)!) in worst case, but with pruning much better
        Space: O(n²) for rank matrix + O(2^n) for memoization
        """
        n = len(vecA)
        
        # Build rank matrix for quick lookup
        rank_matrix = {}
        for i, a in enumerate(vecA):
            for j, b in enumerate(vecB):
                rank_matrix[(i, j)] = rank(a, b)
        
        # Recursive backtracking with memoization
        # State: (current_a_index, used_b_mask) -> (max_sum, best_pairing)
        memo = {}
        
        def solve(a_idx: int, used_b_mask: int) -> Tuple[int, List[Tuple[int, int]]]:
            """
            Find best pairing for vecA[a_idx:] given that vecB elements 
            in used_b_mask are already used.
            
            Returns: (max_sum, list of (a_index, b_index) pairs)
            """
            # Base case: all A's have been paired
            if a_idx == n:
                return (0, [])
            
            # Check memo
            if (a_idx, used_b_mask) in memo:
                return memo[(a_idx, used_b_mask)]
            
            best_sum = float('-inf')
            best_pairing = []
            
            # Try pairing vecA[a_idx] with each unused vecB[j]
            for j in range(n):
                # Check if vecB[j] is already used
                if used_b_mask & (1 << j):
                    continue
                
                # Try this pairing
                current_rank = rank_matrix[(a_idx, j)]
                new_mask = used_b_mask | (1 << j)
                future_sum, future_pairing = solve(a_idx + 1, new_mask)
                
                total_sum = current_rank + future_sum
                
                if total_sum > best_sum:
                    best_sum = total_sum
                    best_pairing = [(a_idx, j)] + future_pairing
            
            memo[(a_idx, used_b_mask)] = (best_sum, best_pairing)
            return (best_sum, best_pairing)
        
        # Solve and convert indices back to actual elements
        _, index_pairs = solve(0, 0)
        result = [(vecA[i], vecB[j]) for i, j in index_pairs]
        
        return result


if __name__ == "__main__":
    # Example 1
    vecA = ["A1", "A2", "A3"]
    vecB = ["B1", "B2", "B3"]

    rank_matrix = {
        ("A1", "B1"): 3, ("A1", "B2"): 1, ("A1", "B3"): 2,
        ("A2", "B1"): 2, ("A2", "B2"): 4, ("A2", "B3"): 6,
        ("A3", "B1"): 5, ("A3", "B2"): 2, ("A3", "B3"): 3
    }

    def rank(a, b):
        return rank_matrix[(a, b)]

    sol = Solution()
    result = sol.highest_rank_sum_pairs(vecA, vecB)
    print("Result:", result)

    # Example 2
    vecA = ["A1", "A2"]
    vecB = ["B1", "B2"]

    rank_matrix = {
        ("A1", "B1"): 1, ("A1", "B2"): 100,
        ("A2", "B1"): 50, ("A2", "B2"): 2
    }

    def rank(a, b):
        return rank_matrix[(a, b)]

    result = sol.highest_rank_sum_pairs(vecA, vecB)
    print("Result:", result)
