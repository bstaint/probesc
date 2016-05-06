#!/usr/bin/env python
# coding: utf-8
import re
from collections import defaultdict
from importlib import import_module

from libs.exception import PluginError


class Plugins(object):
    '''
    载入插件并根据优先级以及依赖来返回队列
    '''
    def __init__(self, modules, package=None):
        self._skip = set()
        self.queue = defaultdict(list)
        self.package = package
        map(self.__push, sorted(modules))

    def __push(self, modname):
        if self.package:
            modname = '.'.join([self.package, modname])

        if modname in self._skip: return
        try:
            func = getattr(import_module(modname), 'output')
            name, priority, depends = self.parse(func.func_doc)
        except (ImportError, AttributeError, ValueError), e:
            raise PluginError('[%s] %s' % (modname, e))

        map(self.__push, sorted(depends))
        self.queue[priority].append((name, func))
        self._skip.add(modname)

    @staticmethod
    def parse(doc):
        ''' 解析插件doc信息 '''
        regex = re.compile(r'(name|priority|depends): (.*?)\n')

        parts = dict(regex.findall(doc))
        if not parts.get('name', ''): return

        strip_val = parts.get('priority', '').strip()
        priority = strip_val if strip_val else '9'
        strip_val = parts.get('depends', '').strip()
        depends = strip_val.split(',') if strip_val else []

        return parts['name'], priority, depends
