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
    if getattr(target, 'cdn', False): return

    sameip = []
    for url, regex in apis:
        content = urlopen(url % target.host, attr=('text', ''))
        sameip.extend(re.findall(regex, content))

    target.raw_sameip = set(sameip[:50])
    print target.raw_sameip
