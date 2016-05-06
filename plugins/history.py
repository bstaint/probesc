#!/usr/bin/env python
# coding: utf-8
import re
from datetime import datetime
from operator import itemgetter

from libs.net import urlopen
from libs.utils import cprint

apis_url = [
    ('http://toolbar.netcraft.com/site_report?url=%s', '<td>(?P<ip>\d{1,3}.*?)<\/td>[\s\S]*?(?P<date>\d{1,2}-\w{3}-\d{4})<\/td>', '%d-%b-%Y'),
    ('http://site.ip138.com/%s/', 'date.+?>(?P<date>.+?)--.+>[\s\S]*?\/(?P<ip>.+?)\/', '%Y-%m-%d'),
]

def output(target):
    '''
    name: Hosting History
    priority: 8
    depends: cdn
    version: 0.1
    '''
    if not getattr(target, 'cdn', False): return
    ipdate = set()

    for url, regex, fmt in apis_url:
        content = urlopen(url % target.host, attr=('text', ''))
        for m in re.finditer(regex, content):
            date = datetime.strptime(m.group('date'), fmt)
            ipdate.add((m.group('ip'), date))

    for ip, date in sorted(ipdate, key=itemgetter(1)):
        cprint('%s %s' % (ip, date.strftime('%Y-%m-%d')), '+')
