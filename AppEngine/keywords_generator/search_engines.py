'''
Created on Apr 10, 2011

@author: dlemel
'''
import urllib
import json
import time
from util.cache import SerializableLRU
from util.thread_pool import ThreadPool

class SearchEngine:
    def __init__(self, thread_num, cache_file_name=None):
        self.thread_num = thread_num
        if cache_file_name:
            self.cache = SerializableLRU(10000, cache_file_name)
        else:
            self.cache = None
        
    def search(self, queries, ignore_urls=False):
        """ 
        Search the queries in the web, return a dict between query to search results.
        The web search itself is done in the method _search, implemented by the concrete SearchEngine.
        2 optimizations are used:
        - The queries are spread among threads (their number is determine by the concrete SearchEngine).
        -  
        """
        res = dict()
        web_queries = list()
        if self.cache and ignore_urls:
            for q in queries:
                if q in self.cache:
                    res[q] = self.cache[q]
                else:
                    web_queries.append(q)
        else:
            web_queries = queries
        
        d = {}
        tasks = set(web_queries[:])   
        while tasks:
            tp = ThreadPool(self.thread_num)
            for q in tasks:
                tp.add_task(self._search, q)
            d_items = tp.wait_completion().items()
            d.update([(item[0][1][0],item[1]) for item in d_items])
            tasks -= set(d.keys())
    
        for q in web_queries:
            if ignore_urls:
                res[q] = d[q][0]
            else:
                res[q] = d[q]
            if self.cache:
                self.cache[q] = d[q][0]
        return res
            
    def _search(self, query):
        ''' Search the string query in a search engine, return a tuple of total results and a url list '''
        raise NotImplementedError()

    def pos_query(self, str):
        raise NotImplementedError()
    
    def neg_query(self, str):
        raise NotImplementedError()
    
    def save(self):
        if self.cache:
            self.cache.save()


class BingSE(SearchEngine):
    def __init__(self, cache_file_name=None):
        SearchEngine.__init__(self, 6, cache_file_name)    # bing restrict the usage to less than 7 queries per second  
        app_id = '578DD45E5F45A8185EB6294951DA519BAA52D8C4'     # of username 'yp2010.g7@gmail.com'
        self.base_url = 'http://api.search.live.net/json.aspx?Appid=%s&' % app_id
        
    def _search(self, query):
        start = time.clock()
        payload = { 'Query':query, 'Sources':'web' }
        request = self.base_url + urllib.urlencode(payload)
        response = urllib.urlopen(request).read()
        try:
            data = json.loads(response)['SearchResponse']['Web']    
            urls = [dict['Url'] for dict in data['Results'] if 'Url' in dict]
            res = (data['Total'], urls)
        except:
            res = (0, [])
        delay = 1 - (time.clock() - start)
        if delay > 0:
            time.sleep(delay) 
        return res
    
    def pos_query(self, str):
        return ' +"' + str + '"'

    def neg_query(self, str):
        return ' -"' + str + '"'
    
