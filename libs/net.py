#!/usr/bin/env python
# coding: utf-8
import re
import ssl
import socket
import requests
from collections import defaultdict

from libs import option
from thirds.DNS import DnsRequest

socket.setdefaulttimeout(option['timeout'])

if option['disable_ssl']:
    requests.packages.urllib3.disable_warnings()

def valid_ip(host):
    ''' lookup address with gethostbyname '''
    try:
        ipaddr = socket.gethostbyname_ex(host)[-1][0]
    except socket.error:
        ipaddr = None
    return ipaddr

def ssl_cert(host, port=443):
    ''' 获取ssl证书信息 '''
    ctx = ssl.create_default_context()
    s = ctx.wrap_socket(socket.socket(), server_hostname=host)
    try:
        s.connect((host, port))
        return s.getpeercert()
    except socket.error, e:
        return {}

def urlopen(url, **kwargs):
    ''' URL GET请求 '''
    attr = kwargs.pop('attr', (None, None))
    pattern = re.compile('charset=(?:")?(?P<chatset>[a-zA-Z0-9\-]+)')
    opts = {
        'headers': kwargs.pop('headers', option['headers']),
        'timeout': kwargs.pop('timeout', option['timeout']),
        'verify': False
    }
    try:
        req = requests.get(url, **opts)
        # 检测编码
        match = pattern.search(req.content)
        if match and req.encoding == 'ISO-8859-1':
            req.encoding = match.group('chatset')
        return getattr(req, *attr) if attr[0] else req
    except requests.exceptions.RequestException, e:
        return attr[1]

def parsedns(host, **kwargs):
    ''' 包装解析DNS请求 '''
    ns = kwargs.pop('server', option['ns'])
    zone = defaultdict(list)
    try:
        req = DnsRequest(host, server=ns, **kwargs).req()
        answers = req.answers
    except Exception, e:
        answers = {}
    for ans in answers:
        type, name, data = (ans['typename'], ans['name'], ans['data'])
        if type in ['A', 'CNAME']:
            zone[type].append((name, data))
        elif type is 'NS':
            zone[type].append((data,))
        elif type is 'MX':
            zone[type].append((data[1],))
        elif type is 'SOA':
            zone[type].append((data[0],))
    return zone
