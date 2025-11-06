"""
max path sum between any 2 nodes 3 different subproblems:
    1. started from root to node
    2. between any 2 leaf nodes
    3. between any 2 nodes.
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class MaxPathSum:
    # -----------------------------
    # 1️⃣ Maximum path sum from root to any node
    # -----------------------------
    @staticmethod
    def maxRootToNode(root):
        def dfs(node):
            if not node:
                return float("-inf")  # for non-existent node
            if not node.left and not node.right:
                return node.val
            left = dfs(node.left)
            right = dfs(node.right)
            return node.val + max(left, right)

        return dfs(root)

    # -----------------------------
    # 2️⃣ Maximum path sum between any two leaf nodes
    # -----------------------------
    @staticmethod
    def maxLeafToLeaf(root):
        maxSum = float("-inf")

        def dfs(node):
            nonlocal maxSum
            if not node:
                return float("-inf")  # non-leaf path

            if not node.left and not node.right:
                return node.val  # leaf node

            left = dfs(node.left)
            right = dfs(node.right)

            # if node has both children, consider path through node
            if node.left and node.right:
                maxSum = max(maxSum, left + node.val + right)
                return node.val + max(left, right)

            # if only one child exists, propagate the path sum
            return node.val + (left if node.left else right)

        dfs(root)
        return maxSum

    # -----------------------------
    # 3️⃣ Maximum path sum between any two nodes (general)
    # -----------------------------
    @staticmethod
    def maxAnyNodeToAnyNode(root):
        maxSum = float("-inf")

        def dfs(node):
            nonlocal maxSum
            if not node:
                return 0
            left = max(dfs(node.left), 0)  # ignore negative path
            right = max(dfs(node.right), 0)

            # max path THROUGH this node
            maxSum = max(maxSum, node.val + left + right)

            # max path ending at this node (for parent)
            return node.val + max(left, right)

        dfs(root)
        return maxSum
