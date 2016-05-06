#!/usr/bin/env python
# coding: utf-8

import unittest
from libs.plugin import Plugins

class UtilsTestCase(unittest.TestCase):

    def test_plugin(self):
        queue = Plugins(['iphistory'], 'plugins').queue

    def test_param(self):
        doc = '''
    name: CDN Checker
    priority: 8
    depends: request,dns
    version: 0.1
    '''
        print Plugins.parse(doc)


if __name__ == '__main__':
     unittest.main(verbosity=2)

