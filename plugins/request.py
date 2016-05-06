#!/usr/bin/env python
# coding: utf-8
from libs.net import urlopen
from libs.utils import cprint
from libs.exception import PluginWarning

def output(target):
    '''
    name: HTTP Request
    priority: 1
    version: 0.2
    '''
    req = urlopen(target.geturl())
    log.debug("encoding: " + req.encoding)

    if req is None: 
        raise PluginWarning('target %s connection refused' % target.host)

    target.data = {
        'headers': dict(req.headers.lower_items()),
        'cookies': req.cookies.get_dict(),
        'content': req.text,
        'robots' : urlopen(target.geturl('robots.txt'), attr=('text', ''))
    }
    log.debug('Headers: %s' % str(target.data['headers']))
    log.debug('Cookies: %s' % str(target.data['cookies']))

    if 'server' in req.headers:
        cprint('Server: %s' % req.headers['server'] , '+')

    target.raw_build = urlopen('http://builtwith.com/%s' % target.host,
                               attr=('text', ''))
