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


class Solution:
    def videoStitching(self, clips: List[List[int]], time: int) -> int:
        pass


if __name__ == "__main__":
    sol = Solution()

    # Example 1
    clips1 = [[0, 2], [4, 6], [8, 10], [1, 9], [1, 5], [5, 9]]
    assert sol.videoStitching(clips1, 10) == 3

    # Example 2
    clips2 = [[0, 1], [1, 2]]
    assert sol.videoStitching(clips2, 5) == -1

    # Example 3
    clips3 = [
        [0, 1],
        [6, 8],
        [0, 2],
        [5, 6],
        [0, 4],
        [0, 3],
        [6, 7],
        [1, 3],
        [4, 7],
        [1, 4],
        [2, 5],
        [2, 6],
        [3, 4],
        [4, 5],
        [5, 7],
        [6, 9],
    ]
    assert sol.videoStitching(clips3, 9) == 3

    # Exact coverage with consecutive intervals
    clips4 = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5]]
    assert sol.videoStitching(clips4, 5) == 5

    # Overlapping clips, optimal sub-selection
    clips5 = [[0, 4], [2, 8]]
    assert sol.videoStitching(clips5, 5) == 2

    # Single clip covers all
    clips6 = [[0, 10]]
    assert sol.videoStitching(clips6, 10) == 1

    # Gaps in coverage
    clips7 = [[0, 2], [4, 6], [8, 10]]
    assert sol.videoStitching(clips7, 10) == -1

    # Multiple overlapping short clips
    clips8 = [[0, 1], [0, 2], [1, 3], [2, 5], [4, 6], [5, 7]]
    assert sol.videoStitching(clips8, 7) == 4

    # Clip ends exactly at target time
    clips9 = [[0, 3], [2, 5]]
    assert sol.videoStitching(clips9, 5) == 2

    # Large redundant coverage
    clips10 = [[0, 2], [0, 3], [1, 4], [2, 6], [5, 10], [6, 10]]
    assert sol.videoStitching(clips10, 10) == 3

    print("✅ All test cases passed!")
