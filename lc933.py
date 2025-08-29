# leetcode 933: number of recent calls (easy)

"""
You have a RecentCounter class which counts the number of recent requests within a certain time frame.

Implement the RecentCounter class:

RecentCounter() Initializes the counter with zero recent requests.
int ping(int t) Adds a new request at time t, where t represents some time in milliseconds, and returns the number of requests that has happened in the past 3000 milliseconds (including the new request). Specifically, return the number of requests that have happened in the inclusive range [t - 3000, t].
It is guaranteed that every call to ping uses a strictly larger value of t than the previous call.


"""


class RecentCounter:
    """
    similar to hit counter?
    cant have the same ping in the same time
    just use an array?
    ping:
        append t to the array
        while arr[0] < t-3000:
            pop arr[0]
        return array.length
    """

    def __init__(self):
        self.counter = []
        self.size = 0

    def ping(self, t: int) -> int:
        self.counter.append(t)
        self.size += 1

        while self.counter and self.counter[0] < (t - 3000):
            self.counter.pop(0)
            self.size -= 1

        return self.size


# Your RecentCounter object will be instantiated and called as such:
# obj = RecentCounter()
# param_1 = obj.ping(t)


def main():

    # Example 1
    recentCounter = RecentCounter()
    assert recentCounter.ping(1) == 1
    assert recentCounter.ping(100) == 2
    assert recentCounter.ping(3001) == 3
    assert recentCounter.ping(3002) == 3

    print("All test cases passed!")


if __name__ == "__main__":
    main()
