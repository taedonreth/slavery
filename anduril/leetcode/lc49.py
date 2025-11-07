# leetcode 49: group anagrams (medium)

"""
Given an array of strings strs, group the anagrams together. You can return the answer in any order.

Example 1:
    Input: strs = ["eat","tea","tan","ate","nat","bat"]
    Output: [["bat"],["nat","tan"],["ate","eat","tea"]]

    {"bat": ["bat"], "nat": ["nat", "tan"], "ate": ["ate", "eat", "tea"]}
    Explanation:
        There is no string in strs that can be rearranged to form "bat".
        The strings "nat" and "tan" are anagrams as they can be rearranged to form each other.
        The strings "ate", "eat", and "tea" are anagrams as they can be rearranged to form each other.

Example 2:
    Input: strs = [""]
    Output: [[""]]

Example 3:
    Input: strs = ["a"]
    Output: [["a"]]

Constraints:
    1 <= strs.length <= 104
    0 <= strs[i].length <= 100
    strs[i] consists of lowercase English letters.
"""
from collections import Counter, defaultdict
from typing import List


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        """
        go through strs
            add into dictionary based on anagram
            dict structure: {word: [list of anagrams]}
            how do i check which list a word goes in
                if they have the same anagram
                    how do i know if they are anagrams
                        if their counters are the same
                        counter
        """
        anagrams = defaultdict(list[str])

        for word in strs:
            sorted_word = "".join(sorted(word))
            anagrams[sorted_word].append(word)

        return list(anagrams.values())


if __name__ == "__main__":
    sol = Solution()

    def sort_groups(groups: List[List[str]]) -> List[List[str]]:
        """
        Helper to compare unordered groups regardless of element order.
        Sorts inner lists and outer list so assert works.
        """
        return sorted([sorted(g) for g in groups])

    # Example 1
    strs1 = ["eat", "tea", "tan", "ate", "nat", "bat"]
    expected1 = [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]
    print(sol.groupAnagrams(strs1))
    assert sort_groups(sol.groupAnagrams(strs1)) == sort_groups(expected1)

    # Example 2
    strs2 = [""]
    expected2 = [[""]]
    assert sort_groups(sol.groupAnagrams(strs2)) == sort_groups(expected2)

    # Example 3
    strs3 = ["a"]
    expected3 = [["a"]]
    assert sort_groups(sol.groupAnagrams(strs3)) == sort_groups(expected3)

    # All unique words (no anagrams)
    strs4 = ["abc", "def", "ghi"]
    expected4 = [["abc"], ["def"], ["ghi"]]
    assert sort_groups(sol.groupAnagrams(strs4)) == sort_groups(expected4)

    # All identical words
    strs5 = ["bob", "bob", "bob"]
    expected5 = [["bob", "bob", "bob"]]
    assert sort_groups(sol.groupAnagrams(strs5)) == sort_groups(expected5)

    # Mixed length and overlap
    strs6 = ["listen", "silent", "enlist", "inlets", "google", "gooegl"]
    expected6 = [["listen", "silent", "enlist", "inlets"], ["google", "gooegl"]]
    assert sort_groups(sol.groupAnagrams(strs6)) == sort_groups(expected6)

    # Anagrams differing by single letter
    strs7 = ["abc", "acb", "bac", "bca", "cab", "cba", "abcd", "bcda"]
    expected7 = [["abc", "acb", "bac", "bca", "cab", "cba"], ["abcd", "bcda"]]
    assert sort_groups(sol.groupAnagrams(strs7)) == sort_groups(expected7)

    # Case with some empty and single-letter
    strs8 = ["", "a", "b", "ab", "ba"]
    expected8 = [[""], ["a"], ["b"], ["ab", "ba"]]
    assert sort_groups(sol.groupAnagrams(strs8)) == sort_groups(expected8)

    print("✅ All test cases passed!")
