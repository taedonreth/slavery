import heapq
from typing import List


class Solution:
    """
    You have k lists of sorted integers in non-decreasing order. Find the smallest range that includes at least one number from each of the k lists.
    We define the range [a, b] is smaller than range [c, d] if b - a < d - c or a < c if b - a == d - c.
    """

    def smallestRange(self, nums: List[List[int]]) -> List[int]:
        """
        brute force:
            calculate all ranges that includes at least 1 num from each list, return the smallest one out of those

        optimization: use min heap
            insert first element from each list into the heap
            also keep track of the largest number among the selected elements because our range depends on both the smallest and largest values.

            at each step, we extract the smallest element from the heap
            This number forms the lower bound of our current range and replace this smallest number with the next number from the same list and add it to the heap.
            check the current range between the smallest element (from the heap) and the largest element (which we track separately)
            If this new range is smaller than the previous best range, we update it.

            We repeat this process until we can no longer add numbers from one of the lists to the heap.
        """

        min_heap = []
        max_val = -float("inf")

        # push first element from each list into heap
        for i in range(len(nums)):
            # each item in the heap will be: [value, list, value index]
            heapq.heappush(min_heap, [nums[i][0], i, 0])
            max_val = max(max_val, nums[i][0])

        range_min = -float("inf")
        range_max = float("inf")
        # find lowest and highest bounds, minimize range while maintaining inclusiveness
        while len(min_heap) == len(nums):
            curr_min, arr, idx = heapq.heappop(min_heap)

            # update range
            if (max_val - curr_min < range_max - range_min) or (
                max_val - curr_min == range_max - range_min and curr_min < range_min
            ):
                range_min = curr_min
                range_max = max_val

            # update idx for next iteration, add new element to heap
            if idx + 1 < len(nums[arr]):
                next_val = nums[arr][idx + 1]
                heapq.heappush(min_heap, [next_val, arr, idx + 1])
                max_val = max(max_val, next_val)

        return [range_min, range_max]


def main():
    sol = Solution()

    # Example 1
    nums = [[4, 10, 15, 24, 26], [0, 9, 12, 20], [5, 18, 22, 30]]
    expected = [20, 24]
    assert sol.smallestRange(nums) == expected

    # Example 2
    nums = [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
    expected = [1, 1]
    assert sol.smallestRange(nums) == expected

    # Edge case: single element lists
    nums = [[1], [2], [3]]
    expected = [1, 3]
    assert sol.smallestRange(nums) == expected

    # Edge case: two lists only
    nums = [[1, 3, 5, 7, 9], [2, 4, 6, 8, 10]]
    expected = [1, 2]
    assert sol.smallestRange(nums) == expected

    print("All test cases passed!")


if __name__ == "__main__":
    main()
