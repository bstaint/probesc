#!/usr/bin/env python
# coding: utf-8
import re
import requests
from operator import itemgetter

from libs.utils import cprint
from libs.net import urlopen

apis_url = [
    ('http://api.chaxun.la/toolsAPI/getDomain/', 'k=%s&action=moreson', 'domain":"([^"]+)"'),
    ('http://site.ip138.com/%s/domain.htm', None, '">(.*?)<\/a><\/p>'),
    ('http://www.sitedossier.com/parentdomain/%s', None, '\/site\/([^"]+)">')
]

def output(target):
    '''
    name: Sub-Domain Finder
    depends: request,axfr
    version: 0.1
    '''
    def valid_tld(domain):
        return str.endswith(domain, target.tld)

    target.domains = set()

    if not getattr(target, 'axfr', False):
        # 从同IP中获取
        domains = filter(valid_tld, getattr(target, 'raw_sameip', []))
        target.domains.update(domains)

        # 从content中匹配
        regex = re.compile('(?<=\/\/)([\w\-]+\.)*?%s' % target.tld)
        for m in regex.finditer(target.data['content']):
            target.domains.add(m.group())

        # API 获取
        for url, param, regex in apis_url:
            if not param is None:
                try:
                    text = requests.post(url, params=param % target.tld, 
                                         headers=headers).text
                except requests.exceptions.RequestException, e:
                    text = ''
            else:
                text = urlopen(url % target.tld, attr=('text', ''))

            target.domains.update(re.findall(regex, text))

    # 从zone中获取
    for val in getattr(target, 'zone', {}).values():
        domains = filter(valid_tld, map(itemgetter(0), val))
        target.domains.update(domains)

    print target.domains
