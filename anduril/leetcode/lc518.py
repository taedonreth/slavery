# leetcode 518: coin change II (medium)

"""
You are given an integer array coins representing coins of different denominations and an integer amount representing a total amount of money.

Return the number of combinations that make up that amount. If that amount of money cannot be made up by any combination of the coins, return 0.

You may assume that you have an infinite number of each kind of coin.

The answer is guaranteed to fit into a signed 32-bit integer.



Example 1:

Input: amount = 5, coins = [1,2,5]
Output: 4
Explanation: there are four ways to make up the amount:
5=5
5=2+2+1
5=2+1+1+1
5=1+1+1+1+1
Example 2:

Input: amount = 3, coins = [2]
Output: 0
Explanation: the amount of 3 cannot be made up just with coins of 2.
Example 3:

Input: amount = 10, coins = [10]
Output: 1


Constraints:

1 <= coins.length <= 300
1 <= coins[i] <= 5000
All the values of coins are unique.
0 <= amount <= 5000
"""

from typing import List


class Solution:
    def change(self, amount: int, coins: List[int]) -> int:
        """
        dp to keep track of the # of ways to make amount i
        loop through coins
            loop through amount from coin c -> amount + 1
                # recurrence
                dp[amount] += dp[amount - coin]

        return dp[amount]

        for each coin and each amount
            you are looking at how many ways did you make this value with this coin, built on top of how many ways did I make this value without this
            coin
        """

        dp = [0] * (amount + 1)
        dp[0] = 1

        for c in coins:
            for val in range(c, amount + 1):
                dp[val] += dp[val - c]

        return dp[amount]


if __name__ == "__main__":
    sol = Solution()

    # Example 1
    amount1 = 5
    coins1 = [1, 2, 5]
    assert sol.change(amount1, coins1) == 4

    # Example 2
    amount2 = 3
    coins2 = [2]
    assert sol.change(amount2, coins2) == 0

    # Example 3
    amount3 = 10
    coins3 = [10]
    assert sol.change(amount3, coins3) == 1

    # Edge case: amount = 0
    amount4 = 0
    coins4 = [1, 2, 3]
    assert sol.change(amount4, coins4) == 1  # one way — use no coins

    # Edge case: large coin values
    amount5 = 7
    coins5 = [5, 10, 25]
    assert sol.change(amount5, coins5) == 0  # cannot make 7 with these coins

    # Multiple combinations
    amount6 = 10
    coins6 = [1, 2, 5]
    assert sol.change(amount6, coins6) == 10

    # Coins with gaps
    amount7 = 6
    coins7 = [1, 3, 4]
    assert sol.change(amount7, coins7) == 4
    # (1x6), (3+3), (4+1+1), (3+1+1+1)

    # Larger denomination set
    amount8 = 8
    coins8 = [2, 3, 5]
    assert sol.change(amount8, coins8) == 3
    # (3+5), (2+3+3), (2+2+2+2)

    # Duplicate coverage test
    amount9 = 4
    coins9 = [1, 2, 3]
    assert sol.change(amount9, coins9) == 4
    # (1+1+1+1), (2+2), (1+3), (1+1+2)

    print("✅ All test cases passed!")
