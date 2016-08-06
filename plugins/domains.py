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
    depends: request,axfr,sameip
    version: 0.2
    '''
    def valid_tld(domain):
        # 解决UNICODE编码问题
        if type(domain) == unicode:
            domain = domain.encode('utf-8')
        return str.endswith(domain, target.tld)

    target.domains = set()
    # 从zone里过滤子域名
    for val in getattr(target, 'zone', {}).values():
        domains = filter(valid_tld, map(itemgetter(0), val))
        target.domains.update(domains)
    # 域传送漏洞检测
    if getattr(target, 'axfr', False): return

    # 从content中匹配子域名
    regex = re.compile('(?<=\/\/)([\w\-]+\.)*?%s' % target.tld)
    for m in regex.finditer(target.data['content']):
        target.domains.add(m.group())

    # 从同IP中提取子域名
    domains = filter(valid_tld, getattr(target, 'raw_sameip', []))
    target.domains.update(domains)

    # API 获取子域名
    for url, param, regex in apis_url:
        text = urlopen(url, attr=('text', ''), 
                       params=param % target.tld if param else None)
        target.domains.update(re.findall(regex, text))

    # 从SSL证书中提取子域名
    if target.scheme == 'https':
        certs = ssl_cert(target.host, target.port)
        # 过滤子域名
        for _, domain in certs.get('subjectAltName', []):
            if not valid_tld(domain): continue
            target.domains.add(domain.replace('*.', ''))

    print target.domains
