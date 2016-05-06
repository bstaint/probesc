#!/usr/bin/env python
# coding: utf-8
import logging


class Logger(object):
    ''' 日志记录类 '''
    def __init__(self, name, src_dir):
        self.name = name
        self.handler = logging.FileHandler(src_dir, 'w')
        self.handler.addFilter(logging.Filter(name))
        # 日志格式
        fmt = logging.Formatter('[%(levelname)s] [%(name)s] %(message)s')
        self.handler.setFormatter(fmt)

    def get(self, name):
        logger = logging.getLogger('%s.%s' % (self.name, name))
        logger.setLevel(logging.DEBUG)
        logger.addHandler(self.handler)
        return logger
