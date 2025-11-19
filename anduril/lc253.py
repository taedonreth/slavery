# leetcode 253: meeting rooms II (medium)

"""
Given an array of meeting time intervals intervals where intervals[i] = [starti, endi], 
    return the minimum number of conference rooms required.

Example 1:
    Input: intervals = [[0,30],[5,10],[15,20]]
    Output: 2

Example 2:
    Input: intervals = [[7,10],[2,4]]
    Output: 1

Constraints:
    1 <= intervals.length <= 104
    0 <= starti < endi <= 106
"""

from typing import List
import heapq

class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        """
        sort by starting time
        min heap:
            add meeting end times to min heap
            if the current intervals starting time is >= top value in min heap
                pop from min heap and add the new ending time in
            otherwise
                add it to heap
        return size of heap
        """
        intervals.sort(key=lambda x: x[0])
        heap = [intervals[0][1]]

        for interval in intervals[1:]:
            if interval[0] >= heap[0]:
                heapq.heappop(heap)
            heapq.heappush(heap, interval[1])

        return len(heap)

if __name__ == "__main__":
    sol = Solution()
    assert sol.minMeetingRooms([[0,30], [5,10], [15,20]]) == 2
    assert sol.minMeetingRooms([[7,10], [2,4]]) == 1