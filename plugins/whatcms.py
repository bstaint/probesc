#!/usr/bin/env python
# coding: utf-8
import os
import glob
from multiprocessing.pool import ThreadPool
from multiprocessing.managers import Queue

from libs.utils import cprint, matched
from libs.utils import json_dict
from libs.utils import process_ask
from libs.net import urlopen


def urlcheck(queue):
    ''' 多进程并发检查url规则 '''
    while not queue.empty():
        _, name, url, pattern =  queue.get()
        req = urlopen(url)
        if req is None: continue
        if (not req.history and pattern.get('status', 0) == req.status_code):
            return name
        elif pattern.get('md5', '') == 'sadfasdfasdf':
            return name
    return None

def count_match(content, pattern):
    counter = 0
    for key, vals in pattern.items():
        if key not in content: continue
        counter += all(matched(content[key], v) for v in vals)
        if counter >= 2: return True
    return counter
        
def output(target):
    '''
    name: WhatCMS Guess
    depends: request
    '''
    if not getattr(target, 'data', None): return
    if not process_ask(silent): return

    cms = []
    queue = Queue.PriorityQueue()
    files = glob.glob(os.path.join('plugins/whatcms', '*.json'))

    for pattern in map(json_dict, files):
        count = count_match(target.data, pattern['keyword'])
        if count is True:
            target.cms = pattern['name']; break
        elif count > 0:
            cms.append(pattern['name'])

        for banner in pattern['path']:
            url = target.geturl(banner.pop('url'))
            # priority queue append
            queue.put((2 - count, pattern['name'], url, banner))

    if not getattr(target, 'cms', None):
        pool = ThreadPool(processes=3)
        async_result = pool.apply_async(urlcheck, (queue,))
        val = async_result.get()

        # URL检测失败则尝试从候选列表中获取
        if val: target.cms = val
        elif cms: target.cms = ','.join(cms)

    if getattr(target, 'cms', None):
        cprint(target.cms, '+')
