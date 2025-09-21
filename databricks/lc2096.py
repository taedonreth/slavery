from collections import deque
from typing import List, Optional

"""
You are given the root of a binary tree with n nodes. Each node is uniquely assigned a value from 1 to n. You are also given an integer startValue representing the value of the start node s, and a different integer destValue representing the value of the destination node t.

Find the shortest path starting from node s and ending at node t. Generate step-by-step directions of such path as a string consisting of only the uppercase letters 'L', 'R', and 'U'. Each letter indicates a specific direction:

'L' means to go from a node to its left child node.
'R' means to go from a node to its right child node.
'U' means to go from a node to its parent node.
Return the step-by-step directions of the shortest path from node s to node t.
"""


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def getDirections(
        self, root: Optional[TreeNode], startValue: int, destValue: int
    ) -> str:
        """
        high level:
            1. find root -> start
            2. find root -> destination
            3. find longest common prefix between the two paths above
            4. reverse direction of root to start so all 'D' turn into 'U'
        """

        # define dfs function to get path, given a starting point and a target
        # base case: if node is None → fail
        # If node.val == target → success, stop searching
        # Otherwise:
        #   try left: add "L", recurse. If success, return otherwise pop
        #   try right: add "R", recurse. If success, return otherwise pop
        def dfs(node: Optional[TreeNode], target: int, arr: List[str]) -> bool:
            if not node:
                return False
            if node.val == target:
                return True

            # try left
            arr.append("L")
            if dfs(node.left, target, arr):
                return True
            arr.pop()

            # try right
            arr.append("R")
            if dfs(node.right, target, arr):
                return True
            arr.pop()

            return False

        # both paths will be an array
        root_to_start, root_to_destination = [], []
        dfs(root, startValue, root_to_start)
        dfs(root, destValue, root_to_destination)

        # find index of longest common prefix
        i = 0
        while (
            i < min(len(root_to_start), len(root_to_destination))
            and root_to_start[i] == root_to_destination[i]
        ):
            i += 1

        # splice out root -> lca, turn direction into start -> lca
        lca_to_start = ["U"] * len(root_to_start[i:])
        lca_to_destination = root_to_destination[i:]

        combined_list = lca_to_start + lca_to_destination
        return "".join(combined_list)


def build_tree(values):
    """
    Build a binary tree from a list of values given in level-order.
    None represents a missing node.
    """
    if not values:
        return None

    root = TreeNode(values[0])
    queue = deque([root])
    i = 1

    while queue and i < len(values):
        node = queue.popleft()

        # Left child
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1

        # Right child
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1

    return root


def main():
    sol = Solution()

    # Example 1
    root = build_tree([5, 1, 2, 3, None, 6, 4])
    assert sol.getDirections(root, 3, 6) == "UURL"

    # Example 2
    root = build_tree([2, 1])
    assert sol.getDirections(root, 2, 1) == "L"

    print("All tests passed!")


if __name__ == "__main__":
    main()
