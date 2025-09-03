class Solution:
    """
    Given an unsorted integer array nums. Return the smallest positive integer that is not present in nums.
    You must implement an algorithm that runs in O(n) time and uses O(1) auxiliary space.
    """

    def firstMissingPositive(self, nums: List[int]) -> int:
        pass


def main():
    sol = Solution()

    # Example cases
    assert sol.firstMissingPositive([1, 2, 0]) == 3
    assert sol.firstMissingPositive([3, 4, -1, 1]) == 2
    assert sol.firstMissingPositive([7, 8, 9, 11, 12]) == 1

    # Extra cases
    assert sol.firstMissingPositive([1, 2, 3]) == 4  # all consecutive → next one
    assert sol.firstMissingPositive([0]) == 1  # single non-positive
    assert sol.firstMissingPositive([-5, -10, -1]) == 1  # all negatives
    assert sol.firstMissingPositive([2, 2, 2, 2]) == 1  # duplicate 2s
    assert sol.firstMissingPositive([1]) == 2  # smallest case, already has 1
    assert sol.firstMissingPositive([2]) == 1  # smallest case, missing 1

    print("All tests passed!")


if __name__ == "__main__":
    main()
