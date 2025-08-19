# lc1146.py


class SnapshotArray:
    # SnapshotArray(int length) initializes an array-like data structure with the given length. Initially, each element equals 0.
    def __init__(self, length: int):
        # keep a list of lists, where each list represents one index
        # each index list will hold tuples of format (snapid, value)
        # [[(x, y), (x, y)], [(w, e)], []]

        self.array = [[(-1, 0)] for _ in range(length)]
        self.curr_snap_id = 0

    # void set(index, val) sets the element at the given index to be equal to val
    def set(self, index: int, val: int) -> None:
        # append (curr snap id, val) to index's list (or overwrite if its the same)
        if self.array[index][-1][0] == self.curr_snap_id:
            self.array[index][-1] = (self.array[index][-1][0], val)
        else:
            self.array[index].append((self.curr_snap_id, val))

    # int snap() takes a snapshot of the array and returns the snap_id: the total number of times we called snap() minus 1.
    def snap(self) -> int:
        # increment snap_id and return it
        self.curr_snap_id += 1
        return self.curr_snap_id - 1

    # int get(index, snap_id) returns the value at the given index, at the time we took the snapshot with the given snap_id
    def get(self, index: int, snap_id: int) -> int:
        # binary search the index's list to find latest value = snap_id
        left = 0
        right = len(self.array[index]) - 1

        while left <= right:
            mid = (right + left) // 2
            if self.array[index][mid][0] == snap_id:
                return self.array[index][mid][1]
            elif self.array[index][mid][0] > snap_id:
                right = mid - 1
            else:
                left = mid + 1
        return self.array[index][right][1]


# Your SnapshotArray object will be instantiated and called as such:
# obj = SnapshotArray(length)
# obj.set(index,val)
# param_2 = obj.snap()
# param_3 = obj.get(index,snap_id)


def main():
    # Example from the problem description
    snapshotArr = SnapshotArray(3)  # set the length to be 3

    snapshotArr.set(0, 5)  # Set array[0] = 5
    snap_id0 = snapshotArr.snap()  # Take a snapshot, should return 0
    snapshotArr.set(0, 6)

    # Assertions from the example
    assert snap_id0 == 0

    # [[[-1, 0], [, 5]],[[-1, 0]],[[-1, 0]]]
    assert snapshotArr.get(0, 0) == 5

    print("All tests passed!")


if __name__ == "__main__":
    main()
