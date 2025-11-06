# leetcode 875: koko eating bananas (medium)

"""
Koko loves to eat bananas. There are n piles of bananas, the ith pile has piles[i] bananas. The guards have gone and will come back in h hours.

Koko can decide her bananas-per-hour eating speed of k. Each hour, she chooses some pile of bananas and eats k bananas from that pile. If the pile has less than k bananas, she eats all of them instead and will not eat any more bananas during this hour.

Koko likes to eat slowly but still wants to finish eating all the bananas before the guards return.

Return the minimum integer k such that she can eat all the bananas within h hours.
"""

from typing import List
from math import ceil


class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        """
        Input: piles = [3,6,7,11], h = 8
        Output: 4

        sort piles
        k has to be between 0 and piles[-1]
        helper function to see if our candidate k is valid
            how do we tell if k is valid?
                iterate through piles:
                    hours += ceil(piles[i] / k)

                return hours <= h

        binary search from 0 to piles[-1]
            test if k is valid and return the lowest valid k
        """

        def _is_valid_k(candidate: int) -> bool:
            hours = 0
            for num_bananas in piles:
                hours += ceil(num_bananas / candidate)

            return hours <= h

        left = 1
        right = max(piles)
        res = 0

        while left <= right:
            mid = (left + right) // 2
            if _is_valid_k(mid):
                res = mid
                right = mid - 1
            else:
                left = mid + 1

        return res


"""
time: O(n * log(max(piles)))
    binary runs log(max(piles)) times and each time does O(n) search through piles
space: O(1)
"""
