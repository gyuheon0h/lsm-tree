from point import Point

class BTreeNode:
    def __init__(self, t, leaf=False):
        self.t = t
        self.leaf = leaf
        self.points = []
        self.children = []

    def __str__(self):
        if self.leaf:
            return f"Leaf BTreeNode with points {self.points}"
        else:
            return f"BTreeNode with points {self.points} and {len(self.children)} children"

class BTree:
    def __init__(self, t):
        self.root = None
        self.t = t
        self.size = 0

    def traverse(self):
        if self.root is not None:
            self._traverse(self.root)

    def _traverse(self, node: BTreeNode):
        i = 0
        for i in range(len(node.points)):
            if not node.leaf:
                self._traverse(node.children[i])
            print(node.points[i], end=' ')
        if not node.leaf:
            self._traverse(node.children[i+1])

    def flush(self, file_path):
        with open(file_path, 'a') as file:
            self._flush_to_file(self.root, file)

    def _flush_to_file(self, node: BTreeNode, file):
        if node is None:
            return
        i = 0
        for i in range(len(node.points)):
            if not node.leaf:
                self._flush_to_file(node.children[i], file)
            file.write(f"{node.points[i].get_key()}: {node.points[i].get_value()}\n")
        if not node.leaf:
            self._flush_to_file(node.children[i + 1], file)

    def search(self, key):
        return self._search(self.root, key) if self.root is not None else None

    def _search(self, node, key):
        i = 0
        while i < len(node.points) and key > node.points[i].get_key():
            i += 1
        if i < len(node.points) and node.points[i].get_key() == key:
            return node.points[i]
        if node.leaf:
            return None
        return self._search(node.children[i], key)

    def insert(self, point: Point):
        if self.root is None:
            self.root = BTreeNode(self.t, True)
            self.root.points.append(point)
        else:
            if len(self.root.points) == 2*self.t - 1:
                s = BTreeNode(self.t, False)
                s.children.append(self.root)
                self._split_child(s, 0)
                self._insert_non_full(s, point)
                self.root = s
            else:
                self._insert_non_full(self.root, point)
        self.size += 1

    def _insert_non_full(self, node: BTreeNode, point: Point):
        i = len(node.points) - 1
        if node.leaf:
            node.points.append(None)  # Append a dummy value to expand the list
            while i >= 0 and node.points[i].get_key() > point.get_key():
                node.points[i+1] = node.points[i]
                i -= 1
            node.points[i+1] = point
        else:
            while i >= 0 and node.points[i].get_key() > point.get_key():
                i -= 1
            i += 1
            if len(node.children[i].points) == 2*self.t - 1:
                self._split_child(node, i)
                if point.get_key() > node.points[i].get_key():
                    i += 1
            self._insert_non_full(node.children[i], point)

    def _split_child(self, parent: BTreeNode, i):
        t = self.t
        y = parent.children[i]
        z = BTreeNode(t, y.leaf)
        mid_point = y.points[t - 1]
        parent.children.insert(i + 1, z)
        parent.points.insert(i, mid_point)

        z.points = y.points[t:(2*t - 1)]
        y.points = y.points[0:(t - 1)]

        if not y.leaf:
            z.children = y.children[t:(2*t)]
            y.children = y.children[0:t]