class Solution:
    """
    The string "PAYPALISHIRING" is written in a zigzag pattern on a given number of rows like this: (you may want to display this pattern in a fixed font for better legibility)

    P   A   H   N
    A P L S I I G
    Y   I   R

    And then read line by line: "PAHNAPLSIIGYIR"
    Write the code that will take a string and make this conversion given a number of rows:
    string convert(string s, int numRows);
    """

    def convert(self, s: str, numRows: int) -> str:
        """
        build arr of numRows arrays
        keep track of direction: going down or up
        keep track of current row
        append letter into arr[currentrow]
        if current row == numRows - 1:
            going_up = true
        if currentrow == 0:
            going_up = false

        if going_up:
            current_row -= 1
        else:
            current_row += 1

        build string res by reading arr in order
        """
        if numRows == 1:
            return s

        zigzag = [[] for i in range(numRows)]
        DIRECTION = "DOWN"
        curr_row = 0

        for c in s:
            zigzag[curr_row].append(c)

            if curr_row == numRows - 1:
                DIRECTION = "UP"
            if curr_row == 0:
                DIRECTION = "DOWN"

            if DIRECTION == "UP":
                curr_row -= 1
            else:
                curr_row += 1

        res = ""
        for i in range(numRows):
            res += "".join(zigzag[i])

        return res


def main():
    sol = Solution()

    # Example 1
    assert sol.convert("PAYPALISHIRING", 3) == "PAHNAPLSIIGYIR"

    # Example 2
    assert sol.convert("PAYPALISHIRING", 4) == "PINALSIGYAHRPI"

    # Example 3
    assert sol.convert("A", 1) == "A"

    # Extra cases
    assert sol.convert("ABC", 1) == "ABC"  # single row → original string
    assert sol.convert("ABC", 2) == "ACB"  # zigzag with 2 rows
    assert sol.convert("", 3) == ""  # empty string

    print("All tests passed!")


if __name__ == "__main__":
    main()
