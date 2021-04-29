import time
from cache_entry import CacheEntry

class Cache:
    def __init__(self, size):
        self.size = size
        self.queue = []

    def __reorder_queue(self):
        self.queue = sorted(self.queue, key=lambda entry: entry.accessed_at, reverse=True)

    def is_full(self):
        return len(self.queue) >= self.size
    
    def is_empty(self):
        return len(self.queue) == 0
    
    def get_mru(self):
        return self.queue[0]

    def detach_lru(self):
        return self.queue.pop()

    def contains(self, data):
        return len([entry for entry in self.queue if entry.data == data]) != 0

    def add(self, entry):
        if self.is_full():
            raise Exception('cache is full')

        self.queue.append(entry)

        self.__reorder_queue()

    def remove(self, data):
        remove_entry = [entry for entry in self.queue if entry.data == data][0]
        entry_index = self.queue.index(remove_entry)

        self.queue.pop(entry_index)

        self.__reorder_queue()
        