# leetcode 150: evaluate reverse polish notation (medium)

"""
You are given an array of strings tokens that represents an arithmetic expression in a Reverse Polish Notation.

Evaluate the expression. Return an integer that represents the value of the expression.

Note that:

The valid operators are '+', '-', '*', and '/'.
Each operand may be an integer or another expression.
The division between two integers always truncates toward zero.
There will not be any division by zero.
The input represents a valid arithmetic expression in a reverse polish notation.
The answer and all the intermediate calculations can be represented in a 32-bit integer.
 

Example 1:

Input: tokens = ["2","1","+","3","*"]
Output: 9
Explanation: ((2 + 1) * 3) = 9
Example 2:

Input: tokens = ["4","13","5","/","+"]
Output: 6
Explanation: (4 + (13 / 5)) = 6
Example 3:

Input: tokens = ["10","6","9","3","+","-11","*","/","*","17","+","5","+"]
Output: 22
Explanation: ((10 * (6 / ((9 + 3) * -11))) + 17) + 5
= ((10 * (6 / (12 * -11))) + 17) + 5
= ((10 * (6 / -132)) + 17) + 5
= ((10 * 0) + 17) + 5
= (0 + 17) + 5
= 17 + 5
= 22
 

Constraints:

1 <= tokens.length <= 104
tokens[i] is either an operator: "+", "-", "*", or "/", or an integer in the range [-200, 200].
"""

from typing import List

class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        """
        use stack
        if its a number
            add it to stack
        if its an operation
            pop 2 most recent numbers, apply operation, add result to stack

        note: use floor division
        """
        stack = []
        for char in tokens:
            if char not in ["-", "+", "/", "*"]:
                stack.append(int(char))
            else:
                num1 = int(stack.pop())
                num2 = int(stack.pop())
                curr_res = 0
                if char == "+":
                    curr_res = num1 + num2
                elif char == "-":
                    curr_res = num2 - num1
                elif char == "*":
                    curr_res = num1 * num2
                elif char == "/":
                    curr_res = int(num2 / num1)
                stack.append(curr_res)

        return stack.pop()

if __name__ == "__main__":
    sol = Solution()

    # Example tests
    assert sol.evalRPN(["2","1","+","3","*"]) == 9
    assert sol.evalRPN(["4","13","5","/","+"]) == 6
    assert sol.evalRPN(["10","6","9","3","+","-11","*","/","*","17","+","5","+"]) == 22
    

    # Additional cases
    # Single number
    assert sol.evalRPN(["5"]) == 5

    # Negative numbers
    assert sol.evalRPN(["-2","3","*"]) == -6

    # Subtraction ordering
    assert sol.evalRPN(["5","1","-"]) == 4   # 5 - 1

    # Division truncation toward zero
    assert sol.evalRPN(["7","-3","/"]) == -2   # trunc toward 0

    # Larger expression
    assert sol.evalRPN(["3","4","+","2","*","7","/"]) == 2  # ((3+4)*2)/7 = 14/7 = 2

    print("All tests passed!")