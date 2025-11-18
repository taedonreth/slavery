# leetcode 1268: search suggestion system (medium)

"""
You are given an array of strings products and a string searchWord.

Design a system that suggests at most three product names from products after each character of searchWord is typed. Suggested products should have common prefix with searchWord.
If there are more than three products with a common prefix return the three lexicographically minimums products.

Return a list of lists of the suggested products after each character of searchWord is typed.

Example 1:
    Input: products = ["mobile","mouse","moneypot","monitor","mousepad"], searchWord = "mouse"
    Output: [["mobile","moneypot","monitor"],["mobile","moneypot","monitor"],["mouse","mousepad"],["mouse","mousepad"],["mouse","mousepad"]]
    Explanation: products sorted lexicographically = ["mobile","moneypot","monitor","mouse","mousepad"].
    After typing m and mo all products match and we show user ["mobile","moneypot","monitor"].
    After typing mou, mous and mouse the system suggests ["mouse","mousepad"].

Example 2:
    Input: products = ["havana"], searchWord = "havana"
    Output: [["havana"],["havana"],["havana"],["havana"],["havana"],["havana"]]
    Explanation: The only word "havana" will be always suggested while typing the search word.

Constraints:
    1 <= products.length <= 1000
    1 <= products[i].length <= 3000
    1 <= sum(products[i].length) <= 2 * 104
    All the strings of products are unique.
    products[i] consists of lowercase English letters.
    1 <= searchWord.length <= 1000
    searchWord consists of lowercase English letters.
"""

from typing import List


class Solution:
    def suggestedProducts(
        self, products: List[str], searchWord: str
    ) -> List[List[str]]:
        """
        sort products
        binary search helper to find leftmost index where current word could fit
        res list

        for each letter for searchWord
            initialize similar list
            find leftmost index

            loop through left most index -> at most 3 words away or end of list
                if prefix is prefix of current word
                    add it to similar list
                else
                    no other word after is similar too
                    break

            add similar list to res list
        """

        def _binary_search(arr: List[str], prefix: str) -> int:
            left = 0
            right = len(arr)
            res = -1

            while left <= right:
                mid = (left + right) // 2

                if arr[mid] >= prefix:
                    res = mid
                    right = mid - 1
                else:
                    left = mid + 1

            return res

        res = []
        prefix = ""
        products.sort()

        for char in searchWord:
            prefix += char
            start = _binary_search(products, prefix)
            similar_words = []

            for i in range(start, min(start + 3, len(products))):
                if products[i].startswith(prefix):
                    similar_words.append(products[i])
                else:
                    break

            res.append(similar_words)

        return res


if __name__ == "__main__":
    sol = Solution()

    # Example 1
    products1 = ["mobile", "mouse", "moneypot", "monitor", "mousepad"]
    searchWord1 = "mouse"
    expected1 = [
        ["mobile", "moneypot", "monitor"],
        ["mobile", "moneypot", "monitor"],
        ["mouse", "mousepad"],
        ["mouse", "mousepad"],
        ["mouse", "mousepad"],
    ]
    assert sol.suggestedProducts(products1, searchWord1) == expected1

    # Example 2
    products2 = ["havana"]
    searchWord2 = "havana"
    expected2 = [["havana"], ["havana"], ["havana"], ["havana"], ["havana"], ["havana"]]
    assert sol.suggestedProducts(products2, searchWord2) == expected2

    # No matches after first few letters
    products3 = ["bags", "baggage", "banner", "box", "cloths"]
    searchWord3 = "bags"
    expected3 = [
        ["baggage", "bags", "banner"],  # prefix "b"
        ["baggage", "bags", "banner"],  # prefix "ba"
        ["baggage", "bags"],  # prefix "bag"
        ["bags"],  # prefix "bags"
    ]
    assert sol.suggestedProducts(products3, searchWord3) == expected3

    # All items share prefix, but limit to 3 lexicographically smallest
    products4 = ["apple", "app", "applet", "application", "apply", "apt"]
    searchWord4 = "app"
    expected4 = [
        ["app", "apple", "applet"],  # "a"
        ["app", "apple", "applet"],  # "ap"
        ["app", "apple", "applet"],  # "app"
    ]
    assert sol.suggestedProducts(products4, searchWord4) == expected4

    # Search word not found at all
    products5 = ["dog", "deer", "deal"]
    searchWord5 = "cat"
    expected5 = [[], [], []]
    assert sol.suggestedProducts(products5, searchWord5) == expected5

    # Mixed overlap — only some prefixes match
    products6 = ["car", "cart", "carbon", "care", "dog", "door"]
    searchWord6 = "carp"
    expected6 = [
        ["car", "carbon", "care"],  # "c"
        ["car", "carbon", "care"],  # "ca"
        ["car", "carbon", "care"],  # "car"
        [],  # "carp"
    ]
    assert sol.suggestedProducts(products6, searchWord6) == expected6

    # Search longer than any product
    products7 = ["to", "tea", "ten"]
    searchWord7 = "teach"
    expected7 = [
        ["tea", "ten", "to"],  # "t"
        ["tea", "ten"],  # "te"
        ["tea"],  # "tea"
        [],  # "teac"
        [],  # "teach"
    ]
    assert sol.suggestedProducts(products7, searchWord7) == expected7

    # Case with overlapping start but no exact continuation
    products8 = ["mouse", "monitor", "moon", "mop"]
    searchWord8 = "moose"
    expected8 = [
        ["monitor", "moon", "mop"],  # "m"
        ["monitor", "moon", "mop"],  # "mo"
        ["moon"],  # "moo"
        [],  # "moos"
        [],  # "moose"
    ]
    assert sol.suggestedProducts(products8, searchWord8) == expected8

    print("✅ All test cases passed!")
