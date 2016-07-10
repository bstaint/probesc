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

    def test_option_input(self):
        # option_input.slient = True
        print option_input();
        print option_input('1 2 4: ', [1,2,4], '7');


if __name__ == '__main__':
     unittest.main(verbosity=2)

