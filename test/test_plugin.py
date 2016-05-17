#!/usr/bin/env python
# coding: utf-8

import unittest
from libs.plugin import Plugins
from plugins.script import url_extract

class UtilsTestCase(unittest.TestCase):

    def test_plugin(self):
        queue = Plugins(['domains'], 'plugins').queue

    def test_param(self):
        doc = '''
    name: CDN Checker
    priority: 8
    depends: request,dns
    version: 0.1
    '''
        print Plugins.parse(doc)


    def test_url_ext(self):
        content = '''
<div class=foot_r><a href=http://210.76.65.188/ target=_blank><img src=http://xy.ixinyou.com/img/2012/0406/foot_nt2.jpg width=48 height=59 title=/></a><a href=http://210.76.65.188/webrecord/innernet/Welcome.jsp?bano=4404024022281 target=_blank><img src=http://xy.ixinyou.com/img/2012/0406/foot_nt3.jpg width=48 height=59></a><a href=http://www.ixinyou.com/web/jiazhang/ target=_blank><img src=http://xy.ixinyou.com/img/2012/0406/jiazhang.jpg width=48 height=59></a></div>
<a href="/1.php"
<a href='src.php'
<a src='1.php 


		  <div class="foot_l">
'''
        print url_extract(content, 'test')


if __name__ == '__main__':
     unittest.main(verbosity=2)

