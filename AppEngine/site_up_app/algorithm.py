'''Defines `algorithm`, the core SiteUp algorithm.'''
from . import KeywordsGenerator

def algorithm(query, searchtime, iterations):
    '''
    The core SiteUp algorithm.
    
    Returns string of keywords - seperated by \n
    '''
    context = query.split()
    for _ in range(iterations):
        res = KeywordsGenerator.KeywordsGenerator().run(context, searchtime)
        #res = [x[0] for x in res[:20]]
        #context += res[:1]
    return '\n'.join(set(res))