# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
base64 convert to dict, default logfile 'log.txt'
"""
import base64
import sys
import create_requestheader
import datetime


def b64convertdict(base64string):

    try:
        fun_status = 1
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
            request_header['postdata'] = post_data
        for i in range(len(b64list)):
            if len(b64list[i])>= 3:
                tmp = b64list[i].split(':')
                key = tmp[0]
                value = tmp[1]
                request_header[key] = value
        if method == 'POST' or method == 'GET':
            # print type(request_header)
            return request_header
        else:
            fun_status = 0
            return fun_status
    except Exception as e:
        request_header = base64string
        logfile = open('log.txt', 'a')
        # print Exception,':', e
        localtime = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
        logfile.write('%s:%s:%s.ori_string:%s' %(localtime, Exception, e, request_header))
        fun_status = 0
        return fun_status
        logfile.close()
        # return 'program error!'
        # print 'base64string: %s, string: %s' % (base64string, string)
# 从命令行获取base64字符串,注意一定是base64哦!
# b64 = sys.argv[1]
b64 = 'R0VUIC9teWFkbWluL3NjcmlwdHMvc2V0dXAucGhwIEhUVFAvMS4xDQpBY2NlcHQ6ICovKg0KQWNjZXB0LUxhbmd1YWdlOiBlbi11cw0KQWNjZXB0LUVuY29kaW5nOiBnemlwLCBkZWZsYXRlDQpVc2VyLUFnZW50OiBabUV1DQpIb3N0OiAxMjIuMTE1LjQ4LjU0DQpDb25uZWN0aW9uOiBDbG9zZQ0KWC1Gb3J3YXJkZWQtRm9yOiAxNDYuMTg1LjE2Ni4xMjcNCg0K'
b64 = 'hello'
# print b64
request_header = b64convertdict(b64)
# print request_header
if request_header != 0:
    create_requestheader.createfile(request_header)
else:
    print 'last func errors!'
