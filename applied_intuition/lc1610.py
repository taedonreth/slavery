# leetcode 1610: maximum number of visible points (hard)

from typing import List
import math

class Solution:
    def visiblePoints(self, points: List[List[int]], angle: int, location: List[int]) -> int:
        """
        function visiblePoints(points, angle, location):
            xx, yy = location
            arr = []              # will store angles of points relative to me
            extra = 0             # count of points at the same location as me

            # Step 1: compute angles for all points
            for each (x, y) in points:
                if (x == xx and y == yy):
                    extra = extra + 1       # same spot as me, always visible
                else:
                    dx = x - xx
                    dy = y - yy
                    theta = atan2(dy, dx)   # angle in radians from me to point
                    arr.append(theta)

            # Step 2: sort the angles
            sort(arr)

            # Step 3: duplicate angles with +2π to handle wrap-around
            for each angle in copy of arr:
                arr.append(angle + 2π)

            # Step 4: convert viewing angle from degrees to radians
            angle = angle * π / 180

            # Step 5: sliding window to find max points in any angle slice
            res = 0
            l = 0
            for r from 0 to len(arr)-1:
                # shrink left pointer if window too wide
                while arr[r] - arr[l] > angle:
                    l = l + 1

                # update best answer
                window_size = r - l + 1
                res = max(res, window_size)

            # Step 6: include points at same location
            return res + extra
        """
        
        arr, extra = [], 0
        xx, yy = location
        
        
        for x, y in points:
            # count points that are exactly at our location
            if x == xx and y == yy:
                extra += 1
                continue
            # normalize points - what angle is each point relative to location
            arr.append(math.atan2(y - yy, x - xx))
        
        arr.sort()

        # duplicate and add to end to represent cyclic nature of the coordiante plane in an array
        arr = arr + [x + 2.0 * math.pi for x in arr]

        # convert angle grom degrees to radians
        angle = math.pi * angle / 180
        
        # sliding window compute the max # of points that can be seen within our angle
        l = ans = 0
        for r in range(len(arr)):
            # outside of angle, close window scope
            while arr[r] - arr[l] > angle:
                l += 1
            # track # of points
            ans = max(ans, r - l + 1)
            
        return ans + extra