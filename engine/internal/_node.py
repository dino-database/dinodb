class Node:
    def __init__(self, key, value=None, level=1, is_dummy=False):
        self.key = key
        self.value = value if not is_dummy else None
        self.forward = [None] * level
        self.is_dummy = is_dummy
