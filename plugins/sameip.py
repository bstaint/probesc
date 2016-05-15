#!/usr/bin/env python
# coding: utf-8
import re

from libs.utils import cprint
from libs.net import urlopen

apis = [
    ('http://m.tool.chinaz.com/same/?s=%s', '_blank>(.*?)</a></b>'),
    ('http://dns.aizhan.com/%s/', 'nofollow" target="_blank">(.*?)</a>'),
    ('http://www.114best.com/ip/114.aspx?w=%s', '&nbsp;<img alt="(.*?)"')
]

def output(target):
    '''
    name: SameIP Finder
    depends: cdn
    '''
    target.raw_sameip = set()

    # 通过API来获取
    if getattr(target, 'cdn', False): return
    for url, regex in apis:
        content = urlopen(url % target.host, attr=('text', ''))
        target.raw_sameip.update(re.findall(regex, content))

    target.raw_sameip = list(target.raw_sameip)[:50]
    print target.raw_sameip
