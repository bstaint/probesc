#!/usr/bin/env python
# coding: utf-8


class TargetWarning(Exception):
    ''' 目标警告异常 '''

class TargetError(Exception):
    ''' 目标解析错误 '''

class PluginWarning(Exception):
    ''' 插件警告异常 '''

class PluginError(Exception):
    ''' 插件严重错误异常 '''
