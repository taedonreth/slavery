from collections import Counter
from typing import List

"""
You are given an array of strings words. Each element of words consists of two lowercase English letters.
Create the longest possible palindrome by selecting some elements from words and concatenating them in any order. Each element can be selected at most once.
Return the length of the longest palindrome that you can create. If it is impossible to create any palindrome, return 0.
A palindrome is a string that reads the same forward and backward.
"""


class Solution:
    def longestPalindrome(self, words: List[str]) -> int:
        # brute force:
        # try all combinations of the strings in words
        # sift out non-palindromes
        # get longest palindrome from whats left
        # faster?
        """
        Count all words
        Use Counter to track how many times each word appears.
        This is necessary because words can appear multiple times and you can use each at most once.
        Iterate over all unique words
        For each word, consider two cases:

        Case 1: Word is self-palindromic
        Example: "gg", "cc", "ll"
        These read the same forwards and backwards.
        Strategy:
        Take pairs of these words and put one at the start and one at the end of the palindrome.
        Each pair contributes 4 characters (2 + 2).
        If there’s one leftover word, you can put it in the middle of the palindrome.
        Only one self-palindrome can sit in the center, so we use a center flag.

        Case 2: Word is not self-palindromic
        Example: "ab"
        Look for its reverse in the counter ("ba").
        Strategy:
        Take as many pairs of word + reverse as possible.
        Each pair contributes 4 characters (2 + 2).
        After using a pair, decrement the counts for both words in the counter to avoid reuse.

        Finalize the palindrome length
        After processing all words:
        If a center word was found (one leftover self-palindrome), add 2 characters to length.
        """

        counter = Counter(words)
        max_len = 0
        center = False

        for word, count in counter.items():
            reverse = word[::-1]

            if word == reverse:
                max_len += (count // 2) * 4
                if count % 2:
                    center = True
            elif reverse in counter:
                pairs = min(count, counter[reverse])
                max_len += pairs * 4
                counter[word] -= pairs
                counter[reverse] -= pairs

        if center:
            max_len += 2

        return max_len


def main():
    sol = Solution()

    # Example 1
    words1 = ["lc", "cl", "gg"]
    print("Input:", words1)
    print("Output:", sol.longestPalindrome(words1))  # Expected 6

    # Example 2
    words2 = ["ab", "ty", "yt", "lc", "cl", "ab"]
    print("Input:", words2)
    print("Output:", sol.longestPalindrome(words2))  # Expected 8

    # Example 3
    words3 = ["cc", "ll", "xx"]
    print("Input:", words3)
    print("Output:", sol.longestPalindrome(words3))  # Expected 2


if __name__ == "__main__":
    main()

"""
Example 1:

Input: words = ["lc","cl","gg"]
Output: 6
Explanation: One longest palindrome is "lc" + "gg" + "cl" = "lcggcl", of length 6.
Note that "clgglc" is another longest palindrome that can be created.
Example 2:

Input: words = ["ab","ty","yt","lc","cl","ab"]
Output: 8
Explanation: One longest palindrome is "ty" + "lc" + "cl" + "yt" = "tylcclyt", of length 8.
Note that "lcyttycl" is another longest palindrome that can be created.
Example 3:

Input: words = ["cc","ll","xx"]
Output: 2
Explanation: One longest palindrome is "cc", of length 2.
Note that "ll" is another longest palindrome that can be created, and so is "xx".
"""
