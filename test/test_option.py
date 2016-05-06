#!/usr/bin/env python
# coding: utf-8               
from libs import option

def test():
    print option
    print {k:option[k] for k in ['headers', 'timeout']}

test()
