"""
Design a time-based key-value data structure that can store multiple values for the same key at different time stamps and retrieve the key's value at a certain timestamp.
"""


class TimeMap:
    # TimeMap() Initializes the object of the data structure.
    def __init__(self):
        # use a map -> {key: [("value", timestamp)]
        # multiple values can be mapped to the same key, but their timestamps will be in increasing
        # order
        self.map = {}

    # void set(String key, String value, int timestamp) Stores the key key with the value value at the given time timestamp.
    def set(self, key: str, value: str, timestamp: int) -> None:
        # {"foo": ("bar", 1), "foo": ("bar", 2),
        # {"foo": [("bar", 1), ("bar", 2), ("bar2", 4), ("bar", 5), ("bar", 9)]
        if key in self.map:
            self.map[key].append((value, timestamp))
        else:
            self.map[key] = [(value, timestamp)]

    # String get(String key, int timestamp) Returns a value such that set was called previously, with timestamp_prev <= timestamp.
    # If there are multiple such values, it returns the value associated with the largest timestamp_prev. If there are no values, it returns "".
    def get(self, key: str, timestamp: int) -> str:
        # edge case: if key doesnt exist or there are no values where timestamp_prev <= timestamp
        if (key not in self.map) or (timestamp < self.map[key][0][1]):
            return ""

        # binary search on timestamps to find largest timestamp <= timestamp
        res = ""
        left = 0
        right = len(self.map[key]) - 1
        while left <= right:
            mid = (right + left) // 2
            if self.map[key][mid][1] <= timestamp:
                res = self.map[key][mid][0]
                left = mid + 1
            else:
                right = mid - 1
        return res


def main():
    # Your TimeMap object will be instantiated and called as such:
    # obj = TimeMap()
    # obj.set(key,value,timestamp)
    # param_2 = obj.get(key,timestamp)

    obj = TimeMap()
    obj.set("foo", "bar", 1)

    # Example asserts from the problem description
    assert obj.get("foo", 1) == "bar"
    assert obj.get("foo", 3) == "bar"

    obj.set("foo", "bar2", 4)
    assert obj.get("foo", 4) == "bar2"
    assert obj.get("foo", 5) == "bar2"

    print("All tests passed!")


if __name__ == "__main__":
    main()


"""
Constraints:

1 <= key.length, value.length <= 100
key and value consist of lowercase English letters and digits.
1 <= timestamp <= 107
All the timestamps timestamp of set are strictly increasing.
At most 2 * 105 calls will be made to set and get.
"""
