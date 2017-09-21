# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
attack catagory and delete the same line, the list write to file!
"""

import record_err
import load_write_listfile
import write_todb
import linecache
import commands
import time

# filereadlist = []
# xsslist = []
# sqlinject = []
def catagory(attack_data):
    try:
        duplicatedfile = '/tmp/duplicate_attack.txt'
        dupfile = open(duplicatedfile, 'a')
        # load list
        # print load_write_listfile.checkfile()
        filereadlist, xsslist, sqlilist = load_write_listfile.checkfile()
        count = 0
        # tmp means hostname and url, join the new url+host and match if it is in the loaded list
        tmp = attack_data[u'url'] + attack_data[u'hostname']
        if attack_data[u'attack_type'] == u'文件读取' and attack_data[u'status'] == 200:
            # global filereadlist
            if tmp not in filereadlist:
                filereadlist.append(tmp)
                dupfile.write(str(attack_data))
                count += 1
            # print attack_data
        elif attack_data[u'attack_type'] == u'XSS攻击' and attack_data[u'status'] == 200:
            # global xsslist
            if tmp not in xsslist:
                xsslist.append(tmp)
                dupfile.write(str(attack_data))
                count += 1
        elif attack_data[u'attack_type'] == u'SQL注入' :
            # global sqlinject
            if tmp not in sqlilist:
                sqlilist.append(tmp)
                dupfile.write(str(attack_data))
                count += 1
        else:
            pass
        if count > 0:
            # write the new list to file
            dupfile.close()
            load_write_listfile.writelist(filereadlist, xsslist, sqlilist)
    except Exception as e:
        record_err.logrecord()

if __name__ == '__main__':
    print __name__