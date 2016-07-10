#!/usr/bin/env python
# coding: utf-8
import re
import multiprocessing
from difflib import SequenceMatcher
from operator import itemgetter

from libs.utils import cprint, option_input
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

    data = {1: getattr(target, 'domains', set())}
    # raw_sameip差集
    data[2] = getattr(target, 'raw_sameip', set()) - data[1]
    data[2].update(getattr(target, 'email_domains', set()))

    ret = option_input('select extract data subdomain/domains? [1/2] ', [1,2], '3')

    domains = set()
    # 合并数据，删除自身域名
    domains.update(*[data[r] for r in ret])
    domains.discard(target.tld)

    pool = multiprocessing.Pool(5)
    iplist = pool.map(valid_ip, domains)

    target.sameip = set()
    # 根据IP相似度排序
    iters = filter(itemgetter(0), zip(iplist, domains))
    for ip, host in sorted(iters, key=ratio_key, reverse=True):
        if target.ip == ip: target.sameip.add(host)
        cprint('%s %s' % (host, ip), '+')
