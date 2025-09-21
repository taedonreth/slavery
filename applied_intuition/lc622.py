# leetcode 622: design circular queue (medium)

"""
simulate connection using %
[0, 1, 2, 3]
always move tail and insert at tail
start with head and tail at idx 0
"""
class MyCircularQueue:

    def __init__(self, k: int):
        self.max_size = k
        self.curr_size = 0
        self.q = [0] * self.max_size
        self.head = 0 # front of q
        self.tail = 0 # back of q
        
    def isFull(self) -> bool:
        return self.curr_size == self.max_size

    def isEmpty(self) -> bool:
        return self.curr_size == 0

# [0, 1, 2, 3]
    def enQueue(self, value: int) -> bool:
        # insert value value at index tail
        # increment tail for future operations
        # handle moving head if needed
        if self.isFull():
            return False
            
        self.q[self.tail] = value
        self.tail = (self.tail + 1) % self.max_size
        self.curr_size += 1
        
        return True


    def deQueue(self) -> bool:
        if self.isEmpty():
            return False

        self.head = (self.head + 1) % self.max_size
        self.curr_size -= 1
        return True

    def Front(self) -> int:
        return self.q[self.head] if not self.isEmpty() else -1
        
    def Rear(self) -> int:
        if self.isEmpty():
            return -1
        return self.q[(self.tail - 1 + self.max_size) % self.max_size]

        
        


# Your MyCircularQueue object will be instantiated and called as such:
# obj = MyCircularQueue(k)
# param_1 = obj.enQueue(value)
# param_2 = obj.deQueue()
# param_3 = obj.Front()
# param_4 = obj.Rear()
# param_5 = obj.isEmpty()
# param_6 = obj.isFull()