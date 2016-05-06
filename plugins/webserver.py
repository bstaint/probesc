#!/usr/bin/env python
# coding: utf-8
import re
import itertools
from urlparse import urlparse

from libs.utils import cprint
from libs.net import urlopen


def urlsrc(content, host):
    ''' 获取src文件url '''
    pattern = '=["|\']([^ |\'|"]+)\.(js|css|gif|jpg|png|ico)["|\'|\?]'
    for m in re.finditer(pattern, content):
        parsed_url = urlparse('.'.join(m.group(1,2)))

        if parsed_url.netloc in ['', host]:
            return parsed_url.path
    return 'robots.txt'

def output(target):
    '''
    name: WebServer Parser
    priority: 8
    depends: request
    '''
    if not getattr(target, 'data', None): return
    server = target.data['headers'].get('server', '')

    if 'nginx' in server:
        cprint('testing nginx parsing vulnerability...')
        path = urlsrc(target.data['content'], target.host)

        url = target.geturl(path)
        log.debug('URL: %s' % url)

        for url in itertools.product([url], ['/.php', '/1.php']):
            req = urlopen(''.join(url))
            if req and not req.history and \
               'text/html' in req.headers['content-type']:
                cprint('nginx bad!', '+'); break
    elif 'iis' in server:
        pass
    elif 'apache' in server:
        pass
