#!/usr/bin/env python
# coding: utf-8
from operator import itemgetter

from libs.utils import cprint
from libs.utils import matched

pattern = {
    'headers': set([
        'by-360wzb',
        'by-anquanbao',
        'cc_cache',
        'cf-ray',
        'chinacache',
        'webcache',
        'x-cacheable',
        'x-fastly',
        'yunjiasu',
        'cdn cache server',
        'Verycdn'
    ]),
    'cname': set([
        '360wzb',
        'aqb.so',
        'dnspao.com',
        'ccgslb.com.cn',
        'cdn20.com',
        'cdntip.com',
        'incapdns',
        'wscdns.com',
        'yunjiasu-cdn',
        'lxdns.com',
        'fastcdn.com',
        'acadn.com',
        'cloudcdn.net',
        'cdn.dnsv1.com',
        'verygslb.com',
        'ourwebcdn.net',
        'jiasule',
        'jiashule',
        'alikunlun',
        'kunlunca.com',
        'kunlunar',
        'aliyun',
        'cdn-cdn.net',
        'alicloudlayer.com'
    ])
}

def output(target):
    '''
    name: CDN Checker
    priority: 2
    depends: request,dns
    version: 0.2
    '''
    target.cdn = False
    if redirect: return

    # 检测CNAME别名
    if getattr(target, 'zone', None):
        cname = map(itemgetter(1), target.zone.get('CNAME', []))
        log.debug('CNAME: %s' % ', '.join(cname))
        target.cdn = matched(cname, *pattern['cname'])
    # 检测HTTP头
    if not target.cdn and getattr(target, 'data', None):
        data = str(target.data['headers']).lower()
        target.cdn = matched(data, *pattern['headers'])
    # 检测第三方API内容
    if not target.cdn and getattr(target, 'raw_build', None):
        target.cdn = 'CDN Providers' in target.raw_build

    if target.cdn:
        cprint('%s has enable CDN' % target.ip, '+')
