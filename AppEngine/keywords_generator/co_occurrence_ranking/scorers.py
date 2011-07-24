'''
Created on Apr 24, 2011

@author: dlemel
'''
from controller import NGD

class Scorer:
    def score(self, world,  weighted_context, search_engine):
        ''' 
        @param world: the world of terms to be scored
        @param weighted_context: the set of context terms, after weighting.
        @param search_engine: the search engine to use doing the scoring.
        @return: a dict between a word in the world and its score.
        '''
        raise NotImplementedError()
  
  
class BasicScorer(Scorer):
    def score(self, world,  weighted_context, search_engine):
        pq = search_engine.pos_query
        nq = search_engine.neg_query
        context = [c_word for c_word, weight in weighted_context]
        queries = []
        for w_word in world:
            queries += [pq(w_word)+pq(c_word) for c_word, weight in weighted_context]
            queries += [pq(w_word), pq(w_word)+''.join([nq(c_word) for c_word in context])]
        queries = list(set(queries))
        d = search_engine.search(queries, ignore_urls=True)
        res = {}
        for w_word in world:
            l = [d[pq(w_word)+pq(c_word)] * weight for c_word, weight in weighted_context]
            ex = d[pq(w_word)] - d[pq(w_word)+''.join([nq(c_word) for c_word in context])]
            try:
                res[w_word] = sum(l) / float(ex)
            except:
                res[w_word] = 0
        return res


class NGDScorer(Scorer):
    def score(self, world,  weighted_context, search_engine):
        ngd = NGD(search_engine) 
        context = [c_word for c_word, weight in weighted_context] 
        queries = [] 
        for w_word in world: 
            for c_word in context:
                queries += ngd.queries(w_word, c_word)
        queries = list(set(queries)) 
        d = search_engine.search(queries, ignore_urls=True) 
        res = {} 
        for w_word in world: 
            l = [ngd.calc(w_word, c_word, d) * weight for c_word, weight in weighted_context] 
            try: 
                res[w_word] = 1.0 / sum(l) 
            except: 
                res[w_word] = 0 
        return res

class MutualInformationScorerRegular(Scorer):
    def score(self, world,  weighted_context, search_engine):
        pq = search_engine.pos_query
        res = {}
        queries = []
        for w_word in world:
            queries += [pq(w_word)+pq(c_word) for c_word, weight in weighted_context]
        queries = list(set(queries))
            
        d = search_engine.search(queries, ignore_urls=True)
        for w_word in world:
            l = [d[pq(w_word)+pq(c_word)] * weight for c_word, weight in weighted_context]
            res[w_word]=sum(l)
        
        return res

class MutualInformationScorerNormalized(Scorer):
    def score(self, world,  weighted_context, search_engine):
        pq = search_engine.pos_query
        res = {}
        queries = []
        
        for w_word in world:
            queries += [pq(w_word)]
            queries += [pq(w_word)+pq(c_word) for c_word, weight in weighted_context]
        queries = list(set(queries))
        
        d = search_engine.search(queries, ignore_urls=True)
        
        for w_word in world:
            l = [d[pq(w_word)+pq(c_word)] * weight / float(d[pq(w_word)]) for c_word, weight in weighted_context]
            res[w_word]=sum(l)
            
        return res
    