# leetcode 438: find all anagrams in a string
from collections import Counter
from typing import List


class Solution:
    # Given two strings s and p, return an array of all the start indices of p's anagrams in s. You may return the answer in any order.
    def findAnagrams(self, s: str, p: str) -> List[int]:
        """
        brute force:
            helper function to check if a given string is an anagram of another given string
                create a Counter for p
                if Counter for substring matches, then return True
                else return false
            loop through s and call this function on each one
                use sliding window (right and left pointer the length of p)
                when there are no more substrings len(p), finished
            if true, add index to res
            return res

        optimization:
            create Counter for p once
            use a sliding window
                have a COunter for sliding window
                start with the first len(p) characters
                compare counters
                add the right letter, take the right one away for next iteration
                if they match starting at any index, add it to res
        """

        p_map = Counter(p)

        left = 0
        right = len(p) - 1
        curr_map = Counter(s[left : right + 1])
        res = []

        while right < len(s):

            if curr_map == p_map:
                res.append(left)

            # next iteration duties
            curr_map[s[left]] -= 1  # remove left
            if curr_map[s[left]] == 0:
                del curr_map[s[left]]
            left += 1  # increment left

            right += 1  # increment right
            if right < len(s):
                curr_map[s[right]] += 1  # add right

        return res


def main():
    sol = Solution()

    # Example 1
    assert sol.findAnagrams("cbaebabacd", "abc") == [0, 6]

    # Example 2
    assert sol.findAnagrams("abab", "ab") == [0, 1, 2]

    # Edge cases
    assert sol.findAnagrams("", "a") == []  # empty string
    assert sol.findAnagrams("a", "a") == [0]  # single char match
    assert sol.findAnagrams("a", "b") == []  # single char no match
    assert sol.findAnagrams("aaaaa", "aa") == [0, 1, 2, 3]  # overlapping anagrams
    assert sol.findAnagrams("abc", "abcd") == []  # p longer than s

    print("All test cases passed!")


if __name__ == "__main__":
    main()
