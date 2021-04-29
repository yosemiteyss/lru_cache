import unittest
import time
from cache import Cache
from cache_entry import CacheEntry

class CacheTest(unittest.TestCase):

    def test_is_full(self):
        cache = Cache(2)

        cache.add(CacheEntry('A'))
        self.assertFalse(cache.is_full())

        cache.add(CacheEntry('B'))
        self.assertTrue(cache.is_full())
    
    def test_is_empty(self):
        cache = Cache(2)
        self.assertTrue(cache.is_empty())

        cache.add(CacheEntry('A'))
        self.assertFalse(cache.is_empty())

    def test_get_mru(self):
        cache = Cache(2)

        data_1 = 'A'
        cache.add(CacheEntry(data_1))
        self.assertEqual(cache.get_mru().data, data_1)

        data_2 = 'B'
        cache.add(CacheEntry(data_2))
        self.assertEqual(cache.get_mru().data, data_2)

    def test_contains(self):
        cache = Cache(2)

        data = 'A'
        self.assertFalse(cache.contains(data))

        cache.add(CacheEntry(data))
        self.assertTrue(cache.contains(data))

    def test_add(self):
        cache = Cache(2)

        entry_1 = CacheEntry('A')
        cache.add(entry_1)
        self.assertListEqual(cache.queue, [entry_1])
        
        entry_2 = CacheEntry('B')
        cache.add(entry_2)
        self.assertListEqual(cache.queue, [entry_2, entry_1])

        entry_3 = CacheEntry('C')        
        self.assertRaises(Exception, cache.add, entry_3)

    def test_detach_lru(self):
        cache = Cache(3)

        entry_1 = CacheEntry('A')
        cache.add(entry_1)
        lru = cache.detach_lru()
        self.assertEqual(entry_1, lru)

        entry_2 = CacheEntry('B')
        cache.add(entry_2)
        lru = cache.detach_lru()
        self.assertEqual(entry_2, lru)

    def test_remove(self):
        cache = Cache(3)

        entry_1 = CacheEntry('A')
        cache.add(entry_1)
        entry_2 = CacheEntry('B')
        cache.add(entry_2)
        entry_3 = CacheEntry('C')
        cache.add(entry_3)

        cache.remove(entry_2.data)
        self.assertListEqual(cache.queue, [entry_3, entry_1])
        
        cache.remove(entry_1.data)
        self.assertListEqual(cache.queue, [entry_3])

if __name__ == '__main__':
    unittest.main()