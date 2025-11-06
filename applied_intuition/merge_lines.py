from collections import defaultdict
from pprint import pprint

"""
You are given a collection of 2D line segments. Each segment is represented by a sequence of points 
[(x1, y1), (x2, y2), …], where the first point is the start of the segment and the last point is the end. 
All points in a given segment are guaranteed to lie on the same straight line (lines are not curved). 
Your task is to design and implement a function that merges overlapping line segments into larger, continuous 
line segments, but only if they have the same slope. Segments with different slopes should remain separate.
Specifically:
Slope Calculation: Explain how you will calculate the slope of each segment, and how you will handle vertical 
and horizontal lines (where slope may be undefined or zero).


Overlap Detection: Define when two segments with the same slope can be considered overlapping (e.g., 
they lie on the same infinite line and their projections overlap on the x or y axis).


Merging Logic: If two segments overlap and share the same slope, merge them into a single segment by 
combining their points in sorted order.


Output: Return the merged set of line segments as a list of point sequences.


For example, given input:
Segments: 
  [
  [(2, 1), (4, 2))], 
  [(3, 3), (6, 6)], 
  [(8, 8), (9, 9)], 
  [(1, 1), (2, 2), (4, 4), (2.5, 2.5), (3.5, 3.5)]
  ]

The output should be:
[
  [(1, 1), (2, 2), (2.5, 2.5), (3, 3), (3.5, 3.5), (4, 4), (6, 6)], 
  [(8, 8), (9, 9)], 
  [(2, 1), (4, 2)]
]
"""


"""
keep a res list

trick: normalize lines and take into account horizontal/vertical lines with slope infinity and 0

group lines by slope and intercept in a dictionary O(n)  {slope: int: [lines]}
for each group
    # same slope, so see merging criteria

    sort individual segements by starting point


    # sorted = [ [(1, 1), (2, 2), (2.5, 2.5), (3.5, 3.5), (4, 4)], [(3, 3), (6, 6)], [(8, 8), (9, 9)], [(8.5, 8.5), (9.5, 9.5)] ]

    merge_arr = [sorted[0]]
    # merge_arr = [ [(1, 1), (2, 2), (2.5, 2.5), (3.5, 3.5), (4, 4), (3, 3), (6, 6)], [(8, 8), (9, 9)] ]
    for line in sorted[1:]:
        # are they overlapping?
        if merge_arr[-1][-1] >= line[0]:
            combined = set(merge_arr[-1] + line)
            merge_arr[-1] = sorted(list(combined))
        else:
            merge_arr.append(line)
    res.extend(merge_arr)


return res

helper function to calculate slope
"""

def merge_line_segments(segments):
    """
    Merges overlapping 2D line segments that share the same slope.

    Args:
        segments: A list of line segments, where each segment is a list of (x, y) points.

    Returns:
        A list of the final merged line segments.
    """
    if not segments:
        return []

    def calculate_slope(p1, p2):
        """Calculates the slope, handling vertical and horizontal cases."""
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        if dx == 0:
            return float('inf')  # Use infinity for vertical slope
        return round(dy / dx, 5)  # Round to handle floating point issues

    def get_line_key(p1, slope):
        """Generates a unique key (slope, intercept) for the line."""
        if slope == float('inf'):
            # For vertical lines, the 'intercept' is the x-coordinate
            return (slope, p1[0])
        else:
            # For other lines, calculate the y-intercept: b = y - mx
            intercept = round(p1[1] - slope * p1[0], 5)
            return (slope, intercept)

    # 1. Group segments by the infinite line they lie on
    line_groups = defaultdict(list)
    for seg in segments:
        # Sort points to reliably get start and end
        seg.sort()
        if len(seg) < 2:
            continue
        p1, p2 = seg[0], seg[-1]
        slope = calculate_slope(p1, p2)
        key = get_line_key(p1, slope)
        line_groups[key].append(seg)

    final_merged_segments = []

    # 2. For each group, sort segments and merge overlaps
    for key, group in line_groups.items():
        if not group:
            continue

        # Sort the segments within the group by their starting point
        group.sort(key=lambda seg: seg[0])

        # 3. Interval Merging Logic
        # Start with the first segment as the initial merged segment
        to_merge = [group[0]]
        
        for i in range(1, len(group)):
            # Check for overlap: Is the start of the current segment
            # before or at the end of the last merged segment?
            # Tuple comparison (e.g., (4, 4) >= (3, 3)) works correctly.
            if to_merge[-1][-1] >= group[i][0]:
                # Overlap detected, merge them
                combined_points = set(to_merge[-1] + group[i])
                # Update the last segment in place with the newly merged, sorted points
                to_merge[-1] = sorted(list(combined_points))
            else:
                # No overlap (a gap exists), so start a new merged segment
                to_merge.append(group[i])
        
        final_merged_segments.extend(to_merge)

    return final_merged_segments

if __name__ == "__main__":
    test1 = [
        [(2, 1), (4, 2)], 
        [(3, 3), (6, 6)], 
        [(8, 8), (9, 9)], 
        [(1, 1), (2, 2), (4, 4), (2.5, 2.5), (3.5, 3.5)],
    ]
    pprint(f"test1: {merge_line_segments(test1)}")


    test2 = [
        [(0, 0), (0, 1)], 
        [(0, 3), (0, 5)]
    ]
    pprint(f"test2: {merge_line_segments(test2)}")

    test3 = [
        [(0, 0), (1, 0)], 
        [(3, 0), (5, 0)]
    ]
    pprint(f"test3: {merge_line_segments(test3)}")