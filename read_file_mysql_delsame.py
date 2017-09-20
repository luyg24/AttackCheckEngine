# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
attack catagory and delete the same line
"""

import record_err
import write_todb
import linecache
import commands
import time

filereadlist = []
xsslist = []
sqlinject = []
def catagory(attack_data):
    try:
        count = 0
        # tmp means hostname and url
        tmp = attack_data[u'url'] + attack_data[u'hostname']
        if attack_data[u'attack_type'] == u'文件读取' and attack_data[u'status'] == 200:
            global filereadlist
            if tmp not in filereadlist:
                filereadlist.append(tmp)
                count += 1
            # print attack_data
        elif attack_data[u'attack_type'] == u'XSS攻击' and attack_data[u'status'] == 200:
            global xsslist
            if tmp not in xsslist:
                xsslist.append(tmp)
                count += 1
        elif attack_data[u'attack_type'] == u'SQL注入' :
            global sqlinject
            if tmp not in sqlinject:
                sqlinject.append(tmp)
                count += 1
        else:
            pass
        if count > 0:
            print attack_data
            # file.write(str(attack_data))
            # file.write('\n')
            # file.close()
    except Exception as e:
        record_err.logrecord()

if __name__ == '__main__':
    print __name__