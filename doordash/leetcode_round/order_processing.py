"""
The chef processes the eligible orders one at a time and deletes the orderId processed from the array. In a given array of orders, an eligible orderId is the orderId that is greater than its immediate left neighbor and Immediate right neighbor. For the first element in the array, it is eligible if it is greater than its right neighbor; for the last element it should only be greater than its left neighbor. If there are more than 1 eligible orderid then chef processes the order with smaller orderid. Return sequence of processing the order.

Eg.

Initial OrderIds = [3,1,5,4,2]

In first iteration 3 and 5 both eligible so take 3 Order processed: 3 After processing the order 3 array would look like remaining orders would be [1,5,4,2]

After 2nd iteration In second iteration only 5 is eligible so Order processed: 5 Array would [1,4,2]

After 3rd iteration Only 4 is eligible Order processed:4 Array would be[1,2]

After 4th iteration Only eligible item is 2 Order processed:2 Array would be [1]

Finally array would be [1] Order processed: 1

So ans 3,5,4,2,1

Interviwer was looking for O(n) solution.

Naive: go through array and look for eligable, remove and
"""

import heapq


def process_orders(arr):
    if not arr:
        return []

    n = len(arr)
    prev = [i - 1 for i in range(n)]
    nxt = [i + 1 for i in range(n)]
    nxt[-1] = -1
    active = [True] * n  # tracks if the index has been processed

    # Check if an index is eligible
    def eligible(i):
        if not active[i]:
            return False
        l = prev[i]
        r = nxt[i]
        if l == -1 and r == -1:
            return True
        if l == -1:
            return arr[i] > arr[r]
        if r == -1:
            return arr[i] > arr[l]
        return arr[i] > arr[l] and arr[i] > arr[r]

    # Initialize heap with all initially eligible indices
    heap = []
    for i in range(n):
        if eligible(i):
            heapq.heappush(heap, (arr[i], i))

    res = []

    while heap:
        val, idx = heapq.heappop(heap)

        # Skip if already processed (could happen if neighbors were pushed multiple times)
        if not active[idx]:
            continue

        res.append(val)
        active[idx] = False

        l, r = prev[idx], nxt[idx]

        # Update linked list
        if l != -1:
            nxt[l] = r
        if r != -1:
            prev[r] = l

        # Add neighbors if they become eligible
        for ni in (l, r):
            if ni != -1 and eligible(ni):
                heapq.heappush(heap, (arr[ni], ni))

    return res


# ------------------------
# Example test cases
# ------------------------
if __name__ == "__main__":
    tests = [[3, 5, 1, 4, 2], [], [1], [4, 1, 5], [1, 2, 3, 4, 5], [5, 3, 1, 2, 4]]

    for t in tests:
        print(f"{t} -> {process_orders(t)}")

"""
time: O(n log n) heap
space: O(n) tracking arrays
"""
