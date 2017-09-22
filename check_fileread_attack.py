# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
check file reading type attack! return id and vul
"""

import base64
import requests
import record_err
import re

def check(id, hostname, url, method, status, postdata):
    try:
        result1 = ''
        result2 = ''
        # print id, hostname, url, method, status, postdata
        # print type(id), type(hostname), type(url), type(method), type(status), type(postdata)
        url = base64.b64decode(url)
        headers = {'user-agent':'Chrome/60.0.3112.113 Safarids24/537.36'}
        if method.lower() == 'post':
            postdata = base64.b64decode(postdata)
            # print postdata
        if method.lower() == 'get':
            httpurl = 'http://' + hostname + url
            httpsurl = 'https://' + hostname + url
            try:
                r1 = requests.get(httpurl, headers = headers)
            except:
                r1 = ''
            if r1 is not '':
                tmp1 = str(r1)
                tmp2 = tmp1.split()
                httpstatus = tmp2[1]
                if httpstatus:
                    if re.search('200', httpstatus):
                        httpcontent = r1.text
                        id, result1 = content_process(id, httpcontent)
            try:
                r2 = requests.get(httpsurl, headers = headers, verify = False)
            except:
                r2 = ''
            if r2 is not '':
                print r2
                result = ''
                tmp3 = str(r2)
                tmp4 = tmp3.split()
                httpsstatus = tmp4[1]
                if httpsstatus:
                    if re.search('200', httpsstatus):
                        httpscontent = r2.text
                        id, result2 = content_process(id, httpscontent)
        print id, result1, result2

    except Exception as e:
        record_err.logrecord()

def content_process(id, content):
    try:
        if len(content) == 0:
            result = 'N'
            print 'no vul'
            return id, result
        else:
            pass
    except Exception as e:
        record_err.logrecord()

