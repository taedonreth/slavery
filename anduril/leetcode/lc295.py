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
    Use a frequency array of size 101 → O(1) insertion, O(100) = O(1) median finding
If 99% of all integer numbers from the stream are in the range [0, 100], how would you optimize your solution?
    Hybrid approach - frequency array for [0, 100] + heaps for outliers
"""


import heapq


class MedianFinder:
    """
    Two-heap approach to find median in O(log n) time for insertion and O(1) for retrieval.
    
    Strategy:
    - Use a max heap (small) for the smaller half of numbers
    - Use a min heap (large) for the larger half of numbers
    - Keep heaps balanced: sizes differ by at most 1
    - Median is either top of one heap or average of both tops
    
    Invariants:
    1. len(small) == len(large) or len(small) == len(large) + 1
    2. max(small) <= min(large) (all elements in small <= all in large)
    """

    def __init__(self):
        # Max heap for smaller half (negate values since Python only has min heap)
        self.small = []  # Max heap (we negate values)
        # Min heap for larger half
        self.large = []  # Min heap

    def addNum(self, num: int) -> None:
        """
        Add a number to the data structure.
        
        Process:
        1. Add to small heap (max heap)
        2. Balance: move largest from small to large
        3. Rebalance if large becomes larger than small
        
        Time: O(log n) - heap operations
        """
        # Always add to small heap first (as a max heap, we negate)
        heapq.heappush(self.small, -num)
        
        # Ensure all elements in small <= all elements in large
        # Move the largest from small to large
        if self.small and self.large and (-self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        
        # Balance the sizes: small should have equal or 1 more element than large
        if len(self.large) > len(self.small):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)
        
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)

    def findMedian(self) -> float:
        """
        Return the median of all elements.
        
        - If odd count: return top of small heap (which has 1 extra element)
        - If even count: return average of both heap tops
        
        Time: O(1) - just accessing heap tops
        """
        if len(self.small) > len(self.large):
            # Odd number of elements, small has one extra
            return float(-self.small[0])
        else:
            # Even number of elements, take average
            return (-self.small[0] + self.large[0]) / 2.0


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
