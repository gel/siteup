'''
Created on Apr 15, 2011

@author: dlemel
'''
import unittest
import os 
from web_operations.search_engines import BingSE
from web_operations.dictionaries import DictionaryComSearch,\
    GoogleDictionarySearch, TheFreeDictionarySearch,\
    DictionaryMasterSearch, ThesaurusSearch, KeyWordsStealerWithFilter
import time

class BingSETest(unittest.TestCase):
    bws = BingSE()
    
    def test_basic(self):
        res = self.bws.search(['bdio'], ignore_urls=True)
        total = res['bdio']
        assert total > 0
        
    def test_common_query(self):
        res = self.bws.search(['yearly project'])
        total, url_list = res['yearly project'] 
        assert total > 2000000
        assert url_list[0].startswith('http://')
        
class DictionaryMasterSearchTest(unittest.TestCase):
    gd = DictionaryMasterSearch()
    
    def test_basic(self):
        l = self.gd.lookup(['movie'])
        assert 'film' in l
        assert 'flick' in l
        assert 'bdio' not in l
        l = self.gd.lookup(['blechtz'])
        assert not len(l)
        
class ThesaurusSearchTest(unittest.TestCase):
    gd = ThesaurusSearch()
    
    def test_basic(self):
        time.sleep(5)
        l = self.gd.lookup(['movie'])
        assert 'film' in l
        assert 'parade' in l
        assert 'assembly hall' in l
        assert 'amphitheater' in l
        assert 'booshtaut' not in l
        time.sleep(5)
        l = self.gd.lookup(['booshtaut'])
        assert not len(l)
        
class DictionaryComSearchTest(unittest.TestCase):
    gd = DictionaryComSearch()
    
    def test_basic(self):
        time.sleep(5)
        l = self.gd.lookup(['movie'])
        assert 'movie maker' in l
        assert 'movie-goer' in l
        assert 'movie industry' in l
        assert 'movie mogul' in l
        assert 'movie blechtzer' not in l
        time.sleep(5)
        l = self.gd.lookup(['shplechtz'])
        assert not len(l)

class GoogleDictionarySearchTest(unittest.TestCase):
    gd = GoogleDictionarySearch()
    
    def test_basic(self):
        l = self.gd.lookup(['movie'])
        assert 'film' in l
        assert 'cinema' in l
        assert 'motion picture' in l
        assert 'cinematographic' in l
        assert 'sadfsadf' not in l
        l = self.gd.lookup(['bdio'])
        assert not len(l)

class TheFreeDictionarySearchTest(unittest.TestCase):
    gd = TheFreeDictionarySearch()
    
    def test_basic(self):
        l = self.gd.lookup(['movie'])
        assert 'synchronise' in l
        assert 'musical comedy' in l
        assert 'motion-picture show' in l
        assert 'coming attraction' in l
        assert 'sadfsadf' not in l
        l = self.gd.lookup(['bdio'])
        assert not len(l)
      
class KeyWordsStealerWithFilterTest(unittest.TestCase):
    num = 50
    gd = KeyWordsStealerWithFilter(num)
    
    def test_basic(self):
        
        l = self.gd.lookup(['shooki', 'zikri', 'doesnt', 'hedgehog'])
        assert len(l) <= self.num
        assert 'network' in l
        assert 'unix' in l
        assert 'blog' in l
        assert 'sadfsadf' not in l

class CachedSearchEngineTest(unittest.TestCase):
    cache_file_name = 'web_test.cache'
    def test_caching_is_better(self):
        def search_runtime():
            start = time.clock()
            cse.search(['lalala'], ignore_urls=True)
            return time.clock() - start
            
        if os.path.exists(self.cache_file_name):
            os.remove(self.cache_file_name)
        cse = BingSE(self.cache_file_name)
        first_query_runtime = search_runtime()
        cse.save()
        cse = BingSE(self.cache_file_name)
        second_query_runtime = search_runtime()
        assert first_query_runtime > second_query_runtime   

