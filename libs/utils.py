#!/usr/bin/env python
# coding: utf-8

import os
import sys
import json
import time
from glob import glob

from thirds.colorama import init
from thirds.colorama import Fore

init()


def process_ask(slient=False, msg='how do you want to proceed? (y/N) '):
    ''' 询问是否继续，用于跳过耗时长的操作 '''
    return slient or raw_input(msg).lower() == 'y'

def runtime(fmt='%H:%M:%S'):
    ''' 返回当前时间 '''
    return time.strftime(fmt)

def json_dict(src, **kwargs):
    ''' 读取json文件到dict '''
    try:
        data = json.load(open(src))
        data.update(kwargs)
    except (IOError, ValueError), e:
        return kwargs
    return data

def cprint(msg, flag='', wrap=False):
    ''' 根据标志输出信息 '''
    color = {
        '*': Fore.YELLOW,
        '-': Fore.LIGHTRED_EX,
        '+': Fore.LIGHTGREEN_EX
    }.get(flag, Fore.YELLOW)

    mark = flag if flag in ['*', '-', '+'] else runtime()
    prefix = ('\n' if wrap else '') + color + '[%s] ' % mark
    sys.stdout.write(prefix + msg + Fore.RESET + '\n')

def filtered(contexts, *args):
    ''' 字符串列表过滤 '''
    for context in contexts:
        if any(pattern in context for pattern in args):
            continue
        yield context

def matched(context, *args, **kwargs):
    ''' 字符串匹配 '''
    if not isinstance(context, basestring):
        context = str(context)
    # 默认操作函数
    func = kwargs.pop('func', None)
    if not func:
        func = lambda x, y: y in x

    if any(func(context, pattern) for pattern in args):
        return True
