from ._node import Node
import random
import uuid
import sys

class SkipList:
    def __init__(self, max_level=16, p=0.5):
        self.max_level = max_level
        self.p = p
        self.header = Node(None, level=max_level, is_dummy=True)
        self.level = 1

    def _random_level(self):
        lvl = 1
        while random.random() < self.p and lvl < self.max_level:
            lvl += 1
        return lvl

    def insert(self, value, key=None):
        if key is None:
            key = str(uuid.uuid4())
        elif isinstance(key, uuid.UUID):
            key = str(key)

        update = [None] * self.max_level
        current = self.header

        for i in range(self.level - 1, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current

        new_level = self._random_level()
        if new_level > self.level:
            for i in range(self.level, new_level):
                update[i] = self.header
            self.level = new_level

        new_node = Node(key, value, new_level)
        for i in range(new_level):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node

        return key

    
    def search(self, key):
        if isinstance(key, uuid.UUID):
            key = str(key)

        current = self.header
        for i in range(self.level - 1, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]

        current = current.forward[0]
        if current and current.key == key:
            return current.value

        return None
    
    def delete(self, key):
        update = [None] * self.max_level
        current = self.header
        
        for i in range(self.level - 1, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current
        
        current = current.forward[0]
        if current and current.key == key:
            for i in range(self.level):
                if update[i].forward[i] != current:
                    break
                update[i].forward[i] = current.forward[i]
            while self.level > 1 and not self.header.forward[self.level - 1]:
                self.level -= 1
    
    def total_memory_usage(self):
        total_size = sys.getsizeof(self.header)
        current = self.header.forward[0]
        while current:
            total_size += sys.getsizeof(current.key) + (sys.getsizeof(current.value) if current.value else 0)
            current = current.forward[0]
        return total_size