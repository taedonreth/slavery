# design functionality of deque

"""
Design a data structure that implements the functionality of a deque 
(push_front, push_back, pop_front, pop_back), 
and a print function that prints the elements in the deque sequentially.
"""

"""
doubly linked list?
head pointer allows for O(1) operations at the front of the list
tail pointer allows for O(1) operations at the back of the list
we can have dummy tail and dummy head so we don't need to deal with null ptrs
"""

class Node:
    def __init__(self, val: int = float('inf'), prev: "Node | None" = None, next: "Node | None" = None) -> None:
        self.val = val
        self.prev = prev
        self.next = next

class Deque():
    def __init__(self) -> None:
        self.dummyhead = Node()
        self.dummytail = Node()
        self.dummyhead.next = self.dummytail
        self.dummytail.prev = self.dummyhead

    def push_front(self, val: int) -> None:
        # insert between dummyhead and dummyhead.next
        to_insert = Node(val, self.dummyhead, self.dummyhead.next)
        self.dummyhead.next.prev = to_insert
        self.dummyhead.next = to_insert
        
    def push_back(self, val:int) -> None:
        # insert between dummytail.prev and dummytail
        to_insert = Node(val, self.dummytail.prev, self.dummytail)
        self.dummytail.prev.next = to_insert
        self.dummytail.prev = to_insert

    def pop_front(self) -> bool:
        # Check if deque is empty
        if self.dummyhead.next == self.dummytail:
            return False
        
        # Delete dummyhead.next
        to_delete = self.dummyhead.next
        self.dummyhead.next = to_delete.next
        to_delete.next.prev = self.dummyhead
        
        # Disconnect pointers (good practice, not strictly necessary in Python)
        to_delete.prev = None
        to_delete.next = None
        return True

    def pop_back(self) -> bool:
        # Check if deque is empty
        if self.dummytail.prev == self.dummyhead:
            return False
        
        # Delete dummytail.prev
        to_delete = self.dummytail.prev
        self.dummytail.prev = to_delete.prev
        to_delete.prev.next = self.dummytail
        
        # Disconnect pointers (good practice, not strictly necessary in Python)
        to_delete.prev = None
        to_delete.next = None
        return True

    def print(self) -> None:
        result = []
        curr = self.dummyhead.next
        while curr != self.dummytail:
            result.append(curr.val)
            curr = curr.next
        print(result)


if __name__ == "__main__":
    q = Deque()
    q.print()
    q.pop_back()
    
    # Test push_front
    q.push_front(5)
    q.print()
    q.push_front(3)
    q.print()
    
    # Test push_back
    q.push_back(7)
    q.print()
    
    # Test pop_front
    q.pop_front()
    q.print()
    
    # Test pop_back
    q.pop_back()
    q.print()
    
    # Test pop all elements
    q.pop_front()
    q.print()