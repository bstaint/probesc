#!/usr/bin/env python
# coding: utf-8

import subprocess

for domain in [
    "google.com",
    "facebook.com",
    "youtube.com",
    "baidu.com",
    "yahoo.com",
    "amazon.com",
    "wikipedia.org",
    "qq.com",
    "google.co.in",
    "twitter.com",
    "live.com",
    "taobao.com",
    "msn.com",
    "yahoo.co.jp",
    "linkedin.com",
    "sina.com.cn",
    "google.co.jp",
    "weibo.com",
    "bing.com",
    "yandex.ru"]:
    p = subprocess.Popen(["python probesc.py http://www.%s -m whois" % domain], shell=True)
    p.wait()
