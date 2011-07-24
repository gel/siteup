'''
Created on Apr 28, 2011

@author: dlemel
'''
import pickle

class Node(object):
    def __init__(self, prev, me):
        self.prev = prev
        self.me = me
        self.next = None


class LRU:
    """ 
    Implementation of a length-limited O(1) LRU queue.
    Wrote by Josiah Carlson, improvred by dlemel. 
    """
    def __init__(self, count, pairs=[]):
        self.count = max(count, 1)
        self.d = {}
        self._first = None
        self._last = None
        for key, value in pairs:
            self[key] = value
            
    def __contains__(self, obj):
        return obj in self.d
    
    def __getitem__(self, obj):
        a = self.d[obj].me
        self[a[0]] = a[1]
        return a[1]
    
    def __setitem__(self, obj, val):
        if obj in self.d:
            del self[obj]
        nobj = Node(self._last, (obj, val))
        if self._first is None:
            self._first = nobj
        if self._last:
            self._last.next = nobj
        self._last = nobj
        self.d[obj] = nobj
        if len(self.d) > self.count:
            if self._first == self._last:
                self._first = None
                self._last = None
                return
            a = self._first
            a.next.prev = None
            self._first = a.next
            a.next = None
            del self.d[a.me[0]]
            del a
            
    def __delitem__(self, obj):
        nobj = self.d[obj]
        if nobj.prev:
            nobj.prev.next = nobj.next
        else:
            self._first = nobj.next
        if nobj.next:
            nobj.next.prev = nobj.prev
        else:
            self._last = nobj.prev
        del self.d[obj]
    
    def flush(self):
        self.d.clear()
         
    def first(self):
        return self._first.me
    
    def last(self):
        return self._last.me
    
    def keys(self):
        return self.d.keys()
    
    def items(self):
        return [v.me for v in self.d.values()]

    def values(self):
        return [v[1] for v in self.items()]


class SerializableLRU(LRU):
    def __init__(self, count, file_name):
        try:
            file = open(file_name,'r')
            pairs = pickle.load(file)
            file.close()
            LRU.__init__(self, count, pairs)
        except:
            LRU.__init__(self, count)
        self.file_name = file_name
        
    def save(self):
        file = open(self.file_name,'w')
        pickle.dump(self.items(), file)
        file.close()
    
    
    