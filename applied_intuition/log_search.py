# log search function

"""
Implement a log search function that returns all entries containing a keyword, then extend 
it to support fuzzy searching (e.g., query "bre" should match "bread") and discuss 
scaling to large datasets
"""

def search_logs(logs: list[str], query: str, fuzzy: bool = False) -> list[str]:
    """
    Searches a list of log entries for a given query.

    Args:
        logs: A list of strings, where each string is a log entry.
        query: The string to search for.
        fuzzy: If False (default), performs an exact substring match.
               If True, performs a fuzzy (prefix) match on any word in the log.

    Returns:
        A list of log entries that match the query.
    """
    if not query:
        return []

    matching_logs = []
    for log_entry in logs:
        if fuzzy:
            # Fuzzy Search: Check if any word in the log starts with the query.
            words = log_entry.split()
            for word in words:
                if word.startswith(query):
                    matching_logs.append(log_entry)
                    break # Move to the next log entry once a match is found
        else:
            # Exact Search: Check if the query is a substring of the log.
            if query in log_entry:
                matching_logs.append(log_entry)

    return matching_logs

# --- Test Cases ---
if __name__ == "__main__":
    sample_logs = [
        "2025-10-05 INFO: User 'alice' logged in successfully.",
        "2025-10-05 WARNING: Disk space is running low.",
        "2025-10-05 INFO: Starting backup process.",
        "2025-10-05 ERROR: Connection to database failed. Retrying...",
        "2025-10-05 DEBUG: Breaking news: bread delivery is late.",
        "2025-10-05 INFO: User 'bob' logged out."
    ]

    print("--- Running Test Cases ---")

    # Test 1: Exact search for a word
    print("\n1. Exact search for 'logged':")
    results = search_logs(sample_logs, "logged")
    for r in results:
        print(f"   - {r}")

    # Test 2: Exact search for a phrase
    print("\n2. Exact search for 'database failed':")
    results = search_logs(sample_logs, "database failed")
    for r in results:
        print(f"   - {r}")

    # Test 3: Fuzzy search for a prefix
    print("\n3. Fuzzy search for 'log':")
    results = search_logs(sample_logs, "log", fuzzy=True)
    for r in results:
        print(f"   - {r}")

    # Test 4: Another fuzzy search
    print("\n4. Fuzzy search for 'bre':")
    results = search_logs(sample_logs, "bre", fuzzy=True)
    for r in results:
        print(f"   - {r}")
        
    # Test 5: No results found
    print("\n5. Search for 'transaction' (no match):")
    results = search_logs(sample_logs, "transaction")
    print(f"   - Found {len(results)} results.")

    # Test 6: Empty query
    print("\n6. Search for empty query (no match):")
    results = search_logs(sample_logs, "")
    print(f"   - Found {len(results)} results.")


"""

Scaling to Large Datasets
The current solution iterates through every log entry for every search.
 This is a full scan, with a time complexity of roughly O(N⋅M), 
where N is the number of log entries and M is the average length of an entry. 
This works for a small list but will be extremely slow for millions or billions of logs.

To scale this, you would stop treating the logs as a simple list and instead use a
 specialized data structure, a technique 
common in search engines like Elasticsearch or Splunk.

Preprocessing and Indexing: You wouldn't search the raw log files directly. 
Instead, you would preprocess them and build a search index. The most common 
type of index for this is an Inverted Index.

An Inverted Index is a data structure, like a hash map, where the keys are words 
(tokens) and the values are lists of documents (in this case, log IDs) that 
contain that word.

Example:
{"logged": [0, 5], "database": [3], "failed": [3], "bread": [4]}

An exact search for "database" becomes a very fast O(1) lookup in this index to find that it appears in log 3.

Handling Fuzzy (Prefix) Searches: An inverted index with a standard hash map is great for full-word 
matches, but not for prefix searches. To support efficient prefix matching, you would enhance the index's underlying data structure.

A Trie (Prefix Tree) is the ideal data structure for this. You would store your vocabulary of log 
words in a Trie. Each node in the Trie represents a character, and a path from the root spells a word.

To search for "bre", you would traverse the Trie to the node corresponding to this prefix. 
From there, you could quickly find all words that start with "bre" (e.g., "breaking", "bread") by 
traversing the sub-tree from that node. You would then use the Inverted Index to find all the logs containing those completed words.

By shifting from a "search-time" full scan to a "pre-processing time" indexing strategy, you can 
reduce the search latency from minutes or hours on a large dataset to milliseconds.








"""