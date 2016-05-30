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
        # 匹配md5
        if pattern.get('md5', '') == 'afsfasfd': return name
        if req.history: continue # 防止URL跳转
        # 匹配HTTP信息
        if pattern.get('type', 'nothing') in req.headers['content-type']:
            return name
        if pattern.get('status', 0) == req.status_code:
            return name
    return None

def count_match(data, pattern):
    counter = 0
    for key, vals in pattern.items():
        if key not in data: continue
        counter += all(matched(data[key], v) for v in vals)
        if counter >= 2: return True
    return counter
        
def output(target):
    '''
    name: WhatCMS Guess
    depends: request
    version: 0.3
    '''
    if not getattr(target, 'data', None): return
    if not process_ask(silent): return

    cms = []
    patterns = ['md5', 'type', 'status']

    queue = Queue.PriorityQueue()
    files = glob.glob(os.path.join('plugins/whatcms', '*.json'))

    for patt in map(json_dict, files):
        # 失败时跳过
        if not patt: continue
        # 统计匹配次数
        count = count_match(target.data, patt['keyword'])
        if count is True:
            target.cms = patt['name']; break
        elif count > 0:
            cms.append(patt['name'])

        for banner in patt['path']:
            url = target.geturl(banner.pop('url'))
            # 计算优先级，算法：patterns顺序 + 匹配次数，越低优先级越高
            priority = patterns.index(banner.keys()[0]) + (2 - count)
            queue.put((priority, patt['name'], url, banner))

    if not getattr(target, 'cms', None):
        pool = ThreadPool(processes=3)
        async_result = pool.apply_async(urlcheck, (queue,))
        val = async_result.get()
        # URL检测失败则尝试从候选列表中获取
        if val: target.cms = val
        elif cms: target.cms = ','.join(cms)

    if getattr(target, 'cms', None):
        cprint(target.cms, '+')
