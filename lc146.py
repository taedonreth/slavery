# leetcode 146: LRU cache (medium)


# make class for doubly linked list
class Node:
    def __init__(self, key: int, value: int):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None


"""
dict = {key: pointer to node}
linked list: key, value <-> key, value <-> key, value
"""


class LRUCache:
    """
    init:
        dict
        linked list
        max = capacity
        current size = 0
    """

    def __init__(self, capacity: int):
        self.cache = {}
        self.capacity = capacity
        self.dummyhead = Node(0, 0)
        self.dummytail = Node(0, 0)

        self.dummyhead.next = self.dummytail
        self.dummytail.prev = self.dummyhead

    """
    get:
        if in dict
            move to front
            return val
        else
            return -1
    """

    def get(self, key: int) -> int:
        if key in self.cache:
            self._move_to_front(self.cache[key])
            return self.cache[key].value

        return -1

    """
    put:
        if key in dict
            update value
            move to front
            return
        add to dict
        increase curr size
        if currrent size > max
            delete from dict
            delete from tail
            
        return
    """

    def put(self, key: int, value: int) -> None:
        # case 1: key is in there
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._move_to_front(node)
            return

        # case 2: key does not exist yet, add it to dict and ll and check LRU property
        newNode = Node(key, value)
        self._add_to_front(newNode)
        self.cache[key] = newNode
        if self.capacity - len(self.cache) < 0:
            lru = self.dummyhead.next
            self._remove_node(lru)
            del self.cache[lru.key]

    def _move_to_front(self, node: Node) -> None:

        # already at the front
        if self.dummytail.prev == node:
            return

        # not at front yet:
        # remove node
        # move right behind tail node
        self._remove_node(node)
        self._add_to_front(node)

    def _add_to_front(self, node: Node) -> None:
        node.next = self.dummytail
        node.prev = self.dummytail.prev
        self.dummytail.prev.next = node
        self.dummytail.prev = node

    def _remove_node(self, node: Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev


# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)


def main():
    # Example 1: LRUCache with capacity 2
    lru_cache = LRUCache(2)

    lru_cache.put(1, 1)  # cache is {1=1}
    lru_cache.put(2, 2)  # cache is {1=1, 2=2}

    result1 = lru_cache.get(1)  # return 1
    assert result1 == 1, f"Expected 1, got {result1}"

    lru_cache.put(3, 3)  # LRU key was 2, evicts key 2, cache is {1=1, 3=3}

    result2 = lru_cache.get(2)  # returns -1 (not found)
    assert result2 == -1, f"Expected -1, got {result2}"

    lru_cache.put(4, 4)  # LRU key was 1, evicts key 1, cache is {4=4, 3=3}

    result3 = lru_cache.get(1)  # return -1 (not found)
    assert result3 == -1, f"Expected -1, got {result3}"

    result4 = lru_cache.get(3)  # return 3
    assert result4 == 3, f"Expected 3, got {result4}"

    result5 = lru_cache.get(4)  # return 4
    assert result5 == 4, f"Expected 4, got {result5}"

    print("All tests passed!")


if __name__ == "__main__":
    main()
