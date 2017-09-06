# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
create request header file, default path: "/data/tmp/attack_engine"
"""
import sys
import string
import random

def createfile(request_header):
    try:
        #生成16位文件名
        filename = ''.join(random.sample(string.ascii_letters + string.digits, 16))
        print type(request_header)
        print request_header['method']
    except Exception, e:
        print 'error'
#获取request header 注意是dict格式
# request_header = {'method': 'GET', 'test': ' df'}
# request_header = sys.argv[1]
# createfile(request_header)
# print request_header, type(request_header)
# createfile(request_header)