import time

class CacheEntry:
    def __init__(self, data):
        self.data = data
        self.accessed_at = time.time()