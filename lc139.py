# leetcode 139: word break (medium)
from typing import List


class Solution:
    """
    Given a string s and a dictionary of strings wordDict, return true if s can be segmented into a space-separated sequence of one or more dictionary words.
    Note that the same word in the dictionary may be reused multiple times in the segmentation.
    """

    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        """
        dp:
        create dp array of length len(s) + 1, initialized to False
        set dp[0] = True   # empty string is segmentable

        for each index i from 1 to len(s):
            for each j from 0 to i:
                if dp[j] is True and s[j:i] is in dict:
                    dp[i] = True
                    break   # no need to check further splits once dp[i] is True

        if dp[len(s)] is True:
            return True
        else:
            return False
        """
        dp = [False] * (len(s) + 1)
        dp[0] = True

        for i in range(1, len(s) + 1):
            for j in range(0, i):
                if dp[j] and s[j:i] in wordDict:
                    dp[i] = True
                    break

        if dp[len(s)]:
            return True
        else:
            return False


def main():
    sol = Solution()

    assert sol.wordBreak("leetcode", ["leet", "code"]) == True
    assert sol.wordBreak("applepenapple", ["apple", "pen"]) == True
    assert sol.wordBreak("catsandog", ["cats", "dog", "sand", "and", "cat"]) == False

    print("All test cases passed!")


if __name__ == "__main__":
    main()
