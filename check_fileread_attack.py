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
            r1 = requests.get(httpurl, headers = headers)
            tmp = str(r1)
            tmp1 = tmp.split()
            if re.search('200', tmp1[1]):
                httpcontent = r1.text
                content_process(httpcontent)
            r2 = requests.get(httpsurl, headers = headers, verify = False)
            tmp = str(r1)
            tmp1 = tmp.split()
            if re.search('200', tmp1[1]):
                httpscontent = r2.text
                content_process(httpscontent)
    except Exception as e:
        record_err.logrecord()

def content_process(content):
    try:
        print content
    except Exception as e:
        record_err.logrecord()

