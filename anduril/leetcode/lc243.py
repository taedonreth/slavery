# leetcode 243: shortest word distance (easy)

"""
Given an array of strings wordsDict and two different strings that already exist in the array word1 and word2, return the shortest distance between these two words in the list.

Example 1:

Input: wordsDict = ["practice", "makes", "perfect", "coding", "makes"], word1 = "coding", word2 = "practice"
Output: 3
Example 2:

Input: wordsDict = ["practice", "makes", "perfect", "coding", "makes"], word1 = "makes", word2 = "coding"
Output: 1


Constraints:
    2 <= wordsDict.length <= 3 * 104
    1 <= wordsDict[i].length <= 10
    wordsDict[i] consists of lowercase English letters.
    word1 and word2 are in wordsDict.
    word1 != word2
"""

from typing import List


class Solution:
    def shortestDistance(self, wordsDict: List[str], word1: str, word2: str) -> int:
        """
        find index of word 1 and index of word 2 and subtract them?
            go through arr one time and have a pointer for when u run into each word
        """

        word1_ptr = float("inf")
        word2_ptr = float("inf")
        shortest_dist = float("inf")

        for i in range(len(wordsDict)):
            if wordsDict[i] == word1 or wordsDict[i] == word2:
                if wordsDict[i] == word1:
                    word1_ptr = i
                elif wordsDict[i] == word2:
                    word2_ptr = i

                shortest_dist = min(shortest_dist, abs(word2_ptr - word1_ptr))

        return shortest_dist


if __name__ == "__main__":
    sol = Solution()

    # Example 1
    words1 = ["practice", "makes", "perfect", "coding", "makes"]
    assert sol.shortestDistance(words1, "coding", "practice") == 3

    # Example 2
    words2 = ["practice", "makes", "perfect", "coding", "makes"]
    assert sol.shortestDistance(words2, "makes", "coding") == 1

    # Adjacent words
    words3 = ["a", "b", "c", "d"]
    assert sol.shortestDistance(words3, "b", "c") == 1

    # Words appear multiple times
    words4 = ["a", "b", "x", "b", "x", "a"]
    assert sol.shortestDistance(words4, "a", "b") == 1

    # Words separated by multiple same words
    words5 = ["x", "y", "z", "x", "y", "z", "x"]
    assert sol.shortestDistance(words5, "x", "z") == 1

    # Words at start and end
    words6 = ["a", "x", "y", "z", "b"]
    assert sol.shortestDistance(words6, "a", "b") == 4

    # Larger input, words repeated
    words7 = ["word"] * 10000 + ["target1"] + ["word"] * 2000 + ["target2"]
    assert sol.shortestDistance(words7, "target1", "target2") == 2001

    print("✅ All test cases passed!")
