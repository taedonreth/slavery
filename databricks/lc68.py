# leetcode 68: text justification (hard)
from typing import List

"""
Given an array of strings words and a width maxWidth, format the text such that each line has exactly maxWidth characters and is fully (left and right) justified.

You should pack your words in a greedy approach; that is, pack as many words as you can in each line. Pad extra spaces ' ' when necessary so that each line has exactly maxWidth characters.

Extra spaces between words should be distributed as evenly as possible. If the number of spaces on a line does not divide evenly between words, the empty slots on the left will be assigned more spaces than the slots on the right.

For the last line of text, it should be left-justified, and no extra space is inserted between words.

Note:

A word is defined as a character sequence consisting of non-space characters only.
Each word's length is guaranteed to be greater than 0 and not exceed maxWidth.
The input array words contains at least one word.
"""


class Solution:

    def fullJustify(self, words: List[str], maxWidth: int) -> List[str]:
        """
        definitely have a running counter for each line
        each word adds word length + 1 to line width (for a space after), if it isn't the last
        words can be last in line, or not last in line
        last in line adds length of word to width
        not last in line adds length of word + 1 to width
        if another word makes line width > maxWidth
            calculate remaining spaces in current line (maxWidth - curr_line_length)
            calcuate num of existing spaces (num words in line - 1)
            # remaining spaces will become spaces added to existing spaces (left space biased)
            num spaces to add = remaining spaces // existing spaces
            if remaining spaces % existing spaces is not 0 (leftover spaces)
                add num_spaces_to_add + 1 spaces to first (remaining spaces % existing spaces) existing spaces
                add num_spaces_to_add spaces to second space
            start a new line

        # we can treat the last line separately and add the rest of the spaces at the end?
        if len(result[-1]) != maxWidth:
            result[-1] = result[-1] + " " * maxWidth - len(result[-1])??

        """
        res = []
        idx = 0

        # go through entire array
        while idx < len(words):
            # curr_line will hold indexes of words than can fit on the current line (accounting for min # of spaces)
            idx_to_include = []
            len_curr_line = 0

            # build lines one at a time -> there is still more space without overfilling, add more
            while idx < len(words):
                add_len = len(words[idx]) if len_curr_line == 0 else len(words[idx]) + 1
                if len_curr_line + add_len > maxWidth:
                    break
                len_curr_line += add_len
                idx_to_include.append(idx)
                idx += 1

            # given which indices and length of current words in line + min # of spaces: build line and append it to answer
            curr_line = ""
            min_spaces = len(idx_to_include) - 1

            # last line OR line with only one word → left-justified
            if idx == len(words) or min_spaces == 0:
                curr_line = " ".join(words[i] for i in idx_to_include)
                curr_line += " " * (maxWidth - len(curr_line))
                res.append(curr_line)
                continue

            # middle justified
            remaining_spaces = maxWidth - (sum(len(words[i]) for i in idx_to_include))
            spaces_to_add = remaining_spaces // min_spaces
            leftover_spaces = remaining_spaces % min_spaces

            for i in idx_to_include:
                curr_line += words[i]
                if i != idx_to_include[-1]:
                    curr_line += " " * (
                        spaces_to_add + (1 if leftover_spaces > 0 else 0)
                    )
                    if leftover_spaces > 0:
                        leftover_spaces -= 1

            res.append(curr_line)

        return res


def main():
    sol = Solution()

    # Example 1
    words = ["This", "is", "an", "example", "of", "text", "justification."]
    maxWidth = 16
    expected = ["This    is    an", "example  of text", "justification.  "]
    assert sol.fullJustify(words, maxWidth) == expected

    # Example 2
    words = ["What", "must", "be", "acknowledgment", "shall", "be"]
    maxWidth = 16
    expected = ["What   must   be", "acknowledgment  ", "shall be        "]
    assert sol.fullJustify(words, maxWidth) == expected

    # Example 3
    words = [
        "Science",
        "is",
        "what",
        "we",
        "understand",
        "well",
        "enough",
        "to",
        "explain",
        "to",
        "a",
        "computer.",
        "Art",
        "is",
        "everything",
        "else",
        "we",
        "do",
    ]
    maxWidth = 20
    expected = [
        "Science  is  what we",
        "understand      well",
        "enough to explain to",
        "a  computer.  Art is",
        "everything  else  we",
        "do                  ",
    ]
    assert sol.fullJustify(words, maxWidth) == expected

    print("All test cases passed!")


if __name__ == "__main__":
    main()
