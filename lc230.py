# leetcode 230: kth smallest in a BST

from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    # Given the root of a binary search tree, and an integer k,
    # return the kth smallest value (1-indexed) of all the values of the nodes in the tree.
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        arr = []

        def inorder(node):
            if not node:
                return
            inorder(node.left)  # left
            arr.append(node.val)  # node
            inorder(node.right)  # right

        inorder(root)
        return arr[k - 1]


def main():
    # Helper to build a tree quickly
    class TreeNode:
        def __init__(self, val=0, left=None, right=None):
            self.val = val
            self.left = left
            self.right = right

    # Example 1: root = [3,1,4,null,2], k = 1 → Output = 1
    root1 = TreeNode(3)
    root1.left = TreeNode(1)
    root1.right = TreeNode(4)
    root1.left.right = TreeNode(2)

    # Example 2: root = [5,3,6,2,4,null,null,1], k = 3 → Output = 3
    root2 = TreeNode(5)
    root2.left = TreeNode(3)
    root2.right = TreeNode(6)
    root2.left.left = TreeNode(2)
    root2.left.right = TreeNode(4)
    root2.left.left.left = TreeNode(1)

    s = Solution()
    assert s.kthSmallest(root1, 1) == 1
    assert s.kthSmallest(root2, 3) == 3

    print("All tests passed!")


if __name__ == "__main__":
    main()
