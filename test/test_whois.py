#!/usr/bin/env python
# coding: utf-8

import re
from thirds.pythonwhois import get_whois

def preprocess_regex(regex):
    # Fix for #2; prevents a ridiculous amount of varying size permutations.
    regex = re.sub(r"\\s\*\(\?P<([^>]+)>\.\+\)", r"\s*(?P<\1>\S.*)", regex)
    # Experimental fix for #18; removes unnecessary variable-size whitespace
    # matching, since we're stripping results anyway.
    regex = re.sub(r"\[ \]\*\(\?P<([^>]+)>\.\*\)", r"(?P<\1>.*)", regex)
    return regex

content = '''
'''
regex = preprocess_regex('')
match = re.search(regex, content)
print match
# req = get_whois('baidu.com')
# print req
