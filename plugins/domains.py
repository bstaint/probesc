#!/usr/bin/env python
# coding: utf-8
import re
import requests
from operator import itemgetter

from libs.utils import cprint
from libs.net import urlopen, ssl_cert

apis_url = [
    ('http://api.chaxun.la/toolsAPI/getDomain/', 'k=%s&action=moreson', 'domain":"([^"]+)"'),
    ('http://site.ip138.com/%s/domain.htm', None, '">(.*?)<\/a><\/p>'),
    ('http://www.sitedossier.com/parentdomain/%s', None, '\/site\/([^"]+)">')
]

def output(target):
    '''
    name: Sub-Domain Finder
    depends: request,axfr
    version: 0.2
    '''
    def valid_tld(domain):
        return str.endswith(domain, target.tld)

    target.domains = set()
    regex = re.compile('(?<=\/\/)([\w\-]+\.)*?%s' % target.tld)

    for val in getattr(target, 'zone', {}).values():
        domains = filter(valid_tld, map(itemgetter(0), val))
        target.domains.update(domains)

    if getattr(target, 'axfr', False): return

    # 从同IP中获取
    domains = filter(valid_tld, getattr(target, 'raw_sameip', []))
    target.domains.update(domains)

    # 从ssl证书中提取相关域名
    if target.scheme == 'https':
        certs = ssl_cert(target.host, target.port)
        for _, domain in certs.get('subjectAltName', []):
            target.domains.add(domain.replace('*.', ''))

    # 从content中匹配
    for m in regex.finditer(target.data['content']):
        target.domains.add(m.group())

    # API 获取
    for url, param, regex in apis_url:
        params = param % target.tld if param else None
        text = urlopen(url, params=params, attr=('text', ''))

        target.domains.update(re.findall(regex, text))

    print target.domains
