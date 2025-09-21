from typing import List


class Solution:
    def threeSumMulti(self, arr: List[int], target: int) -> int:
        """
        LeetCode 923: 3Sum With Multiplicity

        Given an integer array arr, and an integer target, return the number of
        tuples i, j, k such that i < j < k and arr[i] + arr[j] + arr[k] == target.

        Since the answer can be very large, return it modulo 10^9 + 7.

        Example 1:
        Input: arr = [1,1,2,2,3,3,4,4,5,5], target = 8
        Output: 20
        Explanation:
        Enumerating by the values (arr[i], arr[j], arr[k]):
        (1, 2, 5) occurs 8 times;
        (1, 3, 4) occurs 8 times;
        (2, 2, 4) occurs 2 times;
        (2, 3, 3) occurs 2 times.

        Example 2:
        Input: arr = [1,1,2,2,2,2], target = 5
        Output: 12
        Explanation:
        arr[i] = 1, arr[j] = arr[k] = 2 occurs 12 times:
        We choose one 1 from [1,1] in 2 ways,
        and two 2s from [2,2,2,2] in 6 ways.

        Example 3:
        Input: arr = [2,1,3], target = 6
        Output: 1
        Explanation: We have one choice: arr[0] + arr[1] + arr[2] = 2 + 1 + 3 = 6.

        Constraints:
        3 <= arr.length <= 3000
        0 <= arr[i] <= 100
        0 <= target <= 300

        Args:
            arr: The input integer array.
            target: The target integer sum.

        Returns:
            The number of valid tuples modulo 10^9 + 7.
        """
        MOD = 10**9 + 7
        result = 0

        # --- YOUR CODE GOES HERE ---

        # --- END OF YOUR CODE ---

        return result % MOD


def main():
    """Main function to run test cases."""
    solver = Solution()

    test_cases = [
        {
            "name": "Example 1",
            "input": {"arr": [1, 1, 2, 2, 3, 3, 4, 4, 5, 5], "target": 8},
            "expected": 20,
        },
        {
            "name": "Example 2",
            "input": {"arr": [1, 1, 2, 2, 2, 2], "target": 5},
            "expected": 12,
        },
        {"name": "Example 3", "input": {"arr": [2, 1, 3], "target": 6}, "expected": 1},
        {
            "name": "All zeros",
            "input": {"arr": [0, 0, 0, 0], "target": 0},
            "expected": 4,
        },
        {
            "name": "No valid triplets",
            "input": {"arr": [1, 2, 3], "target": 10},
            "expected": 0,
        },
        {
            "name": "Minimum size array",
            "input": {"arr": [1, 2, 3], "target": 6},
            "expected": 1,
        },
        {
            "name": "All same elements",
            "input": {"arr": [2, 2, 2, 2, 2], "target": 6},
            "expected": 10,
        },
    ]

    print("🧪 Running test cases for 3Sum With Multiplicity...\n")

    for i, test_case in enumerate(test_cases):
        input_arr = test_case["input"]["arr"].copy()  # Copy to avoid modifying original
        input_target = test_case["input"]["target"]
        expected_output = test_case["expected"]

        actual_output = solver.threeSumMulti(input_arr, input_target)

        print(f"--- Test Case {i+1}: {test_case['name']} ---")
        print(f"Input: arr={test_case['input']['arr']}, target={input_target}")
        print(f"Expected: {expected_output}")
        print(f"Actual:   {actual_output}")

        if actual_output == expected_output:
            print("✅ PASS")
        else:
            print("❌ FAIL")
        print("-" * 50)
        print()


if __name__ == "__main__":
    main()

