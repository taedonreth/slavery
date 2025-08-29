# leetcode 2468: split message based on limit (hard)
from typing import List, Optional

"""
You are given a string, message, and a positive integer, limit.

You must split message into one or more parts based on limit. Each resulting part should have the
suffix "<a/b>", where "b" is to be replaced with the total number of parts and "a" is to be replaced
with the index of the part, starting from 1 and going up to b. Additionally, the length of each
resulting part (including its suffix) should be equal to limit, except for the last part whose
length can be at most limit

The resulting parts should be formed such that when their suffixes are removed and they are all
concatenated in order, they should be equal to message. Also, the result should contain as few parts
as possible

Return the parts message would be split into as an array of strings. If it is impossible to split
message as required, return an empty array
"""


class Solution:
    # helper function to split message
    # given argument parts, return true if we can split the message into that many parts
    def find_num_parts(self, message: str, limit: int, parts: int) -> int:
        i = 0
        n = len(message)

        for part in range(1, parts + 1):
            suffix = f"<{part}/{parts}>"
            remaining = limit - len(suffix)

            if remaining <= 0:
                return 0
            i += remaining
            if i >= n:
                if part == parts:
                    return 1
                else:
                    return -1
        return 2

    # binary search to find the right b
    # given any limit and any message:
    # the min # of parts is 1 (whole message on one line), max is len(message) parts (1 char per line)
    # we know b, now build the message based on b
    def splitMessage(self, message: str, limit: int) -> List[str]:
        """
        how do you know what it is out of? how do we know it is out of 14

        the move is to calculate the suffix, then add letters that you can once you know the size of the suffix
        figuring out the size of the suffix is hard because we don't know the total

        big question: how do you know the size of the suffix
            len(str) // (limit - suffix length) would work if we knew suffix length for each part
            to know suffix length for each part, we need to know total parts

            guess total parts using binary search:
                assume some b.
                simulate splitting under that assumption.
                see how many parts you actually produced.
                if it matches your assumption → done.
                if not → increase your guess and try again.
        """

        # loop through possible values of b (start from 1).
        # for each b, compute how many parts you’d need if the suffix size is based on that b.
        # if the number of parts needed is == b, then b is valid → lock it in.
        # once you have b, do the actual splitting.

        l = 1
        r = len(message)
        result = None

        while l <= r:
            mid = (l + r) // 2
            if mid == 0:
                l = 1
                continue

            split_into_mid_parts = self.find_num_parts(message, limit, mid)
            if split_into_mid_parts == 2:
                l = mid + 1
            else:
                result = mid
                r = mid - 1  # continue searching for smaller solution

        if result is None:
            return []

        res, j = [], 0
        for a in range(1, result + 1):
            suffix = f"<{a}/{result}>"
            remaining = limit - len(suffix)
            res.append(message[j : j + remaining] + suffix)
            j += remaining
        return res


def main():
    sol = Solution()

    # example 1
    message = "this is really a very awesome message"
    limit = 9
    expected = [
        "thi<1/14>",
        "s i<2/14>",
        "s r<3/14>",
        "eal<4/14>",
        "ly <5/14>",
        "a v<6/14>",
        "ery<7/14>",
        " aw<8/14>",
        "eso<9/14>",
        "me<10/14>",
        " m<11/14>",
        "es<12/14>",
        "sa<13/14>",
        "ge<14/14>",
    ]
    assert sol.splitMessage(message, limit) == expected

    # Example 2
    message = "short message"
    limit = 15
    expected = ["short mess<1/2>", "age<2/2>"]
    assert sol.splitMessage(message, limit) == expected

    print("All test cases passed!")


if __name__ == "__main__":
    main()
