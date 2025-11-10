# leetcode 3254: design key-value store with transactions (medium)

"""
Design and implement a simple **Key-Value Store** that supports basic operations and transactional behavior.

The key-value store should support the following methods:

### Basic Operations
- `set(key: str, value: Any) -> None`
  - Stores the given value under the given key.
- `get(key: str) -> Any`
  - Returns the value for the given key, or `None` if the key does not exist.
- `delete(key: str) -> None`
  - Deletes the given key from the store if it exists.

### Transactional Operations
- `begin() -> None`
  - Starts a new transaction. Transactions can be **nested**.
- `commit() -> None`
  - Commits all operations in the current transaction to its parent (or to the base store if top-level).
  - If there is no active transaction, do nothing.
- `rollback() -> None`
  - Discards all operations in the current transaction.
  - If there is no active transaction, do nothing.

### Behavior
- Each `begin()` creates a new isolated transaction layer.
- Changes inside a transaction should not affect the outer store until `commit()` is called.
- A `rollback()` undoes all changes in the current transaction scope only.
- Nested transactions are allowed.

---

Example 1:

Input:
store = KVStoreeStore()
store.set("x", 1)
store.begin()
store.set("x", 2)
print(store.get("x"))
store.rollback()
print(store.get("x"))

Output:
2
1

Explanation:
- `set("x", 1)` stores x=1 in the base store.
- Inside a transaction, `x` is temporarily changed to 2.
- `rollback()` discards the change, reverting to x=1.

---

Example 2:

Input:
store = KVStoreeStore()
store.set("a", 10)
store.begin()
store.set("a", 20)
store.begin()
store.set("a", 30)
print(store.get("a"))
store.rollback()
print(store.get("a"))
store.commit()
print(store.get("a"))

Output:
30
20
20

Explanation:
- Two nested transactions were opened.
- The inner transaction was rolled back, so `a` reverted to 20.
- The outer transaction was committed, keeping `a = 20`.

---

Constraints:
- All keys are strings.
- Values can be integers or strings.
- The number of operations will not exceed 10⁴.
- Transactions can be nested arbitrarily deep.
"""


class KVStore:

    def __init__(self):
        # stack of maps
        # each map holds the actions in that commit or layer
        self.transactions = [{}]

    def begin(self) -> None:
        # add a new layer
        self.transactions.append({})

    def set(self, key: str, value: str) -> None:
        if self.transactions:
            self.transactions[-1][key] = value

    def get(self, key: str) -> str | None:
        for i in range(len(self.transactions) - 1, -1, -1):
            if key in self.transactions[i]:
                return self.transactions[i][key]

        return None

    def rollback(self) -> bool:
        if len(self.transactions) > 1:
            self.transactions.pop()
            return True
        return False

    def commit(self) -> bool:
        # if there is more than 1 layer, commit
        # merges the topmost layer to the one directly below it
        if len(self.transactions) <= 1:
            return False

        # for each key-value pair in the topmost layer, add it
        # to the one under or update the value under if it
        # already exists there
        to_merge = self.transactions.pop()
        self.transactions[-1].update(to_merge)

        return True


if __name__ == "__main__":
    # Example 1
    store = KVStore()
    store.set("x", 1)
    store.begin()
    store.set("x", 2)
    assert store.get("x") == 2
    store.rollback()
    assert store.get("x") == 1

    # Example 2
    store = KVStore()
    store.set("a", 10)
    store.begin()
    store.set("a", 20)
    store.begin()
    store.set("a", 30)
    assert store.get("a") == 30
    store.rollback()
    assert store.get("a") == 20
    store.commit()
    assert store.get("a") == 20

    # Example 3: delete inside transaction
    store = KVStore()
    store.set("z", 5)
    store.begin()
    store.delete("z")
    assert store.get("z") is None
    store.rollback()
    assert store.get("z") == 5

    # Example 4: nested transactions and commits
    store = KVStore()
    store.set("k", "v1")
    store.begin()
    store.set("k", "v2")
    store.begin()
    store.set("k", "v3")
    store.commit()
    assert store.get("k") == "v3"
    store.rollback()
    assert store.get("k") == "v1"

    # Example 5: rollback without active transaction (no-op)
    store = KVStore()
    store.set("t", 100)
    store.rollback()  # no transaction active
    assert store.get("t") == 100

    # Example 6: commit without active transaction (no-op)
    store = KVStore()
    store.set("m", 1)
    store.commit()  # no transaction active
    assert store.get("m") == 1

    print("✅ All test cases passed!")
