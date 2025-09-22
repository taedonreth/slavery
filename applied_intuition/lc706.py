# leetcode 706: design hashmap (easy)

"""
list, where each index is a bucket
bucket is a linked list of nodes
each node holds a key, value, and next pointer to the next node
hash the key into the right bucket (right index of the list)
"""
class ListNode:
    def __init__(self, key = -1, value = -1, next = None):
        self.key = key
        self.val = value
        self.next = next

class MyHashMap:

    def __init__(self):
        self.map = [ListNode() for i in range(2069)]
        
    def hash(self, val):
        return val % 2069

    def put(self, key: int, value: int) -> None:
        # iterate through the right bucket
        # if key exists, update it
        # otherwise add to end
        curr = self.map[self.hash(key)]
        while curr.next:
            if curr.next.key == key:
                curr.next.val = value
                return

            curr = curr.next
        
        curr.next = ListNode(key, value)

    def get(self, key: int) -> int:
        # iterate through the right bucket
        # if key exists, return it
        # otherwise return -1
        curr = self.map[self.hash(key)]
        while curr:
            if curr.key == key:
                return curr.val

            curr = curr.next
        
        return -1
        

    def remove(self, key: int) -> None:
        # iterate through the right bucket
        # if we find the key, update pointers to delete the node
        # key is guaranteed to exist
        curr = self.map[self.hash(key)]
        while curr.next:
            if curr.next.key == key:
                curr.next = curr.next.next
                return

            curr = curr.next


# Your MyHashMap object will be instantiated and called as such:
# obj = MyHashMap()
# obj.put(key,value)
# param_2 = obj.get(key)
# obj.remove(key)