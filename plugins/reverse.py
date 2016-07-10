#!/usr/bin/env python
# coding: utf-8
import re
from libs.utils import cprint
from libs.net import urlopen


apis = [
    ('http://www.cxw.com/domain/countercheckdomain?key=%s', '_blank\'>(.*?)</a>'),
    ('http://m.tool.chinaz.com/reverse/?host=%s&ddlSearchMode=1', 'DomainName=(.*?)"'),
    ('http://whois.aizhan.com/reverse-whois?q=%s&t=email', '"links.*?href="http://www.(.*?)/'),
    ('http://www.whoismind.com/email/%s.html', '&nbsp; <a href="\/whois\/([^>]+)\.html')
]

def output(target):
    '''
    name: Reverse Email Finder
    depends: whois
    '''
    if not getattr(target, 'domain', None): return

    domains = []
    for url, regex in apis:
        content = urlopen(url % target.domain[0], attr=('text', ''))
        domains.extend(re.findall(regex, content))

    target.email_domains = set(domains[:50])
    log.debug('DOMAINS: %s' % ', '.join(target.email_domains))

    print target.email_domains
