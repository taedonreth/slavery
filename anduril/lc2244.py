# leetcode 2244: minimum rounds to complete all tasks (medium)

"""
You are given a 0-indexed integer array tasks, where tasks[i] represents the difficulty level of a task. 
In each round, you can complete either 2 or 3 tasks of the same difficulty level.

Return the minimum rounds required to complete all the tasks, or -1 if it is not possible to complete all the tasks.

 

Example 1:

Input: tasks = [2,2,3,3,2,4,4,4,4,4]
Output: 4
Explanation: To complete all the tasks, a possible plan is:
- In the first round, you complete 3 tasks of difficulty level 2. 
- In the second round, you complete 2 tasks of difficulty level 3. 
- In the third round, you complete 3 tasks of difficulty level 4. 
- In the fourth round, you complete 2 tasks of difficulty level 4.  
It can be shown that all the tasks cannot be completed in fewer than 4 rounds, so the answer is 4.
Example 2:

Input: tasks = [2,3,3]
Output: -1
Explanation: There is only 1 task of difficulty level 2, but in each round, you can only complete either 2 or 3 tasks of the same difficulty level. Hence, you cannot complete all the tasks, and the answer is -1.
 

Constraints:

1 <= tasks.length <= 105
1 <= tasks[i] <= 109
"""

from typing import List
from collections import Counter

class Solution:
    def minimumRounds(self, tasks: List[int]) -> int:
        """
        initialize counter for tasks

        min rounds = 0
        go through counter
            if 1:
                return -1
            # how do i find out how many rounds to add
            # least # of 2's and 3's to add up to it
            min_rounds += num / 
        """

        count = Counter(tasks)
        min_rounds = 0
        for key, val in count.items():
            if val == 1:
                return -1

            quotient, remainder = val // 3, val % 3
            if remainder == 0:
                min_rounds += quotient
            else:
                min_rounds += quotient + 1

        return min_rounds
        

if __name__ == "__main__":
    sol = Solution()

    # Example tests
    assert sol.minimumRounds([2,2,3,3,2,4,4,4,4,4]) == 4
    assert sol.minimumRounds([2,3,3]) == -1

    # Additional edge cases
    # Single task → impossible
    assert sol.minimumRounds([5]) == -1
    
    # Exactly 2 of a difficulty
    assert sol.minimumRounds([7,7]) == 1

    # Exactly 3 of a difficulty
    assert sol.minimumRounds([9,9,9]) == 1

    # Mixed groups
    assert sol.minimumRounds([1,1,1,1]) == 2   # 4 → 2+2

    # Multiple difficulties
    assert sol.minimumRounds([1,1,2,2,2,3,3,3,3]) == 4  # 2 rounds for 1's, 1 round for 2's, 2 rounds for 3's

    print("All tests passed!")