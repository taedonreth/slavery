# leetcode 609: find duplicate file in system (medium)

from typing import List
from collections import defaultdict

class Solution:
    def findDuplicate(self, paths: List[str]) -> List[List[str]]:
        """
        Input: paths = ["root/a 1.txt(abcd) 2.txt(efgh)","root/c 3.txt(abcd)","root/c/d 4.txt(efgh)","root 4.txt(efgh)"]
        Output: [["root/a/2.txt","root/c/d/4.txt","root/4.txt"],["root/a/1.txt","root/c/3.txt"]]

        group all content together
        use string methods to format output

        keep a map of content: root_dir + name
        iterate through each path in paths
            split path
            for file in path
                if content in map
                    add root_dir + name as a value and content as key
                if not
                    create a key with content and root_dir + name as value

        collect duplicates
        return result

        # time: O(file length * number of files)
        # space: O(file length * number of files)
        """

        seen = defaultdict(list)
        for path in paths:
            # "root/a 1.txt(abcd) 2.txt(efgh)"
            parts = path.split()
            root_dir = parts[0]

            # ['root/a', '1.txt(abcd)', '2.txt(efgh)']
            for info in parts[1:]:
                # separate name and content
                file_name, file_content = info.split("(")

                # remove trailing )
                file_content = file_content[:-1]

                # add to map
                seen[file_content].append(f"{root_dir}/{file_name}")

        
        # seen = {"abcd": [root/a 1.txt, root/c 3.txt], "efgh": [root/a 2.txt, root/c/d 4.txt, root 4.txt]}
        # colect duplicates
        res = []
        for file_list in seen.values():
            if len(file_list) >= 2:
                res.append(file_list)

        return res

def main():
    sol = Solution()

    # Example 1
    paths1 = [
        "root/a 1.txt(abcd) 2.txt(efgh)",
        "root/c 3.txt(abcd)",
        "root/c/d 4.txt(efgh)",
        "root 4.txt(efgh)"
    ]
    expected1 = [
        ["root/a/2.txt","root/c/d/4.txt","root/4.txt"],
        ["root/a/1.txt","root/c/3.txt"]
    ]
    result1 = sol.findDuplicate(paths1)
    # Sorting inner lists and outer list to make comparison order-independent
    assert sorted([sorted(g) for g in result1]) == sorted([sorted(g) for g in expected1]), "Test case 1 failed"

    # Example 2
    paths2 = [
        "root/a 1.txt(abcd) 2.txt(efgh)",
        "root/c 3.txt(abcd)",
        "root/c/d 4.txt(efgh)"
    ]
    expected2 = [
        ["root/a/2.txt","root/c/d/4.txt"],
        ["root/a/1.txt","root/c/3.txt"]
    ]
    result2 = sol.findDuplicate(paths2)
    assert sorted([sorted(g) for g in result2]) == sorted([sorted(g) for g in expected2]), "Test case 2 failed"

    print("All test cases passed!")

if __name__ == "__main__":
    main()