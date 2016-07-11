#!/usr/bin/env python
# coding: utf-8
import re
import urlparse
import itertools
import multiprocessing

from libs.utils import cprint, option_input
from libs.net import urlopen

ports = [80, 88, 7001, 7002, 7003, 8880, 8000, 8080]
paths = ['/cgi-bin/test-cgi', '/.svn/entries', '/.git/config']
regex = re.compile('<[Tt][Ii][Tt][Ll][Ee][^>]*>([^<]*)</[Tt][Ii][Tt][Ll][Ee]>')

def parse(req):
    ''' 解析返回请求内容 '''
    banner = 'unknown'
    match = regex.search(req.text)
    title = (match.group(1) if match else '').strip()
    server = req.headers.get('server', '')

    if 'servlet' in req.headers.get('x-powered-by', ''):
        banner = 'servlet'
    return title, server, banner

def worker(queue):
    ''' 消费函数 '''
    while True:
        task = queue.get()
        if task is None: break
        req = urlopen(urlparse.urljoin(*task))
        # 状态码200且不重定向
        if req and not req.history:
            cprint('%s status %d' % (req.url, req.status_code), '+')

def producer(task, queue):
    ''' 生产函数 '''
    req = urlopen('http://{}:{}'.format(*task))
    if req is None: return
    # 解析请求内容
    server, title, banner = parse(req)
    cprint('%s %s %s [%s]' % (req.url, server, title, banner))
    for uri in paths:
        queue.put((req.url, uri))

def output(target):
    '''
    name: URI Exploit Finder
    depends: reverse,domains,subnet
    version: 0.2
    '''
    pool = multiprocessing.Pool(10)
    queue = multiprocessing.Manager().Queue()

    data = {
        1: getattr(target, 'domains', set()),
        2: getattr(target, 'email_domains', set()),
        4: getattr(target, 'subnet', set())
    }

    domains = set([target.host])
    ret = option_input('select extract data subdomain/domains/ip? [1/2/4] ', [1,2,4], '3')
    # 根据选择合并数据，删除自身域名
    domains.update(*[data[r] for r in ret])
    domains.discard(target.tld)
    # 生成一个专用进程来处理url检测
    proc_work = multiprocessing.Process(target=worker, args=(queue,))
    proc_work.start()
    # 进程池检测主机端口是否为Web服务
    for tup in itertools.product(domains, ports):
        pool.apply_async(producer, (tup, queue))

    pool.close()
    pool.join()
    # 结束标志，终止工作进程
    queue.put(None)
    proc_work.join()
