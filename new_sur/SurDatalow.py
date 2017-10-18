# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
read from suricata log file use data flow
"""

import record_err
import commands
import linecache
import time
import datetime
import sys


reload(sys)
sys.setdefaultencoding('utf8')


class DataFlow(object):
    def __init__(self, data):

        print data.keys()


class File(object):
    def __init__(self, filepath, startline=1):
        self.filepath = filepath
        self.startline = startline
        print filepath, startline

    def count(self):
        #返回文件行数
        status, output = commands.getstatusoutput('wc -l %s' %self.filepath)
        output = output.split()
        return int(output[0])

    def read(self):
        #每次读取一行内容
        content=linecache.getline(self.filepath)

        print 'reading file per line'


syspath = '/tmp/test1.json'
fromline = 1
readfile = File(syspath, fromline)
filelines = readfile.count()
for i in range(fromline, filelines + 1, ):
    print i

