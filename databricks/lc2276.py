# leetcode 2276: count integers in intervals (hard)

"""
Given an empty set of intervals, implement a data structure that can:

Add an interval to the set of intervals.
Count the number of integers that are present in at least one interval.
Implement the CountIntervals class:

CountIntervals() Initializes the object with an empty set of intervals.
void add(int left, int right) Adds the interval [left, right] to the set of intervals.
int count() Returns the number of integers that are present in at least one interval.
Note that an interval [left, right] denotes all the integers x where left <= x <= right.
"""


class CountIntervals:
    # merge overlapping intervals on addition

    def __init__(self):
        self.intervals = []  # [l, r] sorted by l
        self.total = 0

    def _find_position(self, left: int) -> int:
        """binary search: find index where [left, ?] should be inserted."""
        lo, hi = 0, len(self.intervals)
        while lo < hi:
            mid = (lo + hi) // 2
            if self.intervals[mid][0] < left:
                lo = mid + 1
            else:
                hi = mid
        return lo  # insertion point

    def add(self, left: int, right: int) -> None:
        # add interval to intervals
        # auto merge overlapping intervals on addition
        # [[2, 3], [6, 8]] add [3,6] -> [[2, 8]]
        # update total = right - left + 1 for each interval

        i = self._find_position(left)

        # merge with previous interval if overlapping
        if i > 0 and self.intervals[i - 1][1] >= left - 1:
            i -= 1
            left = min(left, self.intervals[i][0])
            right = max(right, self.intervals[i][1])
            self.total -= self.intervals[i][1] - self.intervals[i][0] + 1
            self.intervals.pop(i)

        # merge with following intervals
        while i < len(self.intervals) and self.intervals[i][0] <= right + 1:
            left = min(left, self.intervals[i][0])
            right = max(right, self.intervals[i][1])
            self.total -= self.intervals[i][1] - self.intervals[i][0] + 1
            self.intervals.pop(i)

        # insert merged interval
        self.intervals.insert(i, [left, right])
        self.total += right - left + 1

    def count(self) -> int:
        # return count
        return self.total


# Your CountIntervals object will be instantiated and called as such:
# obj = CountIntervals()
# obj.add(left,right)
# param_2 = obj.count()


def main():
    obj = CountIntervals()

    obj.add(2, 3)
    obj.add(7, 10)
    assert obj.count() == 6  # [2,3] + [7,8,9,10]

    obj.add(5, 8)
    assert obj.count() == 8  # [2,3] + [5,6,7,8,9,10]

    print("All test cases passed!")


if __name__ == "__main__":
    main()
