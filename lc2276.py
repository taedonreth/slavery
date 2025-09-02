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
    # BST
    # merge overlapping intervals on addition

    def __init__(self):
        pass

    def add(self, left: int, right: int) -> None:
        pass

    def count(self) -> int:
        pass


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
