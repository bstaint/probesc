#!/usr/bin/env python
# coding: utf-8

import unittest
from libs.target import Target

class UtilsTestCase(unittest.TestCase):

    def test_target(self):
        target = Target('https://f.szbaixin.cn:8/')
        self.assertEqual(target.port, 8)

    def test_target_default_port(self):
        target = Target('https://www.baidu.com/')
        self.assertEqual(target.port, 443)


if __name__ == '__main__':
     unittest.main(verbosity=2)

