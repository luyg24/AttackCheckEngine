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
        file = open('/tmp/attackinfo.txt', 'a')
        count = 0
        if attack_data[u'attack_type'] == u'文件读取' and attack_data[u'status'] == 200:
            global filereadlist
            if attack_data not in filereadlist:
                filereadlist.append(attack_data)
                count += 1
            # print attack_data
        elif attack_data[u'attack_type'] == u'XSS攻击' and attack_data[u'status'] == 200:
            global xsslist
            if attack_data not in xsslist:
                xsslist.append(attack_data)
                count += 1
        elif attack_data[u'attack_type'] == u'SQL注入' :
            global xsslist
            if attack_data not in xsslist:
                xsslist.append(attack_data)
                count += 1
        else:
            pass
        if count > 0:
            file.write(str(attack_data))
            file.write('\n')
            file.close()

    except Exception as e:
        record_err.logrecord()