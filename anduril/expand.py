"""
You are given a string `expression` representing a brace expansion.

The expression may contain:
- **Letters (a–z)** representing characters.
- **Braces `{}`** enclosing comma-separated groups.
- **Concatenations** of such groups and/or letters.

Your task is to return **all possible strings** that can be formed by expanding the expression,
**in lexicographically sorted order**.

---

### Rules:

1. Every `{a,b}` means **choose one** of `a` or `b`.
2. Adjacent groups or letters represent **concatenation**.
3. Braces may be **nested**, but for this version, assume braces do **not** nest inside each other.

---

### Example 1:

Input: expression = "{a,b}{c,d}.txt"  
Output: ["ac.txt", "ad.txt", "bc.txt", "bd.txt"]

Explanation:  
Possible expansions are:
- Pick 'a' from first group, 'c' from second → "ac.txt"
- Pick 'a' from first group, 'd' from second → "ad.txt"
- Pick 'b' from first group, 'c' from second → "bc.txt"
- Pick 'b' from first group, 'd' from second → "bd.txt"

---

### Example 2:

Input: expression = "{x,y}z"  
Output: ["xz", "yz"]

---

### Example 3:

Input: expression = "pre{a,b,c}post"  
Output: ["preapost", "prebpost", "precpost"]

---

### Example 4:

Input: expression = "{a,b}{x,y}{1,2}"  
Output: ["ax1", "ax2", "ay1", "ay2", "bx1", "bx2", "by1", "by2"]

---

### Constraints:

- 1 <= len(expression) <= 100
- The expression only contains lowercase letters, `{`, `}`, `,`, and `.`.
- The braces are well-formed (no mismatched `{` or `}`).

---

Follow-up:  
Can you solve this problem if braces can be **nested arbitrarily deep**, e.g., `{a,{b,c}}d`?
"""

from typing import List


class Solution:
    def expand(self, expression: str) -> List[str]:
        """
        Expand brace expressions and return all possible strings in sorted order.
        
        Strategy:
        1. Parse expression into "choice groups"
           - Regular chars are groups with 1 option
           - {a,b,c} are groups with multiple options
        2. Generate cartesian product of all groups manually using recursion
        3. Sort results lexicographically
        
        Time: O(n + k log k) where n = len(expression), k = number of results
        Space: O(k) for storing all results
        """
        # Parse expression into groups
        groups = []
        i = 0
        n = len(expression)
        
        while i < n:
            if expression[i] == '{':
                # Found a brace group, extract all options
                j = i + 1
                # Find the matching closing brace
                while j < n and expression[j] != '}':
                    j += 1
                
                # Extract content between braces: "a,b,c"
                content = expression[i+1:j]
                # Split by comma to get individual options
                options = content.split(',')
                groups.append(options)
                
                i = j + 1  # Move past the closing brace
            else:
                # Regular character, treat as single-option group
                groups.append([expression[i]])
                i += 1
        
        # Generate all combinations manually using backtracking
        results = []
        
        def backtrack(group_idx: int, current: str):
            """
            Build combinations by choosing one option from each group.
            
            group_idx: current group we're choosing from
            current: string built so far
            """
            # Base case: we've chosen from all groups
            if group_idx == len(groups):
                results.append(current)
                return
            
            # Try each option in the current group
            for option in groups[group_idx]:
                backtrack(group_idx + 1, current + option)
        
        # Start backtracking from group 0 with empty string
        backtrack(0, "")
        
        # Sort lexicographically
        results.sort()
        
        return results


if __name__ == "__main__":
    sol = Solution()

    # Example 1
    assert sol.expand("{a,b}{c,d}.txt") == ["ac.txt", "ad.txt", "bc.txt", "bd.txt"]

    # Example 2
    assert sol.expand("{x,y}z") == ["xz", "yz"]

    # Example 3
    assert sol.expand("pre{a,b,c}post") == ["preapost", "prebpost", "precpost"]

    # Example 4
    assert sol.expand("{a,b}{x,y}{1,2}") == ["ax1", "ax2", "ay1", "ay2", "bx1", "bx2", "by1", "by2"]

    print("✅ All test cases passed!")
