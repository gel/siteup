'''
Created on Apr 28, 2011

@author: dlemel
'''
import unittest
import time
from cache import LRU, SerializableLRU
from thread_pool import ThreadPool

class LRUTest(unittest.TestCase):
    def test_prefetching(self):
        elems = {'a':1, 'b':2}.items()
        lru = LRU(5, elems)
        assert lru.items() == elems
        
    def test_same_diffrent_key(self):
        lru = LRU(1)
        lru[0] = 5
        assert lru.items() == [(0,5)]
        lru[0] = 3
        assert lru.items() == [(0,3)]
        lru[2] = 17
        assert lru.items() == [(2,17)]
        
    def test_read_write(self):
        lru = LRU(3)
        lru[0] = 0
        lru[1] = 1
        lru[2] = 2
        assert len(lru.keys()) == 3
        lru[3] = 3
        assert 0 not in lru
        assert lru.last() == (3,3)
        lru[1]
        assert lru.last() == (1,1)
     
class SerializableLRUTest(unittest.TestCase):
    def test_save_flush_load(self):
        cache_name = 'util_test.cache'
        slru = SerializableLRU(2, cache_name)
        slru[6] = 'lalalala'
        old_state = slru.items()
        slru.save()
        slru.flush()
        assert old_state != slru.items()
        slru = SerializableLRU(2, cache_name)
        assert old_state == slru.items()
    
class ThreadPoolTest(unittest.TestCase):
    def test_time(self):
        def pool_time(thread_num):
            start = time.clock()
            tp = ThreadPool(thread_num)
            for i in range(5):
                tp.add_task(time.sleep, i)
            tp.wait_completion()
            return time.clock() - start
        
        one_runtime = pool_time(1)
        ten_runtime = pool_time(3)
        assert one_runtime > ten_runtime

    def test_results(self):
        def my_add(a,b):
            return a+b
        
        tp = ThreadPool(5)
        for i in range(5):
            tp.add_task(my_add, i, i)
        d = tp.wait_completion()
        vals = d.values()
        vals.sort()
        assert vals == [0, 2, 4, 6, 8]
