# leetcode 1024: video stitching (medium)

"""
You are given a series of video clips from a sporting event that lasted time seconds. These video clips can be overlapping with each other and have varying lengths.

Each video clip is described by an array clips where clips[i] = [starti, endi] indicates that the ith clip started at starti and ended at endi.

We can cut these clips into segments freely.

For example, a clip [0, 7] can be cut into segments [0, 1] + [1, 3] + [3, 7].
Return the minimum number of clips needed so that we can cut the clips into segments that cover the entire sporting event [0, time]. If the task is impossible, return -1.

 

Example 1:

Input: clips = [[0,2],[4,6],[8,10],[1,9],[1,5],[5,9]], time = 10
Output: 3
Explanation: We take the clips [0,2], [8,10], [1,9]; a total of 3 clips.
Then, we can reconstruct the sporting event as follows:
We cut [1,9] into segments [1,2] + [2,8] + [8,9].
Now we have segments [0,2] + [2,8] + [8,10] which cover the sporting event [0, 10].
Example 2:

Input: clips = [[0,1],[1,2]], time = 5
Output: -1
Explanation: We cannot cover [0,5] with only [0,1] and [1,2].
Example 3:

Input: clips = [[0,1],[6,8],[0,2],[5,6],[0,4],[0,3],[6,7],[1,3],[4,7],[1,4],[2,5],[2,6],[3,4],[4,5],[5,7],[6,9]], time = 9
Output: 3
Explanation: We can take clips [0,4], [4,7], and [6,9].
 

Constraints:

1 <= clips.length <= 100
0 <= starti <= endi <= 100
1 <= time <= 100
"""

from typing import List

class Solution:
    def videoStitching(self, clips: List[List[int]], time: int) -> int:
        """
        sort intervals by start time
        keep track of what interval we're on
        while loop to go through intervals

            go through all the intervals that are eligible to expand from our current spot ()
                expand right pointer to the highest value

            if theres no connecting interval
                return -1

            increment count 
        
        return count
        """
        clips.sort(key=lambda x: x[0])
        count = 0
        i = 0
        curr_end = 0

        while curr_end < time:
            max_reach = curr_end

            while i < len(clips) and clips[i][0] <= curr_end:
                max_reach = max(max_reach, clips[i][1])
                i += 1

            if max_reach == curr_end:
                return -1

            curr_end = max_reach
            count += 1

        return count


if __name__ == "__main__":
    s = Solution()

    # -----------------------------
    # Example test cases from LC
    # -----------------------------

    # Example 1
    clips = [[0,2],[4,6],[8,10],[1,9],[1,5],[5,9]]
    time = 10
    assert s.videoStitching(clips, time) == 3, "Example 1 failed"

    # Example 2
    clips = [[0,1],[1,2]]
    time = 5
    assert s.videoStitching(clips, time) == -1, "Example 2 failed"

    # Example 3
    clips = [
        [0,1],[6,8],[0,2],[5,6],[0,4],[0,3],
        [6,7],[1,3],[4,7],[1,4],[2,5],[2,6],
        [3,4],[4,5],[5,7],[6,9]
    ]
    time = 9
    assert s.videoStitching(clips, time) == 3, "Example 3 failed"

    # -----------------------------
    # Additional custom tests
    # -----------------------------

    # Case: Perfect coverage with 1 clip
    assert s.videoStitching([[0, 10]], 10) == 1, "Single clip full coverage failed"

    # Case: Cannot start at 0 → impossible
    assert s.videoStitching([[1, 5], [2, 10]], 10) == -1, "No start-at-zero failed"

    # Case: Exact matching segments
    clips = [[0,1], [1,3], [3,5], [5,7]]
    assert s.videoStitching(clips, 7) == 4, "Exact segments failed"

    # Case: Overlapping clips choose greedy max extension
    # best: [0,4], [4,8], [8,10]
    clips = [[0,2],[2,4],[0,4],[4,6],[6,8],[8,10],[1,8]]
    assert s.videoStitching(clips, 10) == 3, "Overlapping greedy case failed"

    # Case: Small time
    clips = [[0,1],[0,2]]
    assert s.videoStitching(clips, 1) == 1, "Small time failed"

    # Case: All clips useless
    clips = [[2,3],[4,5]]
    assert s.videoStitching(clips, 5) == -1, "Useless clips failed"

    # Case: Large overlaps but minimal picks
    # best: [0,5], [5,9]
    clips = [[0,3],[0,5],[1,8],[5,9]]
    assert s.videoStitching(clips, 9) == 2, "Big overlap greedy failed"

    print("All tests passed!")