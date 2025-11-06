"""
In DoorDash, the data importer occasionally makes typos, resulting in restaurant names that are very similar but not identical. Your task is to identify all restaurant names from a given list that are similar to a specified target name.

A restaurant name is considered similar if it can be transformed into the target name by swapping at most one pair of characters within the name.

Example:

Input:
Target restaurant name: "burgerking"
List of restaurant names: ["burgreking", "burgerkin", "burgekirng", "kingburger"]

Output:
["burgreking", "burgekirng"]
(Both names can be corrected to "burgerking" by swapping a single pair of letters.)

Input:
A string representing the target restaurant name.
A list of strings representing restaurant names.

Output:
A list of restaurant names from the given list that are similar to the target name.
"""

from typing import List


def similar_name(target: str, restaurant_names: List[str]) -> List[str]:
    # helper function to determine if a candidate string is similar to the target string
    def _is_similar(target: str, candidate: str) -> bool:
        # there are exactly 2 indicies where the strings differ
        # if you swap those two they become the same word

        if target == candidate:
            return True

        if len(target) != len(candidate):
            return False

        diff = []
        for i in range(len(target)):
            if target[i] != candidate[i]:
                diff.append(i)

                if len(diff) > 2:
                    return False

        if len(diff) != 2:
            return False
        # bank, kanb
        # diff = [0, 3]

        return (
            target[diff[-1]] == candidate[diff[0]]
            and target[diff[0]] == candidate[diff[-1]]
        )

    res = [name for name in restaurant_names if _is_similar(target, name)]
    return res


test = "burgerking"
test2 = ["burgreking", "burgerkin", "burgekring", "kingburger"]

print(similar_name(test, test2))
