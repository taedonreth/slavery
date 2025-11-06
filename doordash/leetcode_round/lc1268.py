# leetcode 1268: search suggestion system (medium)

"""
You are given an array of strings products and a string searchWord.

Design a system that suggests at most three product names from products after each character of searchWord is typed. Suggested products should have common prefix with searchWord. If there are more than three products with a common prefix return the three lexicographically minimums products.

Return a list of lists of the suggested products after each character of searchWord is typed.
"""

from typing import List


class Solution:
    def suggestedProducts(
        self, products: List[str], searchWord: str
    ) -> List[List[str]]:
        """
        Input: products = ["mobile","mouse","moneypot","monitor","mousepad"], searchWord = "mouse"
        Output: [["mobile","moneypot","monitor"],["mobile","moneypot","monitor"],["mouse","mousepad"],["mouse","mousepad"],["mouse","mousepad"]]
        """

        def binary_search_prefix(arr, prefix):
            """Find the leftmost index where prefix could be inserted to maintain sorted order"""
            left, right = 0, len(arr)

            while left < right:
                mid = (left + right) // 2
                if arr[mid] < prefix:
                    left = mid + 1
                else:
                    right = mid

            return left

        products.sort()
        res = []
        prefix = ""

        for char in searchWord:
            prefix += char
            # Find starting position using binary search
            start = binary_search_prefix(products, prefix)

            # Collect up to 3 suggestions
            suggestions = []
            for i in range(start, min(start + 3, len(products))):
                if products[i].startswith(prefix):
                    suggestions.append(products[i])
                else:
                    break

            res.append(suggestions)

        return res


if __name__ == "__main__":
    sol = Solution()
    input = ["mobile", "mouse", "moneypot", "monitor", "mousepad"]
    print(sol.suggestedProducts(input, "mouse"))
