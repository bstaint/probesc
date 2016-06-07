#!/usr/bin/env python
# coding: utf-8
import re
from urlparse import urlparse
from libs.utils import cprint, matched

pattern = {
    'powered': {
        'ASP/ASPX': ['asp'],
        'PHP': ['php']
    },
    'cookie': {
        'JSP': ['JSESSIONID'],
        'PHP': ['PHPSESSID'],
        'ASP/ASPX': ['ASPSESSION', 'ASP.NET']
    },
    'ext': {
        'PHP': ['.php'],
        'JSP': ['.jsp', '.action', '.do'],
        'ASP/ASPX': ['.asp', '.aspx', '.ashx']
    },
    'build': {
        'PHP': ['PHP'],
        'JSP': ['J2EE', 'Spring'],
        'ASP/ASPX': ['ASP'],
    }
}

def check_match(content, type, func=None):
    for key, val in pattern[type].iteritems():
        if matched(content, *val, func=func):
            return key
    return False

def url_extract(content, host):
    ''' 获取页面url '''
    pattern = '=(?:"|\')?([^ ]+)\.(php|asp|aspx|jsp|action|do)(?= |"|\'|\?|\/)'
    for m in re.finditer(pattern, content):
        parsed_url = urlparse('.'.join(m.group(1, 2)))
        if parsed_url.netloc in ['', host]:
            return parsed_url.path
    return u''

def output(target):
    '''
    name: Script Guess
    priority: 8
    depends: request
    version: 0.2
    '''
    if not getattr(target, 'data', None): return
    # 检测URL后缀
    url = url_extract(target.data['content'], target.host)
    target.script = check_match(url, 'ext', unicode.endswith) 
    log.debug('URL: %s' % url)

    if not target.script: # COOKIES
        target.script = check_match(target.data['cookies'], 'cookie')
    # 检测buildwith
    if not target.script:
        context = getattr(target, 'raw_build', '')
        match = re.search('framework\/([^"]+)"><', context)
        if match:
            target.script = check_match(match.group(1), 'build')
            log.debug('Match: %s' % match.group(1))
    # 检查x-powered-by
    if not target.script:
        context = target.data['headers'].get('x-powered-by', '')
        target.script = check_match(context, 'powered')
        log.debug('Powered: %s' % context)

    if target.script:
        cprint(target.script, '+')
