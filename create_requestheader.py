# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
create request header file, default path: "/data/tmp/attack_engine"
"""
import sys
import string
import random
import sql_inject_engine

def createfile(request_header):
    try:
        #生成16位文件名
        filepath = '/data/tmp/attack_engine/'
        tmpname = ''.join(random.sample(string.ascii_letters + string.digits, 16))
        filename = filepath+tmpname
        # 写文件
        file = open(filename, 'a')
        method = request_header['method']
        line1 = request_header['method'] + ' ' + request_header['url'] + ' ' + request_header['protocol']
        del request_header['method']
        del request_header['url']
        del request_header['protocol']
        # print line1
        file.write(line1)
        file.write('\n')
        if method == 'POST':
            postdata = request_header['postdata']
            del request_header['postdata']
        for k, v in request_header.items():
            file.write('%s:%s\n' %(k, v))
        if method == 'POST':
            file.write('\n')
            file.write(postdata)
        file.close()
        sql_inject_engine.runsqlmap(filename)
    except Exception as e:
        print Exception, e
        print 'error'
#获取request header 注意是dict格式
# request_header = {'method': 'GET', 'test': ' df'}
# request_header = sys.argv[1]
# createfile(request_header)
# print request_header, type(request_header)
# createfile(request_header)