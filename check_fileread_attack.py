# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
check file reading type attack! return id and vul
"""

import base64


def check(id, hostname, url, method, status, postdata):
    url = base64.b64decode(url)
    print hostname, url, status, method
    if method.lower() == 'post':
        postdata = base64.b64decode(postdata)
        print postdata