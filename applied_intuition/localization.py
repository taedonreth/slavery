"""
You are tasked with designing a localization algorithm to find the coordinates of 
all hidden mobile devices on a global scale, represented by a 2D plane with continuous 
]latitude [-90, 90] and longitude [-180, 180]. You are provided with a black-box helper 
function, devices_exist(min_lat, min_lon, side_len) -> bool, which takes the bottom-left 
corner of a square region and its side length, and returns True if one or more devices 
are present within that square, and False otherwise; it does not tell you how many devices 
there are or their exact locations. Your goal is to implement a function that finds and 
returns the coordinates of all devices, up to a given precision threshold (epsilon). 
You should first explain your divide-and-conquer approach for the simplified case of 
finding a single device, and then extend your algorithm to robustly handle the primary 
challenge where there are an unknown number of multiple devices. Discuss how your 
extended algorithm manages multiple "hot" regions simultaneously, what data structure 
(e.g., for a DFS vs. BFS approach) would be appropriate, and what condition you would 
use to terminate the search for any given location. Finally, analyze the time 
complexity of your multi-device solution and briefly describe how your strategy 
would need to change if the devices were not stationary and could move.
"""

from typing import List, Tuple
from collections import deque


def find_all_devices(devices_exist, epsilon: float = 0.0001) -> List[Tuple[float, float]]:
    """
    Finds coordinates of all hidden mobile devices using a quadtree-based search.
    
    Args:
        devices_exist: Black-box function (min_lat, min_lon, side_len) -> bool
        epsilon: Precision threshold for device coordinates
    
    Returns:
        List of (latitude, longitude) tuples for all detected devices
    """
    # Start with the entire world
    queue = deque()
    
    # Check both halves of the world (longitude -180 to 0, and 0 to 180)
    if devices_exist(-90, -180, 180):
        queue.append((-90, -180, 180))
    if devices_exist(-90, 0, 180):
        queue.append((-90, 0, 180))
    
    devices = []
    # FIX: Use a set to track found regions to prevent duplicates
    found_regions = set()
    
    while queue:
        min_lat, min_lon, side_len = queue.popleft()
        
        # If region is small enough, we might have found a device
        if side_len <= epsilon:
            # FIX: Create a unique, discretized key for this region to avoid
            # floating point issues and ensure a device is added only once.
            region_key = (round(min_lat / epsilon), round(min_lon / epsilon))
            
            if region_key not in found_regions:
                # Use center of region as device location
                devices.append((
                    min_lat + side_len / 2,
                    min_lon + side_len / 2
                ))
                found_regions.add(region_key)
            continue
        
        # Subdivide into 4 quadrants
        half = side_len / 2
        quadrants = [
            (min_lat, min_lon, half),                  # Southwest
            (min_lat, min_lon + half, half),          # Southeast  
            (min_lat + half, min_lon, half),          # Northwest
            (min_lat + half, min_lon + half, half),   # Northeast
        ]
        
        for quad_lat, quad_lon, quad_side in quadrants:
            # Check if quadrant is within valid bounds
            if quad_lat >= -90 and quad_lat + quad_side <= 90 and \
               quad_lon >= -180 and quad_lon + quad_side <= 180:
                # Check if quadrant contains devices
                if devices_exist(quad_lat, quad_lon, quad_side):
                    queue.append((quad_lat, quad_lon, quad_side))
    
    return devices
    
"""
The initial code splits the rectangular world map into two large squares (Western and Eastern Hemispheres)
because the search function requires square-shaped areas to work.

Visually, latitude lines are horizontal circles on the globe measuring north-south position from -90° 
(South Pole) to +90° (North Pole), while vertical longitude lines measure east-west position from -180° to +180°.

The 3D globe is represented as a 2D plane by conceptually "unwrapping" it into a flat, rectangular map 
where longitude becomes the x-axis and latitude becomes the y-axis.

Yes, on the 2D map, latitude is the vertical Y-axis, so a latitude of -90° corresponds to the very bottom 
of the map (the South Pole).

The algorithm uses a divide-and-conquer approach with a queue to manage multiple searches simultaneously, 
stopping when a region is smaller than a precision epsilon, and its time complexity is O(D * log(1/ε)) for D devices.

"""
