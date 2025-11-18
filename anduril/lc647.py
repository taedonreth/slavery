# leetcode 647: palindromic substrings (medium)

"""
Given a string s, return the number of palindromic substrings in it.

A string is a palindrome when it reads the same backward as forward.

A substring is a contiguous sequence of characters within the string.

 

Example 1:

Input: s = "abc"
Output: 3
Explanation: Three palindromic strings: "a", "b", "c".
Example 2:

Input: s = "aaa"
Output: 6
Explanation: Six palindromic strings: "a", "a", "a", "aa", "aa", "aaa".
 

Constraints:

1 <= s.length <= 1000
s consists of lowercase English letters.
"""

class Solution:
    def countSubstrings(self, s: str) -> int:
        res = 0
        for i in range(len(s)):
            res += self.expand(s, i, i)
            res += self.expand(s, i, i + 1)

        return res

    def expand(self, s: str, left: int, right: int) -> int:
        res = 0
        while left >= 0 and right < len(s) and s[left] == s[right]:
            res += 1
            left -= 1
            right += 1

        return res

if __name__ == "__main__":
    s = Solution()

    # Example 1
    assert s.countSubstrings("abc") == 3, "Example 1 failed"

    # Example 2
    assert s.countSubstrings("aaa") == 6, "Example 2 failed"

    # Single character
    assert s.countSubstrings("a") == 1, "Single character failed"

    # Two characters, no palindrome except singles
    assert s.countSubstrings("ab") == 2, "Two-char no palindrome failed"

    # Two characters, palindrome
    assert s.countSubstrings("aa") == 3, "\"aa\" palindrome set failed"

    # Mixed
    # Palindromes: a, b, a, aba
    assert s.countSubstrings("aba") == 4, "\"aba\" failed"

    # More complex
    # s = "abba"
    # palindromes: a, b, b, a, bb, abba → 6
    assert s.countSubstrings("abba") == 6, "\"abba\" failed"

    # Repeated letters
    assert s.countSubstrings("aaaa") == 10, "\"aaaa\" failed"
    # Explanation: 4 singles + 3 doubles + 2 triples + 1 quadruple

    # Random mixed
    assert s.countSubstrings("racecar") == 10, "\"racecar\" failed"
    # palindromes: r,a,c,e,c,a,r + (cec, aceca, racecar)

    print("All tests passed!")