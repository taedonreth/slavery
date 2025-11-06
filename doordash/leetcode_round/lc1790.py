# leetcode 1790: check if one string swap can make strings equal (easy)

"""
You are given two strings s1 and s2 of equal length. A string swap is an operation where you choose two indices in a string (not necessarily different) and swap the characters at these indices.

Return true if it is possible to make both strings equal by performing at most one string swap on exactly one of the strings. Otherwise, return false.
"""

from collections import Counter


class Solution:
    def areAlmostEqual(self, s1: str, s2: str) -> bool:
        """
        Input: s1 = "bank", s2 = "kanb"
        Output: true
        Explanation: For example, swap the first character with the last character of s2 to make "bank".

        counters are the same and they differ in exactly 2 places?
        """
        if s1 == s2:
            return True

        count1 = Counter(s1)
        count2 = Counter(s2)

        diff = 0
        for i in range(len(s1)):
            if s1[i] != s2[i]:
                diff += 1

        return count1 == count2 and diff == 2
