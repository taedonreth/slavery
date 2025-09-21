# leetcode 308: best time to buy and sell stock with cooldown (medium)

from typing import List

"""
You are given an array prices where prices[i] is the price of a given stock on the ith day.

Find the maximum profit you can achieve. You may complete as many transactions as you like 
(i.e., buy one and sell one share of the stock multiple times) with the following restrictions:

After you sell your stock, you cannot buy stock on the next day (i.e., cooldown one day).
Note: You may not engage in multiple transactions simultaneously (i.e., you must sell the stock before you buy again).
"""


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        """
        dp
        create 3 dp arrays with length len(prices) + 1 where each index i represents total profit possible on day i
            hold # keep holding or buy
            sold # sell today and cooldown tomorrow
            rest # keep holding or buy

            hold represents: holding a stock you already bought or buying one today
            sell= selling today
            rest = cooldown period or doing nothing when you have no stock in possesion like you can buy buyt its not a good choice
        base cases:
            hold[0] = -prices[0] # buy on day 0
            sold[0] = 0 # cant sell on day 0
            rest[0] = 0 # do nothing

        iterate through prices and for each day i,
            keep holding or buy today if we rested yesterday
            hold[i] = max(hold[i-1], rest[i-1] - prices[i])

            sell stock today
            sold[i] = hold[i-1] + prices[i]

            keep resting or if you sold yesterday you need to cooldown so do nothing
            rest[i] = max(rest[i-1], sold[i-1])

        answer will be max(hold[-1], sold[-1])
        """

        # actually since you only need i-1 and i, we can have hold, sold, and rest be ints instead of arrays
        hold, sold, rest = -prices[0], 0, 0
        for price in prices[1:]:
            prev_hold, prev_sold, prev_rest = hold, sold, rest
            hold = max(prev_hold, prev_rest - price)
            sold = prev_hold + price
            rest = max(prev_rest, prev_sold)

        return max(hold, sold, rest)


def main():
    s = Solution()
    # Example 1
    assert s.maxProfit([1, 2, 3, 0, 2]) == 3
    # Example 2
    assert s.maxProfit([1]) == 0
    print("All tests passed!")


if __name__ == "__main__":
    main()
