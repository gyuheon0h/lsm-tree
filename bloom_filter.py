import math
from bitarray import bitarray
from sklearn.utils import murmurhash3_32

def hash_function_factory(m, seed=0):
    def hash_function(key):
        return murmurhash3_32(key, seed=seed, positive=True) % m
    return hash_function

# We want our bit array ranges to be a power of two. therefore, given a calculated range R, we want to round up to the nearest power of two
# greater than or equal to num
def round_up_to_power_of_two(num):
    if num <= 0:
        return 1
    if (num & (num - 1)) == 0:
        return num
    msb_position = 0
    while num > 0:
        num >>= 1
        msb_position += 1
    rounded_num = 1 << msb_position
    return rounded_num

class MTableBloomFilter:
    def __init__(self, n, fp_rate=None, r=None):
        self.n = n
        self.k = (0.7 * r) // self.n if r else int(math.log(fp_rate, 0.618) * math.log(2))
        self.r = r if r else round_up_to_power_of_two(int(math.log(fp_rate, 0.618) * self.n))

        self.hash_array = bitarray(self.r)
        self.hash_array.setall(0)

        # initialize our k independent hash function that map to a bit array of size self.r
        # in order to make this experiment reproducible, for k different independent hash functions we 
        # iterate k times from 0 => k * 5 in increments of 5 to have constant but different murmur hash seeds
        self.hash_functions = []
        for seed in range(0, int(self.k) * 5, 5):
            generated_function = hash_function_factory(self.r, int(seed))
            self.hash_functions.append(generated_function)

    def insert(self, key) -> None:
        for hash_function in self.hash_functions:
            generated_hash = hash_function(key)
            self.hash_array[generated_hash] = 1

    def test(self, key) -> bool:
        for hash_function in self.hash_functions:
            test_hash = hash_function(key)
            if self.hash_array[test_hash]:
                continue
            return False
        return True