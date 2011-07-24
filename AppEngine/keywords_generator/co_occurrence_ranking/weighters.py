'''
Created on Apr 24, 2011

@author: dlemel
'''
from controller import NGD
from math import log

class Weighter:
    def weight(self, context, world, search_engine):
        ''' 
        @param terms: the collections of terms (strings) to be weighted.
        @return: a list of tuples of word and its weight (None if failed).
        '''
        raise NotImplementedError()

class BasicWeighter(Weighter):
    def weight(self, context, world, search_engine):
        return [(w,1) for w in context]

class NGDWeighter(Weighter):
    def weight(self, context, world, search_engine):
        ngd = NGD(search_engine)
        queries = []
        for c_word1 in context:
            sub_context = context[:]
            sub_context.remove(c_word1)
            for c_word2 in sub_context:
                queries += ngd.queries(c_word1, c_word2)
        queries = list(set(queries))
        d = search_engine.search(queries, ignore_urls=True)
        res = []
        for c_word1 in context:
            res.append((c_word1, sum([max(0, 1-ngd.calc(c_word1, c_word2, d)) for c_word2 in context if c_word1!=c_word2])))
        return res
    
class MutualInformationWeighter(Weighter):
    def weight(self, context, world, search_engine):
        pq = search_engine.pos_query
        res = []
        queries = []
        
        for c_word1 in context:
            queries += [pq(c_word1)]
            queries += [pq(c_word1)+pq(c_word2) for c_word2 in context if c_word1!=c_word2]
        queries = list(set(queries))
        
        d = search_engine.search(queries, ignore_urls=True)
        
        for c_word1 in context:
            l = [d[pq(c_word1)+pq(c_word2)] / float(d[pq(c_word1)]*d[pq(c_word2)]) for c_word2 in context if c_word1!=c_word2]
            res.append((c_word1, sum(l)))
        return res
    
class EntropyWeighter(Weighter):
    def weight(self, context, world, search_engine):
        pq = search_engine.pos_query
        res = []
        queries = []
    
        for c_word in context:
            queries += [pq(c_word)+pq(w_word) for w_word in world]
        queries = list(set(queries))
           
        d = search_engine.search(queries, ignore_urls=True)   # d is alpha
        
        P = {}
        for c_word in context:
            w_sum = sum([d[pq(c_word)+pq(w_word)] for w_word in world])
            for w_word in world:
                weight = 0
                if w_sum:
                    weight = float(d[pq(c_word)+pq(w_word)]) / w_sum
                P[(c_word, w_word)] = weight
        
        H = {}
        for c_word in context:
            l = [P[(c_word, w_word)] * log(P[(c_word, w_word)], 2) for w_word in world if P[(c_word, w_word)] > 0]
            H[c_word] = -1 * sum(l)
        
        # c_all cannot be 0
        c_all = sum(H.values())
        for c_word in context:
            res.append((c_word, 1 - float(H[c_word]) / c_all)) 
        
        return res