'''
Created on May 17, 2011

@author: dlemel
'''
import unittest
from keywords_generator import KeywordsGenerator

class KeywordsGeneratorTest(unittest.TestCase):
    def test_imdb(self):
        imdb_keywords = set(['movies', 'films', 'movie database' , 'actors', 'actresses',
                         'directors', 'hollywood', 'stars', 'quotes'])   
        context = ['online database', 'movies', 'television shows', 'actors', 'visual entertainment media']   # from IMDB wiki
        
        l = KeywordsGenerator().run(context, 60)
        res = set([x[0] for x in l[:20]])
        assert res & imdb_keywords
                    
    def test_empty_search(self):
        assert not KeywordsGenerator().run([], 60) 
        
    def test_non_ascii(self):
        assert not KeywordsGenerator().run(['Was\x9f'], 60) 
        
    def test_not_enough_time(self):
        try:
            KeywordsGenerator().run(['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h'], 1)
            assert False 
        except:
            assert True