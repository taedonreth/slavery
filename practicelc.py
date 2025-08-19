import heapq
from typing import List

class Solution:
    def sort_k_messed_array(self, arr: List[int], k: int) -> List[int]:
        """
        Sorts an array of n elements where each element is at most k
        positions away from its sorted position.

        Args:
            arr: The nearly sorted input array.
            k: The maximum distance of an element from its sorted position.

        Returns:
            The sorted array.
        """
        # --- YOUR CODE GOES HERE ---

        # edge case
        n = len(arr)
        if n == 0 or k == 0:
            return arr

        # if arr is smaller than k+1, then we need to handle it differently
        heap_size = min(k+1, n)
        minheap = arr[:heap_size]
        heapq.heapify(minheap)
        res = []

        for i in range(heap_size, n):
            res.append(heapq.heappop(minheap))
            heapq.heappush(minheap, arr[i])
            
        while len(minheap) > 0:
            res.append(heapq.heappop(minheap))


        # --- END OF YOUR CODE ---
        return res # Default return for the placeholder

        """
        [1, 4, 5, 2, 3, 7, 8, 6, 10, 9], "k": 2
        Min heap of size k + 1
        Iterate through array starting at position k
            for each item in the array
                pop min, append to result
                add in new item to the minheap


        While still stuff in the heap:
            pop min, append to result

        Return result
                

        i= 0
        Res: [1]
        temp: [1, 4, 5]

        Res: [1, 2]
        temp: [4, 5, 2]

        Res: [1, 2, 3]
        temp: [4, 5, 3]

        Res: [1, 2, 3, 4]
        temp: [4, 5, 7]

        Res: [1, 2, 3, 4, 5]
        temp: [5, 7, 8]

        Res: [1, 2, 3, 4, 5, 6]
        temp: [7, 8, 6]

        Res: [1, 2, 3, 4, 5, 6, 7]
        temp: [8, 10, 9]

        Res: [1, 2, 3, 4, 5, 6, 7, 8]
        temp: [8, 10, 9]

        Res: [1, 2, 3, 4, 5, 6, 7, 8, 9]
        temp: [10]

        Res: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temp: []
        """

def main():
    """Main function to run test cases."""
    solver = Solution()
    
    test_cases = [
        {
            "name": "Simple Case",
            "input": {"arr": [1, 4, 5, 2, 3, 7, 8, 6, 10, 9], "k": 2},
            "expected": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        },
        {
            "name": "Another Case",
            "input": {"arr": [6, 5, 3, 2, 8, 10, 9], "k": 3},
            "expected": [2, 3, 5, 6, 8, 9, 10]
        },
        {
            "name": "Empty Array",
            "input": {"arr": [], "k": 5},
            "expected": []
        },
        {
            "name": "Already Sorted",
            "input": {"arr": [1, 2, 3, 4, 5], "k": 1},
            "expected": [1, 2, 3, 4, 5]
        },
        {
            "name": "k=1",
            "input": {"arr": [2, 1, 4, 3, 6, 5, 8, 7], "k": 1},
            "expected": [1, 2, 3, 4, 5, 6, 7, 8]
        },
        {
            "name": "All elements shifted right",
            "input": {"arr": [3, 4, 5, 1, 2], "k": 3},
            "expected": [1, 2, 3, 4, 5]
        }
    ]

    for i, test_case in enumerate(test_cases):
        input_arr = test_case["input"]["arr"]
        input_k = test_case["input"]["k"]
        expected_output = test_case["expected"]
        
        # Create a copy to sort, so we don't modify the original test case input
        arr_to_sort = list(input_arr) 
        
        actual_output = solver.sort_k_messed_array(arr_to_sort, input_k)
        
        print(f"--- Test Case {i+1}: {test_case['name']} ---")
        print(f"Input: arr={input_arr}, k={input_k}")
        print(f"Expected Output: {expected_output}")
        print(f"Actual Output:   {actual_output}")
        
        if actual_output == expected_output:
            print("✅ PASS")
        else:
            print("❌ FAIL")
        print("-" * (len(test_case['name']) + 20))
        print()

if __name__ == "__main__":
    main()