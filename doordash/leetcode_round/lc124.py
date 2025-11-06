# leetcode 124: binary tree maximum path sum (hard)

"""
A path in a binary tree is a sequence of nodes where each pair of adjacent nodes in the sequence has an edge connecting them. A node can only appear in the sequence at most once. Note that the path does not need to pass through the root.

The path sum of a path is the sum of the node's values in the path.

Given the root of a binary tree, return the maximum path sum of any non-empty path.
"""

from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        maxPath = -199999

        # post order traversal of subtree rooted at `node`
        def gainFromSubtree(node: Optional[TreeNode]) -> int:
            nonlocal maxPath

            if not node:
                return 0

            # add the gain from the left subtree. Note that if the
            # gain is negative, we can ignore it, or count it as 0.
            # This is the reason we use `max` here.
            gainFromLeft = max(gainFromSubtree(node.left), 0)

            # add the gain / path sum from right subtree. 0 if negative
            gainFromRight = max(gainFromSubtree(node.right), 0)

            # if left or right gain are negative, they are counted
            # as 0, so this statement takes care of all four scenarios
            maxPath = max(maxPath, gainFromLeft + gainFromRight + node.val)

            # return the max sum for a path starting at the root of subtree
            return max(gainFromLeft + node.val, gainFromRight + node.val)

        gainFromSubtree(root)
        return maxPath
