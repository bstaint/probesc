#!/usr/bin/env python
# coding: utf-8
from datetime import datetime

from libs.utils import cprint
from libs.utils import filtered
from libs.exception import PluginWarning

from thirds.pythonwhois import get_whois
from thirds.pythonwhois.shared import WhoisException


pattern = set([
    "protecteddomainservices",
    "whoisprivacyprotect",
    "whoisprotect",
    "yinsibaohu",
    "whoisagent",
    "dmctr.cn",
    "cndns.cn",
    "domainsbyproxy",
    "supervision",
    "privacyprotect",
    "cndns.com",
    "privacyguardian",
    "whoisguard",
    "west263.com",
    "gkg.net",
    "enamewhois.com",
    "privacy",
    'gandi.net',
    'topvhost.com'
])

def output(target):
    '''
    name: Whois
    priority: 1
    version: 0.2
    '''
    try:
        resp = get_whois(target.tld)
    except WhoisException, e:
        raise PluginWarning(e)

    for val in resp['contacts'].values():
        if val and 'email' in val:
            emails = [val['email'].lower()]; break
    else:
        if 'emails' in resp:
            emails = map(unicode.lower, resp['emails'])
        else: return
    print resp
    return

    log.debug('Email: %s' % ','.join(emails))
    email = next(filtered(emails, *pattern), None)
    if not email: return

    expired = resp.get('expiration_date', (None,))[0]
    target.domain = (email, expired)

    output = 'Email: %s' % email
    if expired:
        days = (expired - datetime.now()).days
        output += ', Expired Day: %d' % days
    cprint(output, '+')
