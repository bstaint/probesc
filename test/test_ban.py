#!/usr/bin/env python
# coding: utf-8


from libs.utils import filtered, matched, json_dict

banners = json_dict('settings.json').pop('banners')

print 'filter: ', list(filtered(['ns1.dnsv2.com', 'custom.test.com'], banners['ns']))
print 'matched: ', matched(['custom.test.com'], banners['ns'])
print 'filter match: ', next(filtered(['ns1.dnsv2.com'], banners['ns']), None)
