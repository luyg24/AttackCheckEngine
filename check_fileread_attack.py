# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
check file reading type attack! return id and vul
"""

import base64
import requests
import record_err

def check(id, hostname, url, method, status, postdata):
    try:
        print id, hostname, url, method, status, postdata
        print type(id), type(hostname), type(url), type(method), type(status), type(postdata)
        url = base64.b64decode(url)
        headers = {'user-agent':'Chrome/60.0.3112.113 Safarids24/537.36'}
        # print hostname, url, status, method
        if method.lower() == 'post':
            postdata = base64.b64decode(postdata)
            # print postdata
        if method.lower() == 'get':
            httpurl = 'http://' + hostname + url
            httpsurl = 'https://' + hostname + url
            print httpurl, httpsurl
            r = requests.get(httpurl, headers)
            print 'httpurl', r.text
            r = requests.get(httpsurl, headers)
            print 'httpsurl', r.text
    except Exception as e:
        record_err.logrecord()

