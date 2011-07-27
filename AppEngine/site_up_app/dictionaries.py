'''
Created on Apr 15, 2011

@author: dlemel
'''
import urllib
import time
import re
from search_engines import BingSE
from co_occurrence_ranking.controller import debug_print

def connection_error():
    debug_print("ERROR - problem in open URL")

class Dictionary:
    def __init__(self):
        self.web_time = 0
        self.total_time = 0
        
    def start_time(self):
        self.tmp_total_time = time.clock()
        
    def end_time(self):
        self.total_time += time.clock() - self.tmp_total_time
        
    def start_web_time(self):
        self.tmp_web_time = time.clock()
        
    def end_web_time(self):
        self.web_time += time.clock() - self.tmp_web_time
        
    def lookup(self, queries):
        ''' Search the string query in a online dictionary, return a TODO '''
        raise NotImplementedError()
    
class DictionaryMasterSearch(Dictionary):
    def lookup(self, queries): 
        google = GoogleDictionarySearch()
        the_free = TheFreeDictionarySearch()
        
        l = []
        l += google.lookup(queries)
        l += the_free.lookup(queries)
        
        self.total_time = google.total_time + the_free.total_time
        self.web_time = google.web_time + the_free.web_time;
        return list(set(l))
    
class ThesaurusSearch(Dictionary):
    def __init__(self):
        Dictionary.__init__(self)
        self.first_str_url = 'http://thesaurus.com/browse/'
        self.last_str_url = '?rh=www.google.co.il'
        
    def lookup(self, queries):
        self.start_time()
        l = []
        for query in queries:
            try:
                request = self.first_str_url + query + self.last_str_url
                self.start_web_time()
                response = urllib.urlopen(request).read()
                self.end_web_time()
                groups1 = re.findall(r'<td valign="top">Synonyms:</td>.<td><span>.*?</span></td>', response, re.DOTALL | re.MULTILINE)
                for res in groups1:
                    str = re.sub('[\n\r\*]','',re.sub('<.*?>', '', re.sub('Synonyms:', '', res)))
                    str = str.replace(', ', ',') 
                    l += str.split(',')
            except:
                connection_error()
        self.end_time()
        return list(set(l))

class DictionaryComSearch(Dictionary):
    def __init__(self):
        Dictionary.__init__(self)
        self.base_url = 'http://dictionary.reference.com/browse/'
        
    def lookup(self, queries):
        self.start_time()
        l = []
        for query in queries:
            try:
                request = self.base_url + query
                self.start_web_time()
                response = urllib.urlopen(request).read()
                self.end_web_time()
                no_start = re.search(r'<div class="hd"><span >Nearby Words</span></div>.*', response, re.DOTALL | re.MULTILINE)
                if no_start:
                    no_end = re.search('(.*?)onclick="ask.dict.nearby.scrollDown()', no_start.group(), re.DOTALL | re.MULTILINE)
                    l_groups = re.findall(r'(<div id="nB..?" class="eD "><a href="/browse/)(' 
                                          + query + '.*?)(\?qsrc)', no_end.group(), re.DOTALL | re.MULTILINE)
                    for groups in l_groups:
                        str = re.sub('[+]',' ',groups[1]) 
                        l.append(str)
            except:
                connection_error()
        self.end_time()
        return list(set(l))

    
class GoogleDictionarySearch(Dictionary):
    def __init__(self):
        Dictionary.__init__(self)
        self.base_url = 'http://www.google.com/dictionary?langpair=en|en&hl=en&aq=f&'
        
    def lookup(self, queries):
        self.start_time()
        l = []
        for query in queries:
            try:
                payload = { 'q':query }
                
                request = self.base_url + urllib.urlencode(payload)
                self.start_web_time()
                response = urllib.urlopen(request).read()
                self.end_web_time()
                groups1 = re.search(r'Synonyms:.*', response, re.DOTALL | re.MULTILINE)
                if groups1:
                    groups2 = re.search(r'<ul>.*?</ul>', groups1.group(), re.DOTALL | re.MULTILINE)
                    lines = groups2.group().split('\n')
                    for line in lines:
                        groups3 = re.match('(<a href="/dictionary\?hl=en&q=)(.*)(&sl=en&tl=en&oi=dict_lk">.*)', line, re.DOTALL | re.MULTILINE)
                        if groups3:
                            str = re.sub('[+]', ' ', groups3.group(2))
                            l.append(str)       
            except:
                connection_error()
        self.end_time()  
        return list(set(l))
    
class TheFreeDictionarySearch(Dictionary):
    def __init__(self):
        Dictionary.__init__(self)
        self.base_url = 'http://www.thefreedictionary.com/'
        
    def lookup(self, queries):
        self.start_time()
        l = []
        for query in queries:
            try:
                request = self.base_url + query
                self.start_web_time()
                response = urllib.urlopen(request).read()
                self.end_web_time()
                no_start = re.search(r'ThesaurusTitle.*', response, re.DOTALL | re.MULTILINE)
                if no_start:
                    no_end = re.search('(.*?)wn\(\)</script>', no_start.group(), re.DOTALL | re.MULTILINE)
                    list_words = re.findall(r'(<a href=".*?">)(.*?)(</a>)', no_end.group(), re.DOTALL | re.MULTILINE)
                    for word in list_words:  
                        l.append(word[1])
            except:
                connection_error()
        self.end_time()
        return list(set(l))

class KeyWordsStealerWithFilter(Dictionary):
    def __init__(self, max_urls_to_query):
        Dictionary.__init__(self)
        self.max_urls_to_query = max_urls_to_query
        self.se = BingSE()
        self.dictionary = DictionaryMasterSearch()
    
    def remove_duplicates(self, l):
        for word in l:
            tmp = word + 's'
            if tmp in l:
                l.remove(tmp)
            tmp = re.sub(r'[ -]', '', word)
            if tmp != word and tmp in l:
                l.remove(tmp)
        return l
        
    def steal_keywords(self, urls, num):
        l = set([])
        for url in urls:
            self.start_web_time()
            try:
                response = urllib.urlopen(url).read()
                self.end_web_time()
                keys = re.search(r'<meta[^<>]*?name="keywords"[^<>]*?>', response, re.DOTALL | re.MULTILINE)
                if keys:
                    content = re.search(r'content=".*?"', keys.group(), re.DOTALL | re.MULTILINE)
                    str = content.group().replace('\n', '').replace('content=','').replace('"', '')
                    tmp_l = re.sub(r', *', ',', str).lower().split(',')
                    l = set(tmp_l + list(l))
                    if len(l) >= num:                        
                        l = set(self.remove_duplicates(list(l)))
                        if len(l) >= num:
                            break
            except:
                self.end_web_time()
        l = self.remove_duplicates(list(l))
        return l

    def lookup(self, queries):
		res = []
		self.start_time()
		words_per_query = int(self.max_urls_to_query / float(len(queries)))
		for query in queries:
			l = []
			i = 0
			to_search = query
			while len(l) < words_per_query:
				self.start_web_time()				
				(_, urls) = self.se.search([to_search])[to_search]
				self.end_web_time()
				l += self.steal_keywords(urls, words_per_query - len(l))
				break
				if len(l) < words_per_query: 
					l += self.dictionary.lookup([to_search])
				if i >= len(l):
					break    
				to_search = l[i]
				i += 1
				
			if len(l) > words_per_query:
				l = l[:words_per_query]
			res += l
		# subtract lists
		res = list(set(res).difference(queries))
		res = self.remove_duplicates(res)
		self.end_time()
		return res
		