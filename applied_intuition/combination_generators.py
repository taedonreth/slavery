# generate all possible combinations

"""
given parameters with ranges (e.g., distance 1–10, time 1–10),
 output all possible combinations, then handle extremely large 
 ranges efficiently using streaming via Python generators.
"""

def generate_combinations(parameters):
    """
    Generate all possible combinations using EXPLICIT backtracking.
    Classic "choose → explore → unchoose" pattern.
    
    Args:
        parameters: dict where keys are parameter names and values are tuples (min, max)
                   e.g., {'distance': (1, 10), 'time': (1, 10)}
    
    Returns:
        list of dicts, each representing one combination
    """
    results = []
    param_names = list(parameters.keys())
    current = {}
    
    def backtrack(index):
        # Base case: all parameters have been assigned
        if index == len(param_names):
            results.append(current.copy())  # Must copy!
            return
        
        # Get current parameter and its range
        param = param_names[index]
        min_val, max_val = parameters[param]
        
        # Try each value in the range
        for value in range(min_val, max_val + 1):
            # 1. MAKE CHOICE
            current[param] = value
            
            # 2. EXPLORE/RECURSE
            backtrack(index + 1)
            
            # 3. UNDO CHOICE (backtrack!)
            del current[param]
    
    backtrack(0)
    return results


def generate_combinations_lazy(parameters):
    """
    Generate combinations using GENERATOR (lazy evaluation).
    Yields one combination at a time - memory efficient! ✨
    
    Perfect for large datasets where storing all combinations is impossible.
    Example: 10 params with range 1-10 = 10 billion combos, but only yields
    one at a time, so memory usage stays constant.
    
    Args:
        parameters: dict where keys are parameter names and values are tuples (min, max)
    
    Yields:
        dict representing one combination at a time
    """
    param_names = list(parameters.keys())
    current = {}
    
    def backtrack(index):
        if index == len(param_names):
            yield current.copy()  # Yield instead of append!
            return
        
        param = param_names[index]
        min_val, max_val = parameters[param]
        
        for value in range(min_val, max_val + 1):
            current[param] = value          # Choose
            yield from backtrack(index + 1) # Yield from recursive generator!
            del current[param]              # Unchoose
    
    yield from backtrack(0)

if __name__ == "__main__":

    params = {
        "distance": (1, 3),  # (min, max) tuple format
        "time": (1, 2),
    }

    for combo in generate_combinations(params):
        print(combo)
    for combo in generate_combinations_lazy(params):
        print(combo)