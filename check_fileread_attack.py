# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
check file reading type attack! return id and vul
"""

import base64
import requests

def check(id, hostname, url, method, status, postdata):
    url = base64.b64decode(url)
    # print method
    headers = {'user-agent':'Chrome/60.0.3112.113 Safarids24/537.36'}
    # print hostname, url, status, method
    if method.lower() == 'post':
        postdata = base64.b64decode(postdata)
        # print postdata
    if method.lower() == 'get':
        # print hostname, url
        httpurl = 'http://' + hostname + url
        httpsurl = 'https://' + hostname + url
        r = requests.get(httpurl, headers)
        print 'httpurl', r.text
        r = requests.get(httpsurl, headers)
        print 'httpsurl', r.text

