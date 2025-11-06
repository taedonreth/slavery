# leetcode 146: lru cache (medium)

"""
cache
dictionary where key = int and value = node with that key and value
node has next, prev, key, and value

dummy nodes for head a tail
right side (tail) = lru
head = mru

helper function
    move to front (mru)
    evict (delete lru)
"""

class Node:
    def __init__(self, key=-1, val=-1) -> None:
        self.prev = None
        self.next = None
        self.key = key
        self.val = val

class LRUCache:
    def __init__(self, capacity: int):
        self.cache = {}
        self.capacity = capacity

        self.dummyhead = Node()
        self.dummytail = Node()
        self.dummyhead.next = self.dummytail
        self.dummytail.prev = self.dummyhead

    def _remove(self, node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _move_to_front(self, node) -> None:
        self._remove(node)
        self._add_to_front(node)

    def _evict(self) -> None:
        del self.cache[self.dummytail.prev.key]
        self._remove(self.dummytail.prev)

    def _add_to_front(self, node) -> None:
        node.prev = self.dummyhead
        node.next = self.dummyhead.next
        self.dummyhead.next.prev = node
        self.dummyhead.next = node

    def get(self, key: int) -> int:
        """
        if key exists, return it
        move node to front
        """
        if key in self.cache:
            self._move_to_front(self.cache[key])
            return self.cache[key].val

        return -1
        

    def put(self, key: int, value: int) -> None:
        """
        if exist
            update value and move to front
        else
            if cache is full
                evict lru
                add key value pair to cache (node)
            else
                add key value pair to cache
                move to front
        """

        if key in self.cache:
            self.cache[key].val = value
            self._move_to_front(self.cache[key])
        else:
            if len(self.cache) == self.capacity:
                self._evict()
            new_node = Node(key=key, val=value)
            self.cache[key] = new_node
            self._add_to_front(new_node)
        

        


# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)

"""

Concurrency Trade-offs

Coarse-grained locking (one global lock): Simplest approach but serializes all operations - 
only one thread can access the cache at a time, creating a throughput bottleneck under high load
Fine-grained locking (separate locks for dictionary vs linked list): Improves concurrency by 
allowing some operations to overlap, but introduces deadlock risk and significant implementation complexity
Sharding (split into N independent caches): Best practical solution - with 16 shards you can 
handle ~16x more concurrent operations since operations on different shards don't block each other; 
this is why production systems like Redis and Memcached use this approach
Lock-free data structures: Highest theoretical performance using atomic operations, but extremely 
difficult to implement correctly and harder to debug
Key insight: Every get() operation modifies state (moves node to front), so even read-heavy workloads
 have write contention, making read-write locks less effective than in typical scenarios

Thread Safety Issues

Double eviction bug: Two threads both see cache at capacity, both call _evict(), resulting in two items 
removed instead of one - cache now has capacity-1 items
Lost updates: Two concurrent put() operations with the same key can cause one value to be lost when both
 threads update the node simultaneously
Linked list corruption: Thread 1 modifies head.next while Thread 2 reads it, resulting in broken pointers, 
infinite loops during traversal, or nodes becoming unreachable
Dictionary-list inconsistency: Node exists in self.cache dictionary but not in the linked list (or vice versa)
due to interrupted operations, breaking the fundamental invariant
Race in move-to-front: Thread 1 removes node from position A while Thread 2 tries to traverse through it, 
causing null pointer dereference or skipped nodes
Solution requires: Atomic operations that guarantee both the dictionary and linked list are updated together - 
typically achieved with locks that protect the entire operation from start to finish
"""