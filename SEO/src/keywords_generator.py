'''
Created on May 17, 2011

@author: dlemel
'''
from web_operations.dictionaries import KeyWordsStealerWithFilter
from web_operations.search_engines import BingSE
from co_occurrence_ranking.controller import Controller
from co_occurrence_ranking.weighters import EntropyWeighter
from co_occurrence_ranking.scorers import NGDScorer

def is_ascii(s):
    try:
        s.encode('ascii')
        return True
    except:
        return False

class KeywordsGenerator:
    def run(self, context, run_time):     
        context = list(set(context))
        context = [w for w in context if is_ascii(w)]
        if not context:
            return []
        
        max_num_world = round(run_time / float(len(context)) * 6)
        if max_num_world < 10:
            raise Exception("not enough time") 
        
        world = list()
        world += KeyWordsStealerWithFilter(max_num_world).lookup(context)
        world = list(set(world))
        world = [w for w in world if is_ascii(w)]
        if not world:
            return []
        return Controller(EntropyWeighter(), NGDScorer(), BingSE).run(world, context)
         

