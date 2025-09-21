from collections import deque

"""
Design a hit counter which counts the number of hits received in the past 5 minutes (i.e., the past 300 seconds).

Your system should accept a timestamp parameter (in seconds granularity), and you may assume that calls are being made to the system in chronological order (i.e., timestamp is monotonically increasing). Several hits may arrive roughly at the same time.

Implement the HitCounter class:

HitCounter() Initializes the object of the hit counter system.
void hit(int timestamp) Records a hit that happened at timestamp (in seconds). Several hits may happen at the same timestamp.
int getHits(int timestamp) Returns the number of hits in the past 5 minutes from timestamp (i.e., the past 300 seconds).
 

Example 1:

Input
["HitCounter", "hit", "hit", "hit", "getHits", "hit", "getHits", "getHits"]
[[], [1], [2], [3], [4], [300], [300], [301]]
Output
[null, null, null, null, 3, null, 4, 3]

Explanation
HitCounter hitCounter = new HitCounter();
hitCounter.hit(1);       // hit at timestamp 1.
hitCounter.hit(2);       // hit at timestamp 2.
hitCounter.hit(3);       // hit at timestamp 3.
hitCounter.getHits(4);   // get hits at timestamp 4, return 3.
hitCounter.hit(300);     // hit at timestamp 300.
hitCounter.getHits(300); // get hits at timestamp 300, return 4.
hitCounter.getHits(301); // get hits at timestamp 301, return 3.
"""

class HitCounter:

    def __init__(self):
        self.q = deque()

    def hit(self, timestamp: int) -> None:
        if self.q and self.q[-1][0] == timestamp:
            self.q[-1] = (self.q[-1][0], self.q[-1][1] + 1)
        else:
            self.q.append((timestamp, 1))

    def getHits(self, timestamp: int) -> int:
        # [(1, 1), (2, 1), (3, 1), (4, 300)]
        # return the number of hits in the past 5 minutes from timestamp
        # pop any tuples that are outside the past 5 minutes, then add the counts of the rest (valid tuples)
        while self.q and timestamp - self.q[0][0] >= 300:
            self.q.popleft()
        return sum(count for _, count in self.q)

def main():
    # Create the hit counter object
    obj = HitCounter()

    # Run through the example from the problem
    obj.hit(1)    # hit at timestamp 1
    obj.hit(2)    # hit at timestamp 2
    obj.hit(3)    # hit at timestamp 3
    print(obj.getHits(4))    # expected 3

    obj.hit(300)  # hit at timestamp 300
    print(obj.getHits(300))  # expected 4
    print(obj.getHits(301))  # expected 3

if __name__ == "__main__":
    main()
