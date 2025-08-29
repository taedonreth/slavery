# leetcode 2251: number of flowers in bloom (hard)

from typing import List


class Solution:
    """
    You are given a 0-indexed 2D integer array flowers, where flowers[i] = [starti, endi] means the ith flower will be in full bloom from starti to endi (inclusive).
    You are also given a 0-indexed integer array people of size n, where people[i] is the time that the ith person will arrive to see the flowers.

    Return an integer array answer of size n, where answer[i] is the number of flowers that are in full bloom when the ith person arrives.
    """

    def fullBloomFlowers(
        self, flowers: List[List[int]], people: List[int]
    ) -> List[int]:
        """
        brute force:
            result will be size of people, so loop through people and for every person go through the flowers matrix
            and increment everytime they will see that flower in full bloom

        optimization:
            for any given time t, the number of flowers blooming at time t is equal to the number of flowers
            that have started blooming minus the number of flowers that have already stopped blooming

            create res arr
            create start time array and end time array
            for each time people[i]
                # of flowers bloomed at this time = # of flowers with timestamp <= people[i] - # of flowers with timestamp < people[i]
                use binary search to find this number
                    (# of flowers with timestamp <= people[i] = largest index of start array where start[i] <= people[i])
                    (# of flowers with timestamp < people[i] = largest index of end array where end[i] < people[i])

            return result array
        """
        res = [0] * len(people)

        # use lambda functions to extract + sort start + end times
        starts = sorted(map(lambda x: x[0], flowers))
        ends = sorted(map(lambda x: x[1], flowers))

        for idx in range(len(people)):

            # binary search to find # of flowers with timestamp <= time
            start_l, start_r = 0, len(starts) - 1
            while start_l <= start_r:
                start_mid = (start_l + start_r) // 2

                if starts[start_mid] > people[idx]:
                    start_r = start_mid - 1
                else:
                    start_l = start_mid + 1

            # binary search to find # of flowers with timestamp < time
            end_l, end_r = 0, len(ends) - 1
            while end_l <= end_r:
                end_mid = (end_l + end_r) // 2

                if ends[end_mid] >= people[idx]:
                    end_r = end_mid - 1
                else:
                    end_l = end_mid + 1

            # # of flowers bloomed = bloomed - died
            res[idx] = start_l - end_l

        return res


def main():
    sol = Solution()

    # Example 1
    flowers = [[1, 6], [3, 7], [9, 12], [4, 13]]
    people = [2, 3, 7, 11]
    expected = [1, 2, 2, 2]
    assert sol.fullBloomFlowers(flowers, people) == expected

    # Example 2
    flowers = [[1, 10], [3, 3]]
    people = [3, 3, 2]
    expected = [2, 2, 1]
    assert sol.fullBloomFlowers(flowers, people) == expected

    # Edge case: single flower and single person
    flowers = [[5, 5]]
    people = [5, 6, 4]
    expected = [1, 0, 0]
    assert sol.fullBloomFlowers(flowers, people) == expected

    # Edge case: overlapping flowers
    flowers = [[1, 5], [2, 6], [3, 7]]
    people = [1, 2, 3, 6, 7]
    expected = [1, 2, 3, 2, 1]
    assert sol.fullBloomFlowers(flowers, people) == expected

    print("All test cases passed!")


if __name__ == "__main__":
    main()
