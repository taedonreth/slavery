// leetcode 647: palindromic substrings (medium)

#include <iostream>

/*
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
*/

class Solution {
public:
  int countSubstrings(string s) {
    // helper to expand
    // test each character as a center and try to expand
    // treat odd and even as different "aa" compared to "aba"

    int palindromic_cnt = 0;
    for (int i = 0; i < s.length(); i++) {
      palindromic_cnt += expand(s, i, i); // odd
      palindromic_cnt += expand(s, i, i + 1); // even
    }
    return palindromic_cnt;
  }

  int expand(string& s, int left, int right) {
    int count = 0;
    while (left >= 0 && right < s.length() && s[left] == s[right]) {
      count++;
      left--;
      right++;
    }
    return count;
  }
};
