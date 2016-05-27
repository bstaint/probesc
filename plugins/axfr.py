#!/usr/bin/env python
# coding: utf-8
from operator import itemgetter

from libs.net import parsedns
from libs.utils import cprint, filtered

pattern = set([
    "22.cn",
    "360safe.com",
    "360wzb.com",
    "4cun.com",
    "cloudflare.com",
    "dnspod.net",
    "dnsv2.com",
    "dnsv3.com",
    "dnsv4.com",
    "dnsv5.com",
    "farbox.net",
    "hichina.com",
    "hosting.edu.cn",
    "iidns.com",
    "myhostadmin.net",
    "xincache.com",
    "xinnet.com",
    "yunjiasu.com",
    "domaincontrol.com",
    "bigwww.com",
    "alidns.com",
    "chinanetcenter.com",
    "xincache.com",
    "awsdns",
    "dns.net.cn",
    "dnsdun.com",
    "ffdns.net",
    "ezdnscenter",
    "sfn.cn",
    "365cyd.net"
])

def output(target):
    '''
    name: AXFR Checker
    priority: 8
    depends: dns
    version: 0.3
    '''
    if not getattr(target, 'zone', None): return
    target.axfr = False
    # 从zone中提取NS记录并过滤
    ns = map(itemgetter(0), target.zone.get('NS', []))
    ns = list(filtered(ns, *pattern))
    log.debug('NS: %s' % ', '.join(ns))

    data = parsedns(target.tld, qtype="AXFR", server=ns, protocol='tcp')
    if not data: return

    target.axfr = True
    target.zone.update(data)
    cprint('AXFR!!!', '+')
