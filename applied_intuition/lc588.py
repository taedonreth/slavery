# leetcode 588: design in-memory file system (hard)

from typing import List

class Node:
    def __init__(self):
        self.children = {}
        self.content = ""
        self.is_file = False

class FileSystem:
    def __init__(self):
        self.root = Node()
    
    def ls(self, path: str) -> List[str]:
        node = self._navigate(path)
        if node.is_file:
            return [path.split('/')[-1]]
        return sorted(node.children.keys())
    
    def mkdir(self, path: str) -> None:
        self._navigate(path)
    
    def addContentToFile(self, filePath: str, content: str) -> None:
        node = self._navigate(filePath)
        node.is_file = True
        node.content += content
    
    def readContentFromFile(self, filePath: str) -> str:
        node = self._navigate(filePath)
        return node.content

    def _navigate(self, path: str) -> Node:
        parts = [p for p in path.split('/') if p]
        node = self.root
        for part in parts:
            if part not in node.children:
                node.children[part] = Node()
            node = node.children[part]
        return node

# Your FileSystem object will be instantiated and called as such:
# obj = FileSystem()
# param_1 = obj.ls(path)
# obj.mkdir(path)
# obj.addContentToFile(filePath,content)
# param_4 = obj.readContentFromFile(filePath)


"""
class Node:
    def __init__(self, is_file=False):
        self.is_file = is_file
        self.children = {} if not is_file else None


class FileSystem:
    def __init__(self):
        self.root = Node()

    def _traverse(self, path, create=False):
        parts = [p for p in path.split("/") if p]
        curr = self.root

        for part in parts[:-1]:
            if part not in curr.children:
                if create:
                    curr.children[part] = Node(is_file=False)
                else:
                    raise FileNotFoundError(f"Directory '{part}' does not exist")
            curr = curr.children[part]
            if curr.is_file:
                raise ValueError(f"'{part}' is a file, not a directory")

        return curr, parts[-1] if parts else ""

    def mkdir(self, path):
        parent, name = self._traverse(path, create=True)
        if name in parent.children:
            raise FileExistsError(f"'{name}' already exists")
        parent.children[name] = Node(is_file=False)

    def touch(self, path):
        parent, name = self._traverse(path, create=True)
        if name in parent.children:
            raise FileExistsError(f"'{name}' already exists")
        parent.children[name] = Node(is_file=True)
"""