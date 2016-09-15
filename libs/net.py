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
    ipaddr = None
    fake_domain = 'notexistsfuckispsbbaidu.com'

    try:
        # 防止ISP劫持
        if not hasattr(valid_ip, 'fake_ip'):
            try: valid_ip.fake_ip = socket.gethostbyname(fake_domain)
            except socket.error: valid_ip.fake_ip = None

        _,_,ipaddrs = socket.gethostbyname_ex(host)

        if ipaddrs[0] != valid_ip.fake_ip:
            ipaddr = ipaddrs[0]
    except socket.error:
        pass
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
    params = kwargs.pop('params', None)

    pattern = re.compile('charset=(?:")?(?P<chatset>[a-zA-Z0-9\-]+)')
    opts = {
        'headers': kwargs.pop('headers', option['headers']),
        'timeout': kwargs.pop('timeout', option['timeout']),
        'verify': False
    }
    try:
        if params:
            req = requests.post(url, params=params, **opts)
        else:
            req = requests.get(url, **opts)
        # 获取编码
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
