import time
from cache_entry import CacheEntry

class Cache:
    def __init__(self, size):
        self.size = size
        self.queue = []

    def is_full(self):
        return len(self.queue) >= self.size

    def __reorder_queue(self):
        self.queue = sorted(self.queue, key=lambda entry: entry.accessed_at, reverse=True)
    
    def get_mru(self):
        return self.queue[0]

    def get_lru(self):
        return self.queue[-1]

    def contains(self, data):
        return len([entry for entry in self.queue if entry.data == data]) != 0
    
    def is_empty(self):
        return len(self.queue) == 0

    def add(self, entry):
        if self.is_full():
            raise Exception('cache is full')

        self.queue.append(entry)

        self.__reorder_queue()

    def detach_last(self):
        return self.queue.pop()

    def remove(self, data):
        remove_entry = [entry for entry in self.queue if entry.data == data][0]
        entry_index = self.queue.index(remove_entry)

        self.queue.pop(entry_index)

        self.__reorder_queue()
        