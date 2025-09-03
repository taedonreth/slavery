"""
Implement the myAtoi(string s) function, which converts a string to a 32-bit signed integer.

The algorithm for myAtoi(string s) is as follows:

Whitespace: Ignore any leading whitespace (" ").
Signedness: Determine the sign by checking if the next character is '-' or '+', assuming positivity if neither present.
Conversion: Read the integer by skipping leading zeros until a non-digit character is encountered or the end of the string is reached. If no digits were read, then the result is 0.
Rounding: If the integer is out of the 32-bit signed integer range [-231, 231 - 1], then round the integer to remain in the range. Specifically, integers less than -231 should be
    rounded to -231, and integers greater than 231 - 1 should be rounded to 231 - 1.
Return the integer as the final result.
"""


class Solution:
    # given a string, parse it to relevant integer
    def parse_string(self, s: str) -> str:
        """
        important characters are "-", integers 0-9
        ignore whitespaces until the first important character is read
        stop if we see an english letter, "."
        once an important character is read, we can only see integers 0-9 -> have bool value for if important character has been seen


        remove leading whitespace
        if signed, add sign

        while digits
            add in
        """

        res = ""
        i = 0
        s = s.lstrip()

        if i < len(s) and (s[i] == "+" or s[i] == "-"):
            res += s[i]
            i += 1

        while i < len(s) and s[i].isdigit():
            res += s[i]
            i += 1

        print(res)
        return res

    # given a string of an integer, return its value as a 32-bit signed integer as an integer
    def string_to_bit(self, s: str) -> int:

        # no digits
        if not s or s == "+" or s == "-":
            return 0

        res = int(s)

        if res > 2**31 - 1:
            return 2**31 - 1
        if res < -(2**31):
            return -(2**31)
        return res

    def myAtoi(self, s: str) -> int:
        """
        have a function to parse
        have a function to turn it into a bit value given an integer
        """

        parsed = self.parse_string(s)
        return self.string_to_bit(parsed)


def main():
    sol = Solution()

    # Example 1
    assert sol.myAtoi("42") == 42

    # Example 2
    assert sol.myAtoi("   -042") == -42

    # Example 3
    assert sol.myAtoi("1337c0d3") == 1337

    # Example 4
    assert sol.myAtoi("0-1") == 0

    # Example 5
    assert sol.myAtoi("words and 987") == 0

    print("All test cases passed!")


if __name__ == "__main__":
    main()
