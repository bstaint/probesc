#!/usr/bin/env python
# coding: utf-8
import itertools
import multiprocessing

import re
from libs.utils import cprint
from libs.utils import process_ask
from libs.net import urlopen

ports = [80, 88, 7001, 7002, 7003, 8880, 8000, 8080]

def ip_range(num, limit=25):
    ''' 返回指定范围数值 '''
    bnum, enum = num - limit, num + limit
    if bnum < 1:
        bnum, enum = 1, enum + abs(bnum)
    elif enum > 254:
        bnum, enum = bnum - (enum - 254), 254
    return range(bnum, enum)

def urlcheck(tup):
    req = urlopen('http://%s:%d/' % tup, timeout=3)
    if req is None: return

    match = re.search('<[Tt][Ii][Tt][Ll][Ee][^>]*>([^<]*)</[Tt][Ii][Tt][Ll][Ee]>', req.text)
    server = req.headers['server'] if 'server' in req.headers else ''
    title = (match.group(1) if match else '').strip()

    cprint('%s %s %s' % (req.url, server, title), '+')
    return '%s:%d' % tup

def output(target):
    '''
    name: Subnet Web Scaner
    depends: cdn
    version: 0.2
    '''
    # 询问是否执行
    if getattr(target, 'cdn', True) or not process_ask(silent): return

    pos = target.ip.rfind('.')
    subnet, last_ip = target.ip[:pos], int(target.ip[pos + 1:])
    iplist = [subnet +'.'+ str(i) for i in ip_range(last_ip)]

    pool = multiprocessing.Pool(5)
    res = pool.map(urlcheck, itertools.product(iplist, ports))

    target.subweb = filter(None, res)
