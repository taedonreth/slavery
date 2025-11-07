# leetcode 295: find median from data stream (hard)

"""
The median is the middle value in an ordered integer list. If the size of the list is even, there is no middle value, and the median is the mean of the two middle values.

For example, for arr = [2,3,4], the median is 3.
For example, for arr = [2,3], the median is (2 + 3) / 2 = 2.5.
Implement the MedianFinder class:

MedianFinder() initializes the MedianFinder object.
void addNum(int num) adds the integer num from the data stream to the data structure.
double findMedian() returns the median of all elements so far. Answers within 10-5 of the actual answer will be accepted.


Example 1:

Input
["MedianFinder", "addNum", "addNum", "findMedian", "addNum", "findMedian"]
[[], [1], [2], [], [3], []]
Output
[null, null, null, 1.5, null, 2.0]

Explanation
MedianFinder medianFinder = new MedianFinder();
medianFinder.addNum(1);    // arr = [1]
medianFinder.addNum(2);    // arr = [1, 2]
medianFinder.findMedian(); // return 1.5 (i.e., (1 + 2) / 2)
medianFinder.addNum(3);    // arr[1, 2, 3]
medianFinder.findMedian(); // return 2.0


Constraints:

-105 <= num <= 105
There will be at least one element in the data structure before calling findMedian.
At most 5 * 104 calls will be made to addNum and findMedian.


Follow up:

If all integer numbers from the stream are in the range [0, 100], how would you optimize your solution?
If 99% of all integer numbers from the stream are in the range [0, 100], how would you optimize your solution?
"""


class MedianFinder:

    def __init__(self):
        pass

    def addNum(self, num: int) -> None:
        pass

    def findMedian(self) -> float:
        pass


# Your MedianFinder object will be instantiated and called as such:
# obj = MedianFinder()
# obj.addNum(num)
# param_2 = obj.findMedian()


if __name__ == "__main__":
    mf = MedianFinder()

    # Example 1
    mf.addNum(1)
    mf.addNum(2)
    assert abs(mf.findMedian() - 1.5) < 1e-5
    mf.addNum(3)
    assert abs(mf.findMedian() - 2.0) < 1e-5

    # Reset and test increasing sequence
    mf = MedianFinder()
    for num in [1, 2, 3, 4, 5]:
        mf.addNum(num)
    assert abs(mf.findMedian() - 3.0) < 1e-5

    # Even count of numbers
    mf = MedianFinder()
    for num in [5, 2, 8, 1]:
        mf.addNum(num)
    # Sorted = [1, 2, 5, 8], median = (2 + 5)/2 = 3.5
    assert abs(mf.findMedian() - 3.5) < 1e-5

    # Random order insertions
    mf = MedianFinder()
    for num in [6, 10, 2, 6, 5, 0, 6, 3]:
        mf.addNum(num)
    # Sorted = [0,2,3,5,6,6,6,10]; median = (5+6)/2 = 5.5
    assert abs(mf.findMedian() - 5.5) < 1e-5

    # Duplicate elements
    mf = MedianFinder()
    for num in [2, 2, 2, 2]:
        mf.addNum(num)
    assert abs(mf.findMedian() - 2.0) < 1e-5

    # Single element
    mf = MedianFinder()
    mf.addNum(42)
    assert abs(mf.findMedian() - 42.0) < 1e-5

    # Negative numbers
    mf = MedianFinder()
    for num in [-5, -10, -15]:
        mf.addNum(num)
    # Sorted = [-15, -10, -5], median = -10
    assert abs(mf.findMedian() - (-10.0)) < 1e-5

    # Mix of positive and negative
    mf = MedianFinder()
    for num in [-3, 1, -2, 8, 4]:
        mf.addNum(num)
    # Sorted = [-3, -2, 1, 4, 8]; median = 1
    assert abs(mf.findMedian() - 1.0) < 1e-5

    # Sequential median checks
    mf = MedianFinder()
    mf.addNum(1)
    assert abs(mf.findMedian() - 1.0) < 1e-5
    mf.addNum(2)
    assert abs(mf.findMedian() - 1.5) < 1e-5
    mf.addNum(3)
    assert abs(mf.findMedian() - 2.0) < 1e-5
    mf.addNum(4)
    assert abs(mf.findMedian() - 2.5) < 1e-5
    mf.addNum(5)
    assert abs(mf.findMedian() - 3.0) < 1e-5

    print("✅ All MedianFinder test cases passed successfully!")
