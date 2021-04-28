import time

class CacheEntry:
    def __init__(self, data):
        self.data = data
        self.accessed_at = time.time()
    
    def update_access(self):
        self.accessed_at = time.time()