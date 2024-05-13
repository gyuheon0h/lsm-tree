from typing import Tuple

class Point:
    def __init__(self, key: int, value: Tuple[float, ...]):
        """
        Points to store in the B-tree. Points are ordered by key.
        """
        self.key = key
        self.value = value

    def get_key(self) -> int:
        return self.key
    
    def get_value(self) -> Tuple[float, ...]:
        return self.value
    
    def __str__(self):
        return f"Point(key={self.key}, value={self.value})"
