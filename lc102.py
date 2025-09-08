# leetcode 102: binary tree level order traversal (medium)
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    # Given the root of a binary tree, return the level order traversal of its nodes' values. (i.e., from left to right, level by level).
    def levelOrder(self, root):
        """
        bfs
        """
        res = []

        # edge case: no nodes
        if not root:
            return []

        q = deque()
        q.append(root)

        while q:
            level_size = len(q)
            level = []
            for i in range(level_size):
                curr_node = q.popleft()
                level.append(curr_node.val)

                if curr_node.left:
                    q.append(curr_node.left)
                if curr_node.right:
                    q.append(curr_node.right)

            res.append(level)

        return res


def main():
    # helper to build tree from list (LeetCode style)
    from collections import deque

    def build_tree(values):
        if not values:
            return None
        root = TreeNode(values[0])
        queue = deque([root])
        i = 1
        while queue and i < len(values):
            node = queue.popleft()
            if i < len(values) and values[i] is not None:
                node.left = TreeNode(values[i])
                queue.append(node.left)
            i += 1
            if i < len(values) and values[i] is not None:
                node.right = TreeNode(values[i])
                queue.append(node.right)
            i += 1
        return root

    sol = Solution()

    # Example 1
    root = build_tree([3, 9, 20, None, None, 15, 7])
    assert sol.levelOrder(root) == [[3], [9, 20], [15, 7]]

    # Example 2
    root = build_tree([1])
    assert sol.levelOrder(root) == [[1]]

    # Example 3
    root = build_tree([])
    assert sol.levelOrder(root) == []

    print("All tests passed!")


if __name__ == "__main__":
    main()
