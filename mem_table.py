from b_tree import BTree
from point import Point
from bloom_filter import MTableBloomFilter

MAXSIZE = 100
BTREE_NODE_SIZE = 8

class Memtable:
    def __init__(self):
        self.map = BTree(t=BTREE_NODE_SIZE)
        self.bloom_filter = MTableBloomFilter(n=MAXSIZE, fp_rate=0.001, r=MAXSIZE*2)

    def insert(self, point: Point):
        if self.map.size == MAXSIZE:
            self.flush("disk.txt")
            del self.map
            self.map = BTree(t=BTREE_NODE_SIZE)
        self.map.insert(point=point)
        self.bloom_filter.insert(key=point.get_key())

    def flush(self, file_path):
        self.map.flush(file_path=file_path)
        del self.bloom_filter
        self.bloom_filter = MTableBloomFilter(n=MAXSIZE,fp_rate=0.001, r=MAXSIZE*2)
        
    def search(self, key):
        check_filter = self.bloom_filter.test(key)
        if check_filter:
            searched = self.map.search(key)
            return searched if searched else f"Key: {key}, does not exist in Memtable"
        else:
            return f"Key: {key}, does not exist in Memtable"

table = Memtable()

for i in range(201):
    point = Point(key=i, value=(i, i*2, i/2))
    table.insert(point=point)
print(table.search(200))
print(table.search(400))
