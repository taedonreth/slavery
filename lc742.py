from collections import defaultdict, deque
from typing import List, Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


"""
Given the root of a binary tree where every node has a unique value and a target integer k, return the value of the nearest leaf node to the target k in the tree.
Nearest to a leaf means the least number of edges traveled on the binary tree to reach any leaf of the tree. Also, a node is called a leaf if it has no children.
"""


class Solution:
    def findClosestLeaf(self, root: Optional[TreeNode], k: int) -> int:
        # dfs to create undirected graph of the tree, where each node can have <= 3 edges
        # nodes with <= 1 edge are leaves
        # bfs starting at k on our graph to find closest root to k
        graph = defaultdict(list)
        target = None

        def dfs(node, parent=None):
            nonlocal target
            if node:
                graph[node].append(parent)
                graph[parent].append(node)

                if node.val == k:
                    target = node

                dfs(node.left, node)
                dfs(node.right, node)

        # build graph
        dfs(root)

        # intitialize queue at target node (value k)
        # [1]
        queue = deque([target])
        seen = set(queue)

        # bfs starting at node to find the closest leaf
        while queue:
            curr = queue.popleft()
            if curr:
                if len(graph[curr]) <= 1:
                    return curr.val
                for neighbor in graph[curr]:
                    if neighbor not in seen:
                        seen.add(neighbor)
                        queue.append(neighbor)


def main():
    sol = Solution()

    # Example 1:
    # root = [1,3,2], k = 1
    root1 = TreeNode(1)
    root1.left = TreeNode(3)
    root1.right = TreeNode(2)
    assert sol.findClosestLeaf(root1, 1) in [2, 3]  # both valid

    # Example 2:
    # root = [1], k = 1
    root2 = TreeNode(1)
    assert sol.findClosestLeaf(root2, 1) == 1

    # Example 3:
    # root = [1,2,3,4,null,null,null,5,null,6], k = 2
    root3 = TreeNode(1)
    root3.left = TreeNode(2)
    root3.right = TreeNode(3)
    root3.left.left = TreeNode(4)
    root3.left.left.left = TreeNode(5)
    root3.left.left.left.right = TreeNode(6)
    assert sol.findClosestLeaf(root3, 2) == 3

    print("All tests passed!")


if __name__ == "__main__":
    main()
