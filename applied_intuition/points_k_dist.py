"""
You are given a collection of 2D coordinates and a distance threshold, K, and are 
tasked with implementing an algorithm to partition these points into clusters. 
The rule for grouping is based on transitive proximity: two points belong to the same 
cluster if they are within distance K of each other, or if they can be connected by a 
chain of intermediate points where each consecutive pair is within distance K. After 
implementing a solution, you should discuss which well-known clustering algorithm your 
approach most closely resembles, such as K-Means or DBSCAN, and justify why that model 
is uniquely suited for this problem's specific requirements. Furthermore, you must analyze 
the time and space complexity of your algorithm, explain how it naturally handles outliers 
or points that don't belong to any cluster, and finally, discuss the strategies and challenges 
you would face when scaling your solution to handle a very large point cloud containing millions 
of coordinates.
"""
import collections

def find_clusters(points, K):
    """
    Partitions 2D points into clusters based on transitive proximity.

    Args:
        points (list[tuple[int, int]]): A list of (x, y) coordinates.
        K (float): The distance threshold for connectivity.

    Returns:
        list[list[tuple[int, int]]]: A list of clusters, where each cluster
                                     is a list of points.
    """
    n = len(points)
    if n == 0:
        return []

    # --- 1. Build the graph's adjacency list ---
    # We build the graph by connecting any two points within distance K.
    adj = collections.defaultdict(list)
    k_squared = K * K  # Compare squared distances to avoid costly sqrt()

    for i in range(n):
        for j in range(i + 1, n):
            p1 = points[i]
            p2 = points[j]
            
            # Euclidean distance squared: (x1-x2)^2 + (y1-y2)^2
            dist_sq = (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2
            
            if dist_sq <= k_squared:
                adj[i].append(j)
                adj[j].append(i)

    # --- 2. Find connected components using BFS ---
    all_clusters = []
    visited = set()

    for i in range(n):
        if i not in visited:
            # Start a new cluster for this unvisited point
            current_cluster = []
            q = collections.deque([i])
            visited.add(i)
            
            while q:
                node_idx = q.popleft()
                current_cluster.append(points[node_idx])
                
                # Explore all neighbors of the current node
                for neighbor_idx in adj[node_idx]:
                    if neighbor_idx not in visited:
                        visited.add(neighbor_idx)
                        q.append(neighbor_idx)
            
            all_clusters.append(current_cluster)
            
    return all_clusters

# --- Example Usage ---
points = [(0, 0), (1, 1), (0, 1), (5, 5), (6, 5), (10, 10)]
K = 1.5

clusters = find_clusters(points, K)
print(f"Found {len(clusters)} clusters:")
for i, cluster in enumerate(clusters):
    print(f"  Cluster {i+1}: {cluster}")