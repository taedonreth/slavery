# leetcode 322: coin change (medium)

from typing import List


class Solution:
    """
    You are given an integer array coins representing coins of different denominations and an integer amount representing a total amount of money.
    Return the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return -1.
    You may assume that you have an infinite number of each kind of coin.
    """

    def coinChange(self, coins: List[int], amount: int) -> int:
        """
        dp
        dp array with length amount + 1
        each index in dp represents the min # of coins we can make this value with, -1 if we cant
        base case: dp[0] = 0
        for i in range(1, amount + 1):
            for coin in coins:
                if i - coin >= 0:
                    dp[i] = min(dp[i - coin] + 1, dp[i])

        return dp[amount]
        """
        coins.sort()
        dp = [float("inf")] * (amount + 1)
        dp[0] = 0
        for i in range(1, amount + 1):
            for coin in coins:
                if i - coin >= 0:
                    dp[i] = min(dp[i - coin] + 1, dp[i])

        return dp[amount] if dp[amount] != float("inf") else -1


def main():
    sol = Solution()

    # Example 1
    coins, amount = [1, 2, 5], 11
    assert sol.coinChange(coins, amount) == 3  # 11 = 5 + 5 + 1

    # Example 2
    coins, amount = [2], 3
    assert sol.coinChange(coins, amount) == -1  # cannot make 3 with only 2s

    # Example 3
    coins, amount = [1], 0
    assert sol.coinChange(coins, amount) == 0  # 0 coins to make 0 amount

    # Extra test: single coin type exactly matches
    coins, amount = [7], 14
    assert sol.coinChange(coins, amount) == 2  # 7 + 7

    # Extra test: mixed coins
    coins, amount = [2, 5, 10, 1], 27
    assert sol.coinChange(coins, amount) == 4  # 10 + 10 + 5 + 2

    print("All tests passed!")


if __name__ == "__main__":
    main()
