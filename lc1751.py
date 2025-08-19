from typing import List

class Solution:
    def maxValue(self, events: List[List[int]], k: int) -> int:
        """
        dp[0][k] = 
        What is the maximum value I can get if I am considering events 
        from i to the end of the list, and I have j invitations remaining

        # greedy
        sort by starting time

        make 2d array to keep track of values
            i'th row represents the event we are considering
            j'th col represents the number of invitations we have left

        base case: 
            having no events left, so dp[i][0] = 0
            and dp[n][j] = 0
        
        building the table
        at each of the other i, j:
        loop backwards rows, forwards col:
            (at each i, j)
            skip this event and dont get its value. 
                we still have j invitations, so dp[i][j] = dp[i+1][j]
            take the event and its value
                have j-1 invitations left, so dp[i][j] = event[i][value] + dp[next_event_id][j-1]

        answer:
            final answer will be in dp[0][k]
            (consider events from 0 until the end, and have max # of invitations remaining)

        helper function to find next event id:
            binary search
        """
        return 0

    """
    inputs: current event -> events (sorted), current index i, 
    output: idx of next event
    """
    def find_next_event(self, events: List[List[int]], curr_idx: int) -> int:
        start = curr_idx
        end = len(events)
        EVENT_START_IDX = 0
        EVENT_END_IDX = 1
        # [[1,2,4],[2,3,1],[3,4,3]]
        while start < end:
            next_event_idx = (start + end) // 2

            if events[next_event_idx][EVENT_START_IDX] <= events[start][EVENT_END_IDX]:
                start = next_event_idx + 1
            else:

        
        return 0


def main():
    solution = Solution()
    
    # Test Case 1: Example 1 from LeetCode
    events1 = [[1,2,4],[3,4,3],[2,3,1]]
    k1 = 2
    result1 = solution.maxValue(events1, k1)
    print(f"Test Case 1:")
    print(f"Events: {events1}")
    print(f"k = {k1}")
    print(f"Expected: 7")
    print(f"Got: {result1}")
    print(f"Result: {'PASS' if result1 == 7 else 'FAIL'}")
    print()
    
    # Test Case 2: Example 2 from LeetCode
    events2 = [[1,2,4],[3,4,3],[2,3,10]]
    k2 = 2
    result2 = solution.maxValue(events2, k2)
    print(f"Test Case 2:")
    print(f"Events: {events2}")
    print(f"k = {k2}")
    print(f"Expected: 10")
    print(f"Got: {result2}")
    print(f"Result: {'PASS' if result2 == 10 else 'FAIL'}")
    print()
    
    # Test Case 3: Example 3 from LeetCode
    events3 = [[1,1,1],[2,2,2],[3,3,3],[4,4,4]]
    k3 = 3
    result3 = solution.maxValue(events3, k3)
    print(f"Test Case 3:")
    print(f"Events: {events3}")
    print(f"k = {k3}")
    print(f"Expected: 9")
    print(f"Got: {result3}")
    print(f"Result: {'PASS' if result3 == 9 else 'FAIL'}")
    print()
    
    # Additional Edge Cases
    # Test Case 4: Single event
    events4 = [[1,3,5]]
    k4 = 1
    result4 = solution.maxValue(events4, k4)
    print(f"Test Case 4 (Single event):")
    print(f"Events: {events4}")
    print(f"k = {k4}")
    print(f"Expected: 5")
    print(f"Got: {result4}")
    print(f"Result: {'PASS' if result4 == 5 else 'FAIL'}")
    print()
    
    # Test Case 5: k = 0
    events5 = [[1,2,4],[3,4,3]]
    k5 = 0
    result5 = solution.maxValue(events5, k5)
    print(f"Test Case 5 (k=0):")
    print(f"Events: {events5}")
    print(f"k = {k5}")
    print(f"Expected: 0")
    print(f"Got: {result5}")
    print(f"Result: {'PASS' if result5 == 0 else 'FAIL'}")
    print()
    
    # Test Case 6: All events overlap
    events6 = [[1,3,2],[2,4,3],[1,2,4]]
    k6 = 2
    result6 = solution.maxValue(events6, k6)
    print(f"Test Case 6 (Overlapping events):")
    print(f"Events: {events6}")
    print(f"k = {k6}")
    print(f"Expected: 4")
    print(f"Got: {result6}")
    print(f"Result: {'PASS' if result6 == 4 else 'FAIL'}")
    print()

if __name__ == "__main__":
    main()