"""
You're a dasher, and you want to try planning out your schedule. You can view a list of deliveries along with their associated start time, end time, and dollar amount for completing the order. Assuming dashers can only deliver one order at a time, determine the maximum amount of money you can make from the given deliveries.

The inputs are as follows:

int start_time: when you plan to start your schedule
int end_time: when you plan to end your schedule
int d_starts[n]: the start times of each delivery[i]
int d_ends[n]: the end times of each delivery[i]
int d_pays[n]: the pay for each delivery[i]
The output should be an integer representing the maximum amount of money you can make by forming a schedule with the given deliveries.
  Constraints

end_time >= start_time
d_ends[i] >= d_starts[i]
d_pays[i] > 0
len(d_starts) == len(d_ends) == len(d_pays)
  Example 1

start_time = 0
end_time = 10
d_starts = [2, 3, 5, 7]
d_ends = [6, 5, 10, 11]
d_pays = [5, 2, 4, 1]
Expected output: 6


Followup 1: Return the jobs as well which will give max profit

Followup 2: If the dasher is allowed to handle up to N orders at the same time, what will be the max profit?
"""


def max_delivery_profit(start_time, end_time, d_starts, d_ends, d_pays):
    # Filter and sort deliveries
    deliveries = []
    for i in range(len(d_starts)):
        if d_starts[i] >= start_time and d_ends[i] <= end_time:
            deliveries.append((d_starts[i], d_ends[i], d_pays[i], i))

    if not deliveries:
        return 0

    deliveries.sort(key=lambda x: x[1])
    n = len(deliveries)

    # Binary search for latest non-overlapping delivery
    def find_latest_non_overlap(index):
        start = deliveries[index][0]
        lo, hi = 0, index - 1
        result = -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if deliveries[mid][1] <= start:
                result = mid
                lo = mid + 1
            else:
                hi = mid - 1
        return result

    dp = [0] * n
    dp[0] = deliveries[0][2]

    for i in range(1, n):
        profit_with = deliveries[i][2]
        latest = find_latest_non_overlap(i)
        if latest != -1:
            profit_with += dp[latest]

        dp[i] = max(profit_with, dp[i - 1])

    """
    # Backtrack to find jobs
    selected = []
    i = n - 1
    while i >= 0:
        if i == 0:
            selected.append(deliveries[0][3])
            break
        
        # Check if current job was taken
        profit_with = deliveries[i][2]
        latest = find_latest_non_overlap(i)
        if latest != -1:
            profit_with += dp[latest]
        
        if profit_with >= dp[i - 1]:
            selected.append(deliveries[i][3])
            i = latest
        else:
            i -= 1
    
    return dp[n - 1], selected[::-1]
    """

    return dp[n - 1]


"""
def max_profit_n_concurrent(start_time, end_time, d_starts, d_ends, d_pays, N):
    deliveries = []
    for i in range(len(d_starts)):
        if d_starts[i] >= start_time and d_ends[i] <= end_time:
            deliveries.append((d_starts[i], d_ends[i], d_pays[i], i))
    
    if not deliveries:
        return 0
    
    # Sort by end time
    deliveries.sort(key=lambda x: x[1])
    n = len(deliveries)
    
    # dp[i][k] = max profit using first i deliveries with at most k concurrent
    # But we need to track which jobs are active at each point
    
    # Alternative: For each delivery, track best k-1 non-overlapping sets
    # This gets complex - simpler approach: greedy with heap
    
    import heapq
    # Greedy: sort by end time, maintain heap of active deliveries
    deliveries_by_end = sorted(deliveries, key=lambda x: x[1])
    
    active = []  # min heap by end time
    total_profit = 0
    
    for delivery in deliveries_by_end:
        start, end, pay, idx = delivery
        
        # Remove completed deliveries
        while active and active[0][0] <= start:
            heapq.heappop(active)
        
        # If we have capacity, take it
        if len(active) < N:
            heapq.heappush(active, (end, pay))
            total_profit += pay
        # If this delivery pays more than lowest active, swap
        elif pay > active[0][1]:
            _, old_pay = heapq.heappop(active)
            heapq.heappush(active, (end, pay))
            total_profit += pay - old_pay
    
    return total_profit

time: O(n log n) sorting
space: O(n) dp array
"""
