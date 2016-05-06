#!/usr/bin/env python
# coding: utf-8               
from libs.utils import filtered

ext = {
    'PHP': ['.php'],
    'JSP': ['.jsp', '.action', '.do'],
    'ASP/ASPX': ['.asp', '.aspx', '.ashx']
}

def matched(patterns, context, func=None):
    #转换为str类型
    if not isinstance(context, basestring):
        context = str(context)
    if not func:  # 默认执行函数
        func = lambda x, y: y in x

    if any(func(context, pattern) for pattern in patterns):
        return True

def check_match(content, func=None):
    for key, val in ext.iteritems():
        if matched(val, content, func=func):
            return key

    return False

# print check_match('/index.php', str.endswith)
# print matched(['cdn1', 'cdn2'], 'safdjlktjlkasdf cdn1')

print next(filtered(['tesasfdasdf123', 'kbsfadsd'], 'tesa'))
