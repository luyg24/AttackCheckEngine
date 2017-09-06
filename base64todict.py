# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
base64 convert to dict
"""
import base64
import sys


def b64convertdict(base64string):

    try:
        request_header = {}
        post_data = ''
        base64string = base64string
        string = base64.b64decode(base64string)
        b64list = string.split('\r\n')
        method = b64list[0].split(' ')[0]
        request_header['method'] = method
        url = b64list[0].split(' ')[1]
        request_header['url'] = url
        protocol = b64list[0].split(' ')[2]
        request_header['protocol'] = protocol
        b64list.remove(b64list[0])
        method = method.upper()
        if method == 'POST':
            post_data = b64list[len(b64list)-1]
            b64list.remove(post_data)
        for i in range(len(b64list)):
            if len(b64list[i])>= 3:
                tmp = b64list[i].split(':')
                key = tmp[0]
                value = tmp[1]
                request_header[key] = value
        if method == 'POST' or method == 'GET':
            return request_header
        else:
            return 'other method or error!'
    except Exception, e:
        print 'base64string: %s, string: %s' % (base64string, string)
# 从命令行获取base64字符串
b64 = sys.argv[1]
# print b64
print b64convertdict(b64)
