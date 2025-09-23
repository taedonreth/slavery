# leetcode 1914: cyclically rotating a grid (medium)

from typing import List

"""
You are given an m x n integer matrix grid​​​, where m and n are both even integers, and an integer k.

The matrix is composed of several layers, which is shown in the below image, where each color is its own layer:

A cyclic rotation of the matrix is done by cyclically rotating each layer in the matrix. To cyclically rotate a layer once, 
each element in the layer will take the place of the adjacent element in the counter-clockwise direction. An example rotation is shown below:
"""
class Solution:
    def rotateGrid(self, grid: List[List[int]], k: int) -> List[List[int]]:
        """
        extract different layers
        helper function to rotate given array (a layer) k times
        how do you extract layers:
            extract layers by getting top row, then right column, then bottom row, then left col
            do this until you cant anymore
            Number of layers = min(m, n) // 2
            For each layer l:

                Define boundaries:
                top = l, left = l,
                bottom = rows - 1 - l, right = cols - 1 - l.

                Traverse in 4 steps:
                Top row → (top, left..right)
                Right column → (top+1..bottom, right)
                Bottom row → (bottom, right-1..left) (if top < bottom)
                Left column → (bottom-1..top+1, left) (if left < right)
            
        how do you rotate the array:
            [1, 2, 3, 4, 5] rotated once = [2, 3, 4, 5, 1]
            we can save unnecessary rotations by doing
            k %= len(layer)
            rotate k times = arr[k:] + arr[:k]
            arr[1:] + arr[:1] = [2, 3, 4, 5] + [1] = [2, 3, 4, 5, 1]
        """
        m, n = len(grid), len(grid[0])
        num_layers = min(m, n) // 2

        for layer in range(num_layers):
            # extract current layer
            elems = []
            top, left = layer, layer
            bottom, right = m - 1 - layer, n - 1 - layer

            # top row
            for j in range(left, right + 1):
                elems.append(grid[top][j])
            # right col
            for i in range(top + 1, bottom):
                elems.append(grid[i][right])
            # bottom row
            if bottom > top:
                for j in range(right, left - 1, -1):
                    elems.append(grid[bottom][j])
            # left col
            if right > left:
                for i in range(bottom - 1, top, -1):
                    elems.append(grid[i][left])

            # rotate k times
            k_norm = k % len(elems)
            rotated = elems[k_norm:] + elems[:k_norm]

            # write back to original grid
            idx = 0
            for j in range(left, right + 1):
                grid[top][j] = rotated[idx]
                idx += 1
            for i in range(top + 1, bottom):
                grid[i][right] = rotated[idx]
                idx += 1
            if bottom > top:
                for j in range(right, left - 1, -1):
                    grid[bottom][j] = rotated[idx]
                    idx += 1
            if right > left:
                for i in range(bottom - 1, top, -1):
                    grid[i][left] = rotated[idx]
                    idx += 1

        return grid

def main():
    sol = Solution()

    # Example 1
    grid1 = [[40,10],[30,20]]
    k1 = 1
    expected1 = [[10,20],[40,30]]
    assert sol.rotateGrid(grid1, k1) == expected1

    # Example 2
    grid2 = [[1,2,3,4],
             [5,6,7,8],
             [9,10,11,12],
             [13,14,15,16]]
    k2 = 2
    expected2 = [[3,4,8,12],
                 [2,11,10,16],
                 [1,7,6,15],
                 [5,9,13,14]]
    assert sol.rotateGrid(grid2, k2) == expected2

    # Edge case: no rotation
    grid3 = [[1,2],[3,4]]
    k3 = 0
    expected3 = [[1,2],[3,4]]
    assert sol.rotateGrid(grid3, k3) == expected3

    # Edge case: rotation by full cycle (should return original)
    grid4 = [[1,2],[3,4]]
    k4 = 4
    expected4 = [[1,2],[3,4]]
    assert sol.rotateGrid(grid4, k4) == expected4

    print("All test cases passed!")

if __name__ == "__main__":
    main()
