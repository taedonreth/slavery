# leetcode 138: copy list with random pointer (medium)

from typing import Optional


# Definition for a Node.
class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random

class Solution:
    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':

        if not head:
            return None
            
        copy_map = {}

        curr = head
        while curr:
            copy_map[curr] = Node(curr.val)
            curr = curr.next

        curr = head
        while curr:
            copy_map[curr].next = copy_map.get(curr.next)
            copy_map[curr].random = copy_map.get(curr.random)
            curr = curr.next

        return copy_map[head]
