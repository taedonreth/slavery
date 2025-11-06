"""
Given a list of vertex objects representing triangles in a sequence like v1, v2, v3, v2, v3, v4 
where vertices may be repeated across different triangles, create an indexing system that assigns 
a unique index to each distinct vertex and returns the triangle representation using these indices 
instead of the original vertex objects—for example, transforming the input [v1, v2, v3, v2, v3, v4] 
into indexed triangles [0, 1, 2] and [1, 2, 3] where v1=0, v2=1, v3=2, v4=3
"""

from typing import List, Tuple, Dict

class Vertex:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
    
    def __repr__(self) -> str:
        return f"Vertex({self.x}, {self.y})"


def index_triangles(vertices: List[Vertex]) -> Tuple[List[Vertex], List[List[int]]]:
    vertex_to_index: Dict[Tuple[float, float], int] = {}
    unique_vertices: List[Vertex] = []
    indexed_triangles: List[List[int]] = []
    
    # Create hashable key from 2D vertex object
    def vertex_key(v: Vertex) -> Tuple[float, float]:
        return (v.x, v.y)  # Just x and y for 2D
    
    for i, vertex in enumerate(vertices):
        key = vertex_key(vertex)
        
        if key not in vertex_to_index:
            vertex_to_index[key] = len(unique_vertices)
            unique_vertices.append(vertex)
        
        if i % 3 == 2:
            triangle: List[int] = [
                vertex_to_index[vertex_key(vertices[i-2])],
                vertex_to_index[vertex_key(vertices[i-1])],
                vertex_to_index[vertex_key(vertices[i])]
            ]
            indexed_triangles.append(triangle)
    
    return unique_vertices, indexed_triangles