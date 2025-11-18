"""
You are given two lists:

- `points`, where each element is `[x, y]` representing a point on a 2D plane.
- `circles`, where each element is `[x_center, y_center, radius]` representing a circle.

Your task is to determine, for each point, whether it lies **inside or on the boundary**
of **at least one** of the given circles.

Return a list of booleans `result`, where `result[i]` is `True` if `points[i]`
is inside or on any circle, and `False` otherwise.

---

Example 1:

Input:
points = [[1, 2], [3, 4], [0, 0]]
circles = [[1, 2, 2], [5, 5, 1]]

Output:
[True, False, True]

Explanation:
- Point (1, 2) lies at the center of the first circle → inside.
- Point (3, 4) is outside all circles.
- Point (0, 0) is inside the first circle since (1−0)² + (2−0)² = 5 ≤ 4.

---

Example 2:

Input:
points = [[0, 0], [10, 10]]
circles = [[0, 0, 1], [10, 10, 2]]

Output:
[True, True]

---

Constraints:

- 1 <= len(points), len(circles) <= 10⁵
- -10⁴ <= x, y, x_center, y_center <= 10⁴
- 1 <= radius <= 10⁴

---

Follow-Up:

When there are **many points and many circles**, the naive O(N × M) approach
(checking every point against every circle) becomes too slow.

To improve efficiency:
1. Use **spatial partitioning** (e.g., a quadtree or k-d tree).
2. Pre-filter circles using their **bounding boxes** before checking exact distance.
3. For large datasets, use **vectorized operations** (NumPy) or spatial indexes (e.g., R-trees).

---

Hint:
A point `(x, y)` lies inside or on a circle `(xc, yc, r)` if and only if:
    (x - xc)² + (y - yc)² <= r²
"""

from typing import List

class Solution:
    def pointsInsideCircles(self, points: List[List[int]], circles: List[List[int]]) -> List[bool]:
        """
        Determine if each point is inside or on at least one circle.
        
        Key Formula:
        A point (x, y) is inside/on circle (xc, yc, r) if:
            (x - xc)² + (y - yc)² <= r²
        
        Strategy:
        1. For each point, check against all circles
        2. If any circle contains the point, mark as True
        3. Otherwise, mark as False
        
        Time: O(P × C) where P = number of points, C = number of circles
        Space: O(P) for the result array
        
        Note: We use squared distances to avoid floating point operations
        with square roots, which is both faster and more accurate.
        """
        result = []
        
        for point in points:
            px, py = point[0], point[1]
            is_inside = False
            
            # Check if this point is inside any circle
            for circle in circles:
                cx, cy, r = circle[0], circle[1], circle[2]
                
                # Calculate squared distance from point to circle center
                dx = px - cx
                dy = py - cy
                distance_squared = dx * dx + dy * dy
                
                # Check if point is inside or on the circle boundary
                if distance_squared <= r * r:
                    is_inside = True
                    break  # Found at least one circle, no need to check more
            
            result.append(is_inside)
        
        return result


if __name__ == "__main__":
    sol = Solution()

    # Example 1
    points = [[1, 2], [3, 4], [0, 0]]
    circles = [[1, 2, 2], [5, 5, 1]]
    assert sol.pointsInsideCircles(points, circles) == [True, False, True]

    # Example 2
    points = [[0, 0], [10, 10]]
    circles = [[0, 0, 1], [10, 10, 2]]
    assert sol.pointsInsideCircles(points, circles) == [True, True]

    print("✅ All test cases passed!")
