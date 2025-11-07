# leetcode 818: race car (hard)

"""
Your car starts at position 0 and speed +1 on an infinite number line. Your car can go into negative positions. Your car drives automatically according to a sequence of instructions 'A' (accelerate) and 'R' (reverse):

When you get an instruction 'A', your car does the following:
position += speed
speed *= 2
When you get an instruction 'R', your car does the following:
If your speed is positive then speed = -1
otherwise speed = 1
Your position stays the same.
For example, after commands "AAR", your car goes to positions 0 --> 1 --> 3 --> 3, and your speed goes to 1 --> 2 --> 4 --> -1.

Given a target position target, return the length of the shortest sequence of instructions to get there.



Example 1:

Input: target = 3
Output: 2
Explanation:
The shortest instruction sequence is "AA".
Your position goes from 0 --> 1 --> 3.
Example 2:

Input: target = 6
Output: 5
Explanation:
The shortest instruction sequence is "AAARA".
Your position goes from 0 --> 1 --> 3 --> 7 --> 7 --> 6.


Constraints:

1 <= target <= 104
"""


class Solution:
    def racecar(self, target: int) -> int:
        pass


if __name__ == "__main__":
    sol = Solution()

    # Example 1
    assert sol.racecar(3) == 2  # "AA"

    # Example 2
    assert sol.racecar(6) == 5  # "AAARA"

    # Small targets (edge base cases)
    assert sol.racecar(1) == 1  # "A"
    assert sol.racecar(2) == 4  # "AARA"
    assert sol.racecar(4) == 5  # "AARAR" or equivalent

    # Slightly larger
    assert sol.racecar(5) == 7
    assert sol.racecar(7) == 3  # "AAA" (1 → 3 → 7)
    assert sol.racecar(8) == 6
    assert sol.racecar(9) == 8
    assert sol.racecar(10) == 7

    # Random mid-size targets
    assert sol.racecar(15) == 4  # "AAAA" (1+2+4+8=15)
    assert sol.racecar(16) == 5  # "AAAAA" overshoots, needs reverse
    assert sol.racecar(11) == 10
    assert sol.racecar(12) == 7

    # Nontrivial reach near powers of two
    assert sol.racecar(31) == 5  # "AAAAA"
    assert sol.racecar(32) == 6
    assert sol.racecar(17) == 8

    # Larger stress tests (should run efficiently)
    assert sol.racecar(50) == 11
    assert sol.racecar(100) == 15
    assert sol.racecar(300) == 21
    assert sol.racecar(500) == 25
    assert sol.racecar(1000) == 29

    print("✅ All test cases passed!")
