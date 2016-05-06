#!/usr/bin/env python
# coding: utf-8

import unittest
import logging
from libs.net import *

class UtilsTestCase(unittest.TestCase):

    def test_urlopen(self):
        print urlopen('http://localhost/', attr=('content', ''))

    def test_ssl_cert(self):
        print ssl_cert('www.baidu.com')


if __name__ == '__main__':
     unittest.main(verbosity=2)
