'''
Created on Apr 30, 2011

@author: dlemel
'''
import glob
import os
from math import log
from datetime import date

is_print_debug = False

def debug_print(param):
    if is_print_debug:
        print param

class NGD:
    def __init__(self, search_engine):
        self.search_engine = search_engine
        
    def queries(self, term1, term2):
        pq = self.search_engine.pos_query
        return [pq(term1), pq(term2), pq(term1) + pq(term2)]
    
    def safe_log(self, val):
        if val:
            return log(val)
        else:
            return 0
        
    def calc(self, term1, term2, search_engine_res_d):
        results = [self.safe_log(search_engine_res_d[x]) for x in self.queries(term1, term2)]
        x, y, xy = results[0], results[1], results[2]
        return (max(x,y)-xy)/float(log(14100000000)-min(x,y))

   
class Controller:
    def __init__(self, weighter, scorer, search_engine_name):
        self.weighter = weighter
        self.scorer = scorer
        cache_files = glob.glob('*.cache')
        today = str(date.today())
        if cache_files:
            cache_file_name = cache_files[0]
            if not cache_file_name.split('.')[0] == today:
                os.remove(cache_file_name)
                cache_file_name = today + '.cache'
        else:
            cache_file_name = today + '.cache'
        self.cached_search_engine = search_engine_name(cache_file_name)
    
    def run(self, world, context):
        weighted_context = self.weighter.weight(context, world, self.cached_search_engine)
        scored_world = self.scorer.score(world,  weighted_context, self.cached_search_engine)
        res = scored_world.items()
        res.sort(key=lambda tuple: tuple[1], reverse=True)
        self.cached_search_engine.save()
        return res
            