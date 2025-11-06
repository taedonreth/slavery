"""
Design and implement a unit conversion system that takes a list of conversion facts (for example, 
\'1 m = 3.28 ft', '1 ft = 12 in', '1 hr = 60 min', '1 min = 60 sec') and can answer conversion queries 
between different units; implement two functions: parse_facts(facts) which parses the conversion 
facts from a string format and builds an internal representation (such as a graph where nodes are 
units and edges are conversion ratios), and answer_query(query, facts) which takes a query like '2 m = ? in' 
and returns the converted value (78.72), or '13 in = ? m' returning 0.338, or '13 in = ? hr' returning 
'not convertible!' when no conversion path exists between units; discuss how you would represent the 
conversion graph to enable efficient pathfinding between units (BFS/DFS to find conversion chains), 
handle bidirectional conversions (if 1 m = 3.28 ft, then 1 ft = 1/3.28 m), maintain precision in floating-point 
calculations, detect impossible conversions between incompatible unit types (length vs. time), and optimize 
for scenarios where the same conversions are queried repeatedly; analyze the time and space complexity of 
both parsing and querying operations, and explain how your solution compares to graph problems like 
Evaluate Division' on LeetCode
"""

import collections

def parse_facts(facts):
    """
    Parses a list of conversion facts and builds a weighted, directed graph.
    
    Args:
        facts (list[str]): A list of conversion facts like '1 m = 3.28 ft'.
        
    Returns:
        dict: An adjacency list representing the conversion graph.
    """
    graph = collections.defaultdict(list)
    for fact in facts:
        # e.g., '1', 'm', '=', '3.28', 'ft'
        parts = fact.split()
        val1, unit1, _, val2, unit2 = parts
        val1, val2 = float(val1), float(val2)
        
        # Add forward and backward edges for bidirectional conversion
        # Edge from unit1 -> unit2 has ratio val2 / val1
        graph[unit1].append((unit2, val2 / val1))
        # Edge from unit2 -> unit1 has ratio val1 / val2
        graph[unit2].append((unit1, val1 / val2))
        
    return graph

def answer_query(query, graph):
    """
    Answers a conversion query using the pre-built conversion graph.
    
    Args:
        query (str): A query string like '2 m = ? in'.
        graph (dict): The conversion graph from parse_facts.
        
    Returns:
        float or str: The converted value or 'not convertible!'.
    """
    # 1. Parse the query
    parts = query.split()
    start_val, source_unit, _, _, target_unit = parts
    start_val = float(start_val)
    
    # Edge case: no conversion needed or unit doesn't exist
    if source_unit not in graph or target_unit not in graph:
        return 'not convertible!'
    if source_unit == target_unit:
        return start_val

    # 2. Find path using BFS and calculate product of ratios
    # Queue stores tuples of (current_unit, cumulative_ratio_from_source)
    q = collections.deque([(source_unit, 1.0)])
    visited = {source_unit}
    
    while q:
        curr_unit, curr_ratio = q.popleft()
        
        if curr_unit == target_unit:
            # Path found, return the final converted value
            return start_val * curr_ratio
            
        for neighbor_unit, conversion_ratio in graph[curr_unit]:
            if neighbor_unit not in visited:
                visited.add(neighbor_unit)
                # Append the neighbor and the updated cumulative ratio
                q.append((neighbor_unit, curr_ratio * conversion_ratio))
                
    # 3. If BFS completes and target was not found
    return 'not convertible!'

# --- Example Usage ---
facts = ['1 m = 3.28 ft', '1 ft = 12 in', '1 hr = 60 min', '1 min = 60 sec']
conversion_graph = parse_facts(facts)

# Query 1: Simple conversion
query1 = '2 m = ? in'
print(f"'{query1}' -> {answer_query(query1, conversion_graph)}") # Expected: ~78.72

# Query 2: Reverse conversion
query2 = '13 in = ? m'
print(f"'{query2}' -> {answer_query(query2, conversion_graph)}") # Expected: ~0.33

# Query 3: Impossible conversion
query3 = '13 in = ? hr'
print(f"'{query3}' -> {answer_query(query3, conversion_graph)}") # Expected: 'not convertible!'