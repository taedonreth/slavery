# leetcode 527: word abbreviation (hard)

from typing import List
from collections import defaultdict

class Solution:
    def wordsAbbreviation(self, words: List[str]) -> List[str]:
        """
        Input: words = ["like","god","internal","me","internet","interval","intension","face","intrusion"]
        Output: ["l2e","god","internal","me","i6t","interval","inte4n","f2e","intr4n"]

        trick: words can only have same abbreviations if they have the same length and first + last letters
        helper function to find longest common prefix between two words
        group words in map: (length, first letter, last letter): (word, index)

        iterate through enumerated map:
            sort values
            find longest common prefix between the grouped words

            check if words can be abbreviated (if abbreviation made the word shorter)

        return ans
        """

        def longest_common_prefix(word1: str, word2: str) -> int:
            i = 0
            while i < len(word1) and i < len(word2) and word1[i] == word2[i]:
                i += 1
            return i

        res = [""] * len(words)

        groups = defaultdict(list)
        for idx, word in enumerate(words):
            groups[len(word), word[0], word[-1]].append((word, idx))

        # iterate through groups - (length, first letter, last letter): (word, index)
        for (size, first, last), similar_words in groups.items():
            similar_words.sort()
            lcp = [0] * len(similar_words)
            # iterate through similar words - [("internal", 0), ("internet", 1), ("interval", 2)]
            for i, (word, _) in enumerate(similar_words):
                # compare a word with previous, so we need to skip the first index
                if i > 0:
                    lcp[i] = longest_common_prefix(word, similar_words[i-1][0])
                    lcp[i-1] = max(lcp[i-1], lcp[i])

                # check if words should be abbreviated - (("internal",0), 6), (("internet",1), 6), (("interval",2), 5)
                for (word, index), p in zip(similar_words, lcp):
                    diff = size - 2 - p
                    if diff <= 1:
                        res[index] = word
                    else:
                        res[index] = word[:p + 1] + str(diff) + last

        return res