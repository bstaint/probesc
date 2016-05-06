#!/usr/bin/env python
# coding: utf-8
import itertools
from libs.net import parsedns

def output(target, opts = None):
    '''
    name: DNS Zone Query
    priority: 1
    version: 0.2
    '''
    target.zone = {}
    hosts = [target.tld]
    qtypes = ['A', 'CNAME', 'NS', 'MX', 'SOA']

    if target.host in hosts:
        hosts.append('www.' + target.host)
    else:
        hosts.append(target.host)

    for host, type in itertools.product(hosts, qtypes):
        target.zone.update(parsedns(host, qtype=type))

    # 将SOA作为NS记录处理
    target.zone.setdefault('NS', [])
    target.zone['NS'] += target.zone.pop('SOA', [])
