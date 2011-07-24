'''
Created on May 15, 2011

@author: dlemel
'''
from Queue import Queue
from threading import Thread

class Worker(Thread):
    """Thread executing tasks from a given tasks queue"""
    def __init__(self, tasks, res_dict):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.res_dict = res_dict
        self.start()
    
    def run(self):
        while True:
            func, args = self.tasks.get()
            try:
                k = (func,args)
                res = func(*args)
                self.res_dict[k] = res   # atomic!
            except Exception, e: 
                print args, e
            self.tasks.task_done()

class ThreadPool:
    """Pool of threads consuming tasks from a queue"""
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        self.res_d = dict()
        for _ in range(num_threads): Worker(self.tasks, self.res_d)

    def add_task(self, func, *args):
        """Add a task to the queue"""
        self.tasks.put((func, args))

    def wait_completion(self):
        """Wait for completion of all the tasks in the queue"""
        self.tasks.join()
        return self.res_d
