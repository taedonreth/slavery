# leetcode 244: shortest word distance II (medium)

"""
Design a data structure that will be initialized with a string array, and then it should answer queries of the shortest distance between two different strings from the array.

Implement the WordDistance class:
    WordDistance(String[] wordsDict) initializes the object with the strings array wordsDict.
    int shortest(String word1, String word2) returns the shortest distance between word1 and word2 in the array wordsDict.

Example 1:

Input
["WordDistance", "shortest", "shortest"]
[[["practice", "makes", "perfect", "coding", "makes"]], ["coding", "practice"], ["makes", "coding"]]
Output
[null, 3, 1]

Explanation
WordDistance wordDistance = new WordDistance(["practice", "makes", "perfect", "coding", "makes"]);
wordDistance.shortest("coding", "practice"); // return 3
wordDistance.shortest("makes", "coding");    // return 1


Constraints:
    1 <= wordsDict.length <= 3 * 104
    1 <= wordsDict[i].length <= 10
    wordsDict[i] consists of lowercase English letters.
    word1 and word2 are in wordsDict.
    word1 != word2
    At most 5000 calls will be made to shortest.
"""

from collections import defaultdict
from typing import List


class WordDistance:
    """
    on initialization we can keep track of indexes of all occurrences of each word in a map
    {word: [indicies]}

    O(n)
    """

    def __init__(self, wordsDict: List[str]):
        self.word_indicies = defaultdict(list)

        for idx, word in enumerate(wordsDict):
            self.word_indicies[word].append(idx)

    """
    need to make this super efficient if we call it 5000 times and wordsDict is as long as 3 * 104
    utilize map
        get index lists of both words
        word1: [0, 5, 8]
        word2: [1, 2, 30]

        find min distance between any of these
    O(n)
    """

    def shortest(self, word1: str, word2: str) -> int:
        word1_indicies, word2_indicies = (
            self.word_indicies[word1],
            self.word_indicies[word2],
        )
        min_dist = float("inf")

        ptr1, ptr2 = 0, 0
        while ptr1 < len(word1_indicies) and ptr2 < len(word2_indicies):
            curr_dist = abs(word1_indicies[ptr1] - word2_indicies[ptr2])
            min_dist = min(min_dist, curr_dist)

            if word1_indicies[ptr1] >= word2_indicies[ptr2]:
                ptr2 += 1
            else:
                ptr1 += 1

        return min_dist


# Your WordDistance object will be instantiated and called as such:
# obj = WordDistance(wordsDict)
# param_1 = obj.shortest(word1,word2)

if __name__ == "__main__":
    # Example 1
    words = ["practice", "makes", "perfect", "coding", "makes"]
    wd = WordDistance(words)
    assert wd.shortest("coding", "practice") == 3
    assert wd.shortest("makes", "coding") == 1

    # Words appear multiple times, should choose closest pair
    words2 = ["a", "b", "a", "c", "a", "b", "a"]
    wd2 = WordDistance(words2)
    assert wd2.shortest("a", "b") == 1
    assert wd2.shortest("a", "c") == 1
    assert wd2.shortest("b", "c") == 2

    # Words alternate positions
    words3 = ["x", "y", "x", "y", "x", "y"]
    wd3 = WordDistance(words3)
    assert wd3.shortest("x", "y") == 1

    # Words separated by several positions
    words4 = ["alpha", "beta", "gamma", "delta", "epsilon", "zeta"]
    wd4 = WordDistance(words4)
    assert wd4.shortest("alpha", "zeta") == 5
    assert wd4.shortest("beta", "delta") == 2
    assert wd4.shortest("gamma", "epsilon") == 2

    # Only two distinct words repeated many times
    words5 = ["foo", "bar", "foo", "bar", "foo", "bar"]
    wd5 = WordDistance(words5)
    assert wd5.shortest("foo", "bar") == 1

    # Non-adjacent repetitions with gaps
    words6 = ["one", "two", "three", "four", "one", "five", "two", "six"]
    wd6 = WordDistance(words6)
    assert wd6.shortest("one", "two") == 1
    assert wd6.shortest("two", "five") == 1
    assert wd6.shortest("three", "six") == 5

    # Minimal input (2 elements)
    words7 = ["apple", "banana"]
    wd7 = WordDistance(words7)
    assert wd7.shortest("apple", "banana") == 1

    print("✅ All test cases passed!")
