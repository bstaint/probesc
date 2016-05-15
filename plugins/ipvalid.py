#!/usr/bin/env python
# coding: utf-8
import re
import multiprocessing
from difflib import SequenceMatcher
from operator import itemgetter

from libs.utils import cprint
from libs.net import valid_ip, urlopen

apis = [
    ('http://m.tool.chinaz.com/same/?s=%s', '_blank>(.*?)</a></b>'),
    ('http://dns.aizhan.com/%s/', 'nofollow" target="_blank">(.*?)</a>'),
    ('http://www.114best.com/ip/114.aspx?w=%s', '&nbsp;<img alt="(.*?)"')
]

def output(target):
    '''
    name: IP Valider
    depends: sameip,reverse,domains
    '''
    def ratio_key(x):
        ''' 根据相似度排序 '''
        return SequenceMatcher(None, x[0], target.ip).ratio()

    target.sameip = set()

    # 删除本身域名
    domains = set(getattr(target, 'raw_sameip', []))
    domains.update(getattr(target, 'domains', []))
    domains.update(getattr(target, 'emdomains', []))
    # 剔除自身域名
    domains.discard(target.tld)

    pool = multiprocessing.Pool(5)
    iplist = pool.map(valid_ip, domains)

    iters = filter(itemgetter(0), zip(iplist, domains))
    # 根据IP相似度排序
    for ip, host in sorted(iters, key=ratio_key, reverse=True):
        if target.ip == ip:
            target.sameip.add(host)

        cprint('%s %s' % (host, ip), '+')
