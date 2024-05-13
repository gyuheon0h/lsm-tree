from b_tree import BTree
from point import Point
import random

btree = BTree(t=10)



for i in range(100):
    point = Point(key=i, value=(i, i*2, i//3))
    btree.insert(point)

btree.traverse()
