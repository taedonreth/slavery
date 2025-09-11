# leetcode 100: same tree (easy)

from typing import Optional
from collections import deque


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(values):
    if not values:
        return None
    root = TreeNode(values[0])
    q = deque([root])
    i = 1
    while q and i < len(values):
        node = q.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            q.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            q.append(node.right)
        i += 1
    return root


class Solution:
    """
    Given the roots of two binary trees p and q, write a function to check if they are the same or not.
    Two binary trees are considered the same if they are structurally identical, and the nodes have the same value.
    """

    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        """
        at any given node (could be null), there are 4 options
            they are both null:
                good
            they are both nodes and have the same value:
                good
            they are both nodes and have diff values:
                bad
            one is node and one isnt
                bad

        go down both trees and make the comparisons above
        """
        if not q and not p:
            return True
        if (not p and q) or (p and not q) or (p.val != q.val):
            return False

        left = self.isSameTree(p.left, q.left)
        right = self.isSameTree(p.right, q.right)

        return left and right


def main():
    s = Solution()

    # Example 1
    p = build_tree([1, 2, 3])
    q = build_tree([1, 2, 3])
    expected = True
    assert s.isSameTree(p, q) == expected

    # Example 2
    p = build_tree([1, 2])
    q = build_tree([1, None, 2])
    expected = False
    assert s.isSameTree(p, q) == expected

    # Example 3
    p = build_tree([1, 2, 1])
    q = build_tree([1, 1, 2])
    expected = False
    assert s.isSameTree(p, q) == expected

    print("All test cases passed!")


if __name__ == "__main__":
    main()
