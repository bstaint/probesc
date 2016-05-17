#!/usr/bin/env python
# coding: utf-8

import unittest

from libs.utils import *

class UtilsTestCase(unittest.TestCase):

    def test_cprint(self):
        cprint("test")
        cprint("test", '-')
        cprint("test", '+')
        cprint("test", '*', True)


if __name__ == '__main__':
     unittest.main(verbosity=2)

