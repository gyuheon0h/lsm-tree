from b_tree import BTree
from point import Point
from bloom_filter import MTableBloomFilter

MAXSIZE = 1000
BTREE_NODE_SIZE = 8

class Memtable:
    def __init__(self):
        self.map = BTree(t=BTREE_NODE_SIZE)
        # existence check across both memory and disk
        self.bloom_filter = MTableBloomFilter(n=MAXSIZE, fp_rate=0.1)
        self.file_id = 0

    def insert(self, point: Point):
        # TODO: HOW TO DEDUPE POINTS ACROSS BOTH MEMTABLE AND DISK? Currently only deduping on memory
        if self.map.size == MAXSIZE:
            self.flush(f"disk/file_{self.file_id}.txt")
            self.file_id += 1
            del self.map
            self.map = BTree(t=BTREE_NODE_SIZE)
        
        if self.bloom_filter.test(point.get_key()):
            if self.map.search(point.get_key()) is not None:
                print(f"Key: {point.get_key()} already exists in memory")
                return
            print("Bloom filter false positive")
        
        self.map.insert(point=point)
        self.bloom_filter.insert(key=point.get_key())

    def flush(self, file_path):
        self.map.flush(file_path=file_path)

    def search(self, key):
        check_filter = self.bloom_filter.test(key)
        if check_filter:
            searched = self.map.search(key)
            return searched if searched else f"Key: {key}, does not exist in Memtable"
        else:
            return f"Key: {key}, does not exist in Memtable"

table = Memtable()


import random

for _ in range(1000):
    i = random.randint(0,1000000)
    point = Point(key=i, value=(i, i*2, i/2))
    table.insert(point=point)
print(table.search(200))
print(table.search(400))
