# bloomberg key value store problem

"""
You are tasked with designing and implementing an in-memory key-value store that supports fully nested 
transactions, driven by a sequence of string commands. Your store must handle the following operations: 
SET key value (which sets a key within the current transaction), GET key (which retrieves a value by 
searching from the innermost transaction outwards), BEGIN (which starts a new, nested transaction scope), 
ROLLBACK (which discards all changes in the current scope), and COMMIT (which makes the changes of the 
current scope permanent to its immediate parent scope). The core challenge lies in managing the state of 
these embedded transactions correctly; for instance, a COMMIT should only merge changes one level up the 
transaction stack, not to the global state, unless it's the outermost transaction. After detailing your data 
structure choice, likely a stack-based approach, and implementing the logic to handle these operations, 
discuss how your design would be integrated as a transactional layer on top of a persistent, global database, 
specifically considering how the final, top-level COMMIT would interact with this global store and what 
concurrency issues might arise.
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

    # Test basic SET and GET
    store = KVStore()
    store.set("tom", "4")
    assert store.get("tom") == "4", "Basic set/get failed"
    assert store.get("nonexistent") is None, "Get nonexistent key should return None"
    
    # Test transactions with BEGIN and COMMIT
    store.set("a", "1")
    store.begin()
    store.set("b", "2")
    assert store.get("a") == "1", "Should see parent transaction values"
    assert store.get("b") == "2", "Should see current transaction values"
    assert store.commit(), "Commit should succeed when in a transaction"
    assert store.get("a") == "1", "Value 'a' should persist after commit"
    assert store.get("b") == "2", "Value 'b' should persist after commit"
    
    # Test ROLLBACK
    store.begin()
    store.set("c", "3")
    assert store.get("c") == "3", "Should see value in transaction"
    assert store.rollback(), "Rollback should succeed when in a transaction"
    assert store.get("c") is None, "Value 'c' should be gone after rollback"
    
    # Test nested transactions
    store.set("x", "10")
    store.begin()
    store.set("x", "20")
    store.begin()
    store.set("x", "30")
    assert store.get("x") == "30", "Should see innermost value"
    store.commit()  # Commit inner transaction - merges x=30 into middle
    assert store.get("x") == "30", "After commit, middle transaction has committed value"
    store.commit()  # Commit middle transaction - merges x=30 into base
    assert store.get("x") == "30", "After second commit, value should be in base layer"
    
    # Test cannot rollback/commit at base level
    assert not store.rollback(), "Cannot rollback at base level"
    assert not store.commit(), "Cannot commit at base level"
    
    # Test overwriting values in transactions
    store.set("y", "100")
    store.begin()
    store.set("y", "200")
    store.begin()
    store.set("y", "300")
    store.rollback()  # Discard innermost
    assert store.get("y") == "200", "After rollback, should see middle value"
    store.rollback()  # Discard middle
    assert store.get("y") == "100", "After second rollback, should see original value"
    
    print("All test cases passed!")