from b_tree import BTree
from point import Point
from bloom_filter import MTableBloomFilter

MAXSIZE = 100
BTREE_NODE_SIZE = 8

class Memtable:
    def __init__(self):
        self.map = BTree(t=BTREE_NODE_SIZE)

    def insert(self, point: Point):
        if self.map.size == MAXSIZE:
            self.flush("disk.txt")
            self.map = BTree(t=BTREE_NODE_SIZE)
        self.map.insert(point=point)
        print(f"Inserted {point}")

    def flush(self, file_path):
        self.map.flush(file_path=file_path)

table = Memtable()

for i in range(201):
    point = Point(key=i, value=(i, i*2, i/2))
    table.insert(point=point)
