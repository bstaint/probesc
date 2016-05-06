#!/usr/bin/env python
# coding: utf-8

import nmap
from libs.utils import cprint

ports = set([
    21, 22, 23, 25, 80, 81,
    110, 135, 139, 389, 443, 445, 873,
    1433, 1434, 1521, 2433, 3306, 3307, 3336,
    3380, 3389, 3968, 5800, 5900, 7001, 7755,
    8000, 8001, 8002, 8080, 8650, 8888, 8800, 8880, 9999,
    12580, 22222, 22022, 27017, 28017, 33089, 34567, 43958, 50001
])

def output(target):
    '''
    name: Nmap Ports Scaner
    depends: cdn
    priority: 7
    version: 0.1
    '''
    if getattr(target, 'cdn', True): return

    nm = nmap.PortScanner()
    # nm.scan(target.ip, ','.join(map(str, ports)), arguments='-T4 -A')
    nm.scan(target.ip, ','.join(map(str, ports)))

    if 'tcp' not in nm[target.ip]: return

    target.ports = []
    # target.os = nm[target.ip]['osmatch'][0]['name']

    for key,val in nm[target.ip]['tcp'].items():
        target.ports.append(key)

    target.ports.sort()
    # cprint('OS: %s' % target.os, '+')
    cprint('Ports: %s' % ', '.join(map(str, target.ports)), '+')
