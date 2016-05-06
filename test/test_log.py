#!/usr/bin/env python
# coding: utf-8

import unittest
import logging
from libs.log import Logger

class UtilsTestCase(unittest.TestCase):

    def test_plugin(self):
        logger = Logger('test', 'logs/test.log')

        log1 = logger.get('Whois')
        log1.debug("test")


if __name__ == '__main__':
     unittest.main(verbosity=2)

