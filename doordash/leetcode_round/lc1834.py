# leetcode 1834: single threaded cpu (medium)

"""
You are given n tasks labeled from 0 to n - 1 represented by a 2D integer array tasks, where tasks[i] = [enqueueTimei, processingTimei] means that the ith task will be available to process at enqueueTimei and will take processingTimei to finish processing.

You have a single-threaded CPU that can process at most one task at a time and will act in the following way:

If the CPU is idle and there are no available tasks to process, the CPU remains idle.
If the CPU is idle and there are available tasks, the CPU will choose the one with the shortest processing time. If multiple tasks have the same shortest processing time, it will choose the task with the smallest index.
Once a task is started, the CPU will process the entire task without stopping.
The CPU can finish a task then start a new one instantly.
Return the order in which the CPU will process the tasks.
"""

from typing import List, Tuple
import heapq


class Solution:
    def getOrder(self, tasks: List[List[int]]) -> List[int]:
        """
        Input: tasks = [[1,2],[2,4],[3,2],[4,1]]
        Output: [0,2,3,1]

        minheap for enqueued tasks of the form (processing time, index)
        keep track of curr time

        sort tasks based on enqueue time, keep track of indicies

        while there are still tasks to process
            if heap is empty (no tasks ready)
                skip to first task time

            while loop to push all tasks which have enqueue time <= curr_time

            process task with min process time and min index

            update curr_time
            add to result

        return res
        """

        heap = []
        res = []
        sorted_tasks = []
        curr_time = 0

        # create task list with indicies and sort
        for i, (enqueue, processing) in enumerate(tasks):
            sorted_tasks.append([enqueue, processing, i])

        sorted_tasks.sort()

        idx = 0
        while idx < len(tasks) or heap:
            if not heap and curr_time < sorted_tasks[idx][0]:
                curr_time = sorted_tasks[idx][0]

            while idx < len(tasks) and sorted_tasks[idx][0] <= curr_time:
                heapq.heappush(heap, (sorted_tasks[idx][1], sorted_tasks[idx][2]))
                idx += 1

            processing, index = heapq.heappop(heap)
            curr_time += processing
            res.append(index)

        return res


"""
time: O(n log n)
space: O(n)
"""


if __name__ == "__main__":
    s = Solution()

    # Example 1
    tasks = [[1, 2], [2, 4], [3, 2], [4, 1]]
    assert s.getOrder(tasks) == [0, 2, 3, 1], "Test case 1 failed"

    # Example 2
    tasks = [[7, 10], [7, 12], [7, 5], [7, 4], [7, 2]]
    assert s.getOrder(tasks) == [4, 3, 2, 0, 1], "Test case 2 failed"

    # Example 3 (single task)
    tasks = [[5, 3]]
    assert s.getOrder(tasks) == [0], "Test case 3 failed"

    # Example 4 (tasks available at different times)
    tasks = [[0, 3], [1, 9], [2, 6]]
    assert s.getOrder(tasks) == [0, 2, 1], "Test case 4 failed"

    print("All test cases passed!")
