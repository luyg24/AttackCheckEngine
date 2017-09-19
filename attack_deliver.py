# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
attack catagory and delete the same line
"""

import record_err
import linecache
import commands
import time

filereadlist = []
xsslist = []
def catagory(attack_data):
    try:
        if attack_data[u'attack_type'] == u'文件读取' and attack_data[u'status'] == 200:
            global filereadlist
            if attack_data not in filereadlist:
                filereadlist.append(attack_data)
            print filereadlist
            # print attack_data
        elif attack_data[u'attack_type'] == u'XSS攻击' and attack_data[u'status'] == 200:
            global xsslist
            if attack_data not in xsslist:
                xsslist.append(attack_data)
            print xsslist
    except Exception as e:
        record_err.logrecord()