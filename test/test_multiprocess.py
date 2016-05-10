#!/usr/bin/env python
# coding: utf-8
import re
import urlparse
from libs.net import urlopen
import multiprocessing
import itertools
from libs.utils import cprint

domains = ['192.168.10.%d' % i for i in range(120, 130)]
ports = [80, 88, 7001, 7002, 7003, 8880, 8000, 8080]
uris = ['/cgi-bin/test-cgi', '/.svn/entries', '/.git/config']

def worker(queue):
    while True:
        task = queue.get()
        if task is None: break

        req = urlopen(urlparse.urljoin(*task))
        # 状态码200且不重定向
        if req and not req.history:
            cprint('%s status %d' % (req.url, req.status_code), '+')

def producer(task, queue):
    req = urlopen('http://{}:{}'.format(*task))
    if req is None: return

    match = re.search('<[Tt][Ii][Tt][Ll][Ee][^>]*>([^<]*)</[Tt][Ii][Tt][Ll][Ee]>', req.text)
    title = (match.group(1) if match else '').strip()

    server = req.headers.get('server', '')
    banner = 'unknown'
    if 'servlet' in req.headers.get('x-powered-by', ''):
        banner = 'servlet'

    cprint('%s %s %s [%s]' % (req.url, server, title, banner))
    for uri in uris:
        queue.put((req.url, uri))

queue = multiprocessing.Manager().Queue()

proc_work = multiprocessing.Process(target=worker,args=(queue,))
proc_work.start()

pool = multiprocessing.Pool(10)
for tup in itertools.product(domains, ports):
    pool.apply_async(producer, (tup, queue))

pool.close()
pool.join()

# 结束标志，终止工作进程
queue.put(None)
proc_work.join()
