#!/usr/bin/env python
# coding: utf-8

from urlparse import urlsplit
from urlparse import urlunsplit

from thirds.tldextract import TLDExtract
from libs.net import valid_ip
from libs.exception import TargetWarning
from libs.exception import TargetError


class Target(object):

    prot = {'http': 80, 'https': 443}

    def __init__(self, url):
        parts = urlsplit(url)
        if not parts.netloc or parts.scheme not in self.prot:
            raise TargetError('target %s does not exist.' % url)

        self.host = parts.hostname
        self.ip = valid_ip(self.host)
        if not self.ip:
            raise TargetError('target %s can not resolv.' % self.host)

        self.port = parts.port if parts.port else self.prot[parts.scheme]
        self.scheme = parts.scheme
        self.path = parts.path if parts.path else '/'

    def geturl(self, path=None, ip=False):
        ''' 拼接url '''
        path = path if path else self.path
        netloc = '%s:%s' % (self.ip if ip else self.host, self.port)

        return urlunsplit((self.scheme, netloc, path, '', ''))

    @property
    def tld(self):
        if not getattr(self, '_tld', None):
            extract_domain = TLDExtract(include_psl_private_domains=True)
            self._tld = extract_domain(self.host).registered_domain
            if not self._tld:
                raise TargetWarning('%s not a public domain.' % self.host)

        return self._tld
