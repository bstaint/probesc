#!/usr/bin/env python
# coding: utf-8
import itertools
import multiprocessing

from libs.utils import cprint
from libs.net import urlopen

def urlcheck(host, path):
    req = urlopen('http://%s/%s' % (host, path))
    if req and not req.history:
        cprint('%s status %d' % (req.url, req.status_code), '+')

def output(target):
    '''
    name: URI Exploit Finder
    depends: ipvalid,domains,subweb
    version: 0.1
    '''
    uri = ['/cgi-bin/test-cgi', '/.svn/entries', '/.git/config']

    domains = set([target.host])

    domains.update(getattr(target, 'sameip', []))
    domains.update(getattr(target, 'domains', []))
    domains.update(getattr(target, 'subweb', []))

    pool = multiprocessing.Pool(5)
    for tup in itertools.product(domains, uri):
        pool.apply_async(urlcheck, tup)

    pool.close()
    pool.join()
