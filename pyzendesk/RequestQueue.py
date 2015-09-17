from __future__ import absolute_import
import random
try:
    from queue import Queue
except ImportError:
    from Queue import Queue
import time
from threading import Thread
import requests

class BasicCache:
    def __init__(self):
        self.cache = {}

    def has(self, key):
        return key in self.cache

    def get(self, key):
        if self.has(key):
            return self.cache[key]
        else: 
            return None

    def set(self, key, value):
        self.cache[key] = value

    def delete(self, key):
        del self.cache[key]

    def clear(self):
        self.cache.clear()

class RequestQueue:
    def __init__(self, request_limit=200, num_workers=10, cache=None):
        self.max_speed     = 60/request_limit
        self.request_limit = request_limit
        self.request_queue = Queue()
        self.token_queue   = Queue()
        self.start_workers(num_workers)
        if cache:
            self.cache = cache
        else:
            self.cache = BasicCache()

    def start_workers(self, num):
        ticker = Thread(target=self.timer)
        ticker.daemon = True
        ticker.start()
        for i in range(num):
             t = Thread(target=self.worker)
             t.daemon = True
             t.start()

    def process(self, target):
        if type(target) is list:
            results = Queue()
            for item in target:
                self.request_queue.put((results,item))
            for _ in range(len(target)):
                yield results.get()
        else:
            results = Queue()
            self.request_queue.put((results, target))
            yield results.get()

    def worker(self):
        while True:
            self.token_queue.get()
            item = self.request_queue.get()
            result_queue = item[0]
            url = item[1][0]
            do_work = item[1][1]
            # if self.cache.has(url):
            #     result_queue.put(self.cache.get(url))
            # else:
            result = do_work(url)
            self.cache.set(url, result)
            result_queue.put(result)
            self.request_queue.task_done()
            self.token_queue.task_done()

    def timer(self):
        while True:
            time.sleep(self.max_speed)
            if self.token_queue.qsize() < self.request_limit:
                self.token_queue.put(None)
