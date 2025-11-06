"""
Design a data structure class that supports two primary operations: increase_one(element) 
which increments the count of a given element by one, and topk(k) which returns the k 
elements with the highest counts; discuss multiple approaches to implement this efficiently, 
starting with naive solutions and progressively optimizing through different data structure 
combinations; explore trade-offs between using a hash table with a max-heap (where the hash 
table stores element counts and the heap maintains the top k elements), versus using a hash 
table with a doubly-linked list sorted by frequency (similar to LFU cache design), analyzing 
the time complexity of each operation under both approaches; discuss challenges such as 
maintaining heap consistency when counts change, efficiently updating the linked list 
ordering when frequencies are incremented, handling ties when multiple elements have the 
same count, and optimizing for scenarios where increase_one is called much more frequently 
than topk or vice versa; explain how your design would scale to handle millions of unique 
elements and high-frequency operations, and compare your solution to LeetCode problems like 
'Top K Frequent Elements' and 'LFU Cache' in terms of similar patterns and data structure techniques.
"""

from collections import defaultdict

class Node:
    """A node in a doubly-linked list."""
    def __init__(self, element):
        self.element = element
        self.prev = None
        self.next = None

class DoublyLinkedList:
    """A simple doubly-linked list implementation."""
    def __init__(self):
        # Sentinel nodes simplify insertion and removal logic
        self.head = Node(None)
        self.tail = Node(None)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def add_to_front(self, node):
        """Adds a node to the front of the list in O(1)."""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node
        self.size += 1

    def remove_node(self, node):
        """Removes a given node from the list in O(1)."""
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1
    
    def is_empty(self):
        """Checks if the list is empty."""
        return self.size == 0

# --- Main Data Structure Class ---

class TopKTracker:
    def __init__(self):
        self.element_counts = {}  # element -> count
        self.element_nodes = {}   # element -> Node
        self.frequency_lists = defaultdict(DoublyLinkedList) # count -> DLL of elements
        self.max_frequency = 0

    def increase_one(self, element):
        """Increments the count of an element in O(1) time."""
        # 1. Get the element's current count
        old_count = self.element_counts.get(element, 0)
        new_count = old_count + 1
        
        # 2. If the element already exists, remove it from its old frequency list.
        # This is O(1) thanks to the element_nodes map.
        if old_count > 0:
            node_to_move = self.element_nodes[element]
            old_list = self.frequency_lists[old_count]
            old_list.remove_node(node_to_move)
            # Clean up the frequency_lists map if a list becomes empty
            if old_list.is_empty():
                del self.frequency_lists[old_count]

        # 3. Update the element's count and add it to the new frequency list.
        self.element_counts[element] = new_count
        new_node = Node(element)
        self.element_nodes[element] = new_node
        self.frequency_lists[new_count].add_to_front(new_node)
        
        # 4. Update the maximum frequency tracker
        if new_count > self.max_frequency:
            self.max_frequency = new_count

    def topk(self, k):
        """Returns the k most frequent elements in O(k) time."""
        result = []
        # Iterate downwards from the highest frequency seen so far
        for freq in range(self.max_frequency, 0, -1):
            if freq in self.frequency_lists:
                current_list = self.frequency_lists[freq]
                node = current_list.head.next
                # Traverse the list for this frequency
                while node != current_list.tail:
                    result.append(node.element)
                    if len(result) == k:
                        return result
                    node = node.next
        return result
