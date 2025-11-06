# generate cross product of all json items

"""
You are given a JSON object where each key maps to a list of possible values, 
and you must write a function that generates all possible combinations by picking 
one value per key (e.g., { "color": ["red","blue"], "size": ["S","M"] } should produce 
{"color":"red","size":"S"}, {"color":"red","size":"M"}, {"color":"blue","size":"S"}, 
{"color":"blue","size":"M"}, etc.); implement this using backtracking or DFS, then discuss 
edge cases such as empty lists, and follow up with how you would handle very large inputs 
efficiently, including designing a generator-based approach to stream results without 
materializing everything in memory.
"""

from typing import List

def generate_combinations(json_object: dict[List]) -> List[dict]:
    res = []
    curr = {}
    keys = list(json_object.keys())

    def backtracking(index):
        if index == len(keys):
            res.append(curr.copy())
            return

        # Get the current key and its list of possible values
        key = keys[index]
        values_list = json_object[key]
        
        # Try each value in the list
        for value in values_list:
            curr[key] = value              # Choose
            backtracking(index + 1)        # Explore
            del curr[key]                  # Unchoose

    backtracking(0)
    return res


def generate_combinations_lazy(json_object: dict[List]):
    """
    Generator-based approach for memory efficiency.
    Yields one combination at a time without storing all results in memory.
    Perfect for large inputs where storing all combinations would be impractical.
    
    Example: 10 keys with 10 values each = 10 billion combinations
    - Eager approach: would require storing 10 billion dicts in memory (crash!)
    - Lazy approach: yields one at a time, constant memory usage ✨
    """
    keys = list(json_object.keys())
    curr = {}
    
    # Edge case: empty input
    if not keys:
        yield {}
        return
    
    # Edge case: if any value list is empty, no combinations possible
    for key in keys:
        if not json_object[key]:
            return  # Generator ends, yields nothing
    
    def backtracking(index):
        if index == len(keys):
            yield curr.copy()  # Yield instead of append!
            return
        
        key = keys[index]
        values_list = json_object[key]
        
        for value in values_list:
            curr[key] = value                  # Choose
            yield from backtracking(index + 1) # Yield from recursive generator!
            del curr[key]                      # Unchoose
    
    yield from backtracking(0)


if __name__ == "__main__":
    # Test 1: Normal case
    print("=== Test 1: Normal case ===")
    param = { "color": ["red","blue"], "size": ["S","M"] }
    print(generate_combinations(param))
    
    # Test 2: Edge case - empty dict
    print("\n=== Test 2: Empty dict ===")
    print(generate_combinations({}))  # [{}]
    
    # Test 3: Edge case - empty list value
    print("\n=== Test 3: Empty list value ===")
    print(generate_combinations({"color": [], "size": ["S"]}))  # []
    
    # Test 4: Single key-value
    print("\n=== Test 4: Single key ===")
    print(generate_combinations({"color": ["red"]}))  # [{"color": "red"}]
    
    # Test 5: Generator approach (lazy evaluation)
    print("\n=== Test 5: Generator approach (memory efficient) ===")
    large_param = { "color": ["red","blue","green"], "size": ["S","M","L"], "material": ["cotton", "polyester"] }
    print("Using generator (yields one at a time):")
    for i, combo in enumerate(generate_combinations_lazy(large_param)):
        print(f"{i+1}. {combo}")
    
    print("\n=== Comparison: Eager vs Lazy ===")
    print("Eager: Stores all combos in list -> High memory for large inputs")
    print("Lazy: Yields one at a time -> Constant memory, infinite scalability")
    
    """
    Expected output:
    [{"color":"red","size":"S"}, 
    {"color":"red","size":"M"}, 
    {"color":"blue","size":"S"}, 
    {"color":"blue","size":"M"}]
    
    EDGE CASES HANDLED:
    1. Empty dict {} -> Returns [{}] (one empty combination)
    2. Any empty list value -> Returns [] (no combinations possible)
    3. Single key -> Works correctly
    
    SCALABILITY:
    - Eager (generate_combinations): O(n) space where n = total combinations
      * Problem: 10 keys × 10 values = 10 billion combos = memory crash!
    - Lazy (generate_combinations_lazy): O(k) space where k = number of keys
      * Solution: Generates one at a time, can handle infinite combinations!
    """