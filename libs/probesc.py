#!/usr/bin/env python
# coding: utf-8
import os
import glob
import socket
from itertools import chain

from libs import option
from libs.utils import cprint, option_input
from libs.log import Logger
from libs.target import Target
from libs.plugin import Plugins
from libs.exception import *


class ProbeEngine(object):

    def __init__(self, args):
        modules = args.modules or self.find_modules('plugins')
        self.queue = Plugins(modules, 'plugins').queue
        self.target = Target(args.url)
        # 日志类
        self.logger = Logger('probesc', 'logs/%s.log' % self.target.host)
        # 参数配置
        self.target.redirect = args.redirect
        option_input.silent = args.silent

    def find_modules(self, src_dir):
        ''' 查找插件模块 '''
        for fn in glob.glob1(src_dir, '[!_]*.py'):
            yield os.path.splitext(fn)[0]

    def execute(self, name, func):
        ''' 执行插件，捕获异常 '''
        try:
            func.func_globals.update(log=self.logger.get(name))
            func(self.target)
        except (PluginWarning, TargetWarning), e:
            cprint('[%s] %s' % (name, e), '*')
        except Exception, e:
            raise PluginError('[%s] %s' % (name, e))

    def pentest(self):
        for name, func in self.queue.pop('1', []):
            self.execute(name, func)

        if not self.queue.values(): return
        cprint('testing all plugins from target', '*', True)
        # {'2' : [...], '3': [...]}
        items = sorted(self.queue.items())

        for name, func in chain(*[vals for _, vals in items]):
            cprint('testing plugin %s' % name)
            self.execute(name, func)
