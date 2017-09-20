# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
write info to db
"""

import mysql.connector
import record_err
import linecache
import commands
import time

def writedb(conf):
    pass


def getinfo(filename):
    file = open(filename, 'r')
    config = {}
    content = file.readlines()
    for i in range(len(content)):
        tmp = content[i].split(':')
        key = tmp[0]
        value = tmp[1].split('\n')[0]
        print key, value
    # print content


if __name__ == '__main__':
    # print __name__
    getinfo('ids_mysql.conf')