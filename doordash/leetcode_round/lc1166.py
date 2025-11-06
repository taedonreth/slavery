# leetcode 1166: design file system (medium)

"""
You are asked to design a file system that allows you to create new paths and associate them with different values.

The format of a path is one or more concatenated strings of the form: / followed by one or more lowercase English letters. For example, "/leetcode" and "/leetcode/problems" are valid paths while an empty string "" and "/" are not.

Implement the FileSystem class:

bool createPath(string path, int value) Creates a new path and associates a value to it if possible and returns true. Returns false if the path already exists or its parent path doesn't exist.
int get(string path) Returns the value associated with path or returns -1 if the path doesn't exist.
"""


class FileSystem:
    def __init__(self):
        self.file_sys = {}

    def createPath(self, path: str, value: int) -> bool:
        """
        validate the path
        then add if its valid
        """
        if path in self.file_sys or len(path) == 0 or path == "/":
            return False

        parent = path[: path.rfind("/")]
        if len(parent) > 1 and parent not in self.file_sys:
            return False

        # add path
        self.file_sys[path] = value
        return True

    def get(self, path: str) -> int:
        return self.file_sys.get(path, -1)


# Your FileSystem object will be instantiated and called as such:
# obj = FileSystem()
# param_1 = obj.createPath(path,value)
# param_2 = obj.get(path)

"""
this method uses a lot of space
if many paths and less gets, use trie
if less paths and more gets, use this


# The TrieNode data structure.
class TrieNode(object):
    def __init__(self, name):
        self.map = defaultdict(TrieNode)
        self.name = name
        self.value = -1

class FileSystem:

    def __init__(self):

        # Root node contains the empty string.
        self.root = TrieNode("")

    def createPath(self, path: str, value: int) -> bool:

        # Obtain all the components
        components = path.split("/")

        # Start "curr" from the root node.
        cur = self.root

        # Iterate over all the components.
        for i in range(1, len(components)):
            name = components[i]

            # For each component, we check if it exists in the current node's dictionary.
            if name not in cur.map:

                # If it doesn't and it is the last node, add it to the Trie.
                if i == len(components) - 1:
                    cur.map[name] = TrieNode(name)
                else:
                    return False
            cur = cur.map[name]

        # Value not equal to -1 means the path already exists in the trie.
        if cur.value!=-1:
            return False

        cur.value = value
        return True

    def get(self, path: str) -> int:

        # Obtain all the components
        cur = self.root

        # Start "curr" from the root node.
        components = path.split("/")

        # Iterate over all the components.
        for i in range(1, len(components)):

            # For each component, we check if it exists in the current node's dictionary.
            name = components[i]
            if name not in cur.map:
                return -1
            cur = cur.map[name]
        return cur.value
"""
