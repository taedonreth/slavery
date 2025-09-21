# leetcode 269: alien dictionary (hard)

from collections import defaultdict
from typing import List


class Solution:
    def alienOrder(self, words: List[str]) -> str:

        # data structures to hold information
        unique_chars = set()
        adj_list = defaultdict(list)

        for word in words:
            for c in word:
                unique_chars.add(c)

        # gather precendence information + build adjacency list: if a comes before b, a -> b (b is in a's list)
        for i in range(len(words) - 1):
            first_word = words[i]
            second_word = words[i + 1]

            diff_found = False
            min_len = min(len(first_word), len(second_word))
            for j in range(min_len):
                if first_word[j] != second_word[j]:
                    adj_list[first_word[j]].append(second_word[j])
                    diff_found = True
                    break

            if not diff_found and len(first_word) > len(second_word):
                return ""

        # dfs with cycle detection, add to stack in post order for top sort
        stack = []
        colors = {}  # 0 = not seen, 1 = processing, 2 = finished

        def dfs(node):
            # traverse adjacency list
            # if not seen, move to processing and traverse its children
            # if we see a node in processing, return False (backedge)
            if node in colors:
                if colors[node] == 1:
                    return False
                elif colors[node] == 2:
                    return True

            colors[node] = 1
            for neighbor in adj_list[node]:
                if not dfs(neighbor):
                    return False

            colors[node] = 2

            # if all checks pass, add to stack and return true
            stack.append(node)
            return True

        # for each character, call dfs to get its relative order
        # return early if there are conflicting orderings
        for c in unique_chars:
            if c not in colors and not dfs(c):
                return ""

        # reverse stack to get top order, join to get result
        stack.reverse()
        return "".join(stack)


def main():
    solution = Solution()

    # Example 1
    words1 = ["wrt", "wrf", "er", "ett", "rftt"]
    result1 = solution.alienOrder(words1)
    assert result1 == "wertf", f"Expected 'wertf', got '{result1}'"

    # Example 2
    words2 = ["z", "x"]
    result2 = solution.alienOrder(words2)
    assert result2 == "zx", f"Expected 'zx', got '{result2}'"

    # Example 3 - Invalid case
    words3 = ["z", "x", "z"]
    result3 = solution.alienOrder(words3)
    assert result3 == "", f"Expected '', got '{result3}'"

    # Additional test case - Invalid prefix case
    words4 = ["abc", "ab"]
    result4 = solution.alienOrder(words4)
    assert result4 == "", f"Expected '', got '{result4}'"

    # Test case with multiple valid orderings
    words5 = ["ac", "ab", "zc", "zb"]
    result5 = solution.alienOrder(words5)
    # Multiple valid answers possible, just check it's not empty and has right chars
    assert result5 != "", f"Expected non-empty result, got '{result5}'"
    assert set(result5) == {
        "a",
        "c",
        "b",
        "z",
    }, f"Expected chars a,c,b,z, got '{result5}'"

    print("All tests passed!")


if __name__ == "__main__":
    main()
