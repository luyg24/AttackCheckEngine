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

    def count(self):
        #返回文件行数
        status, output = commands.getstatusoutput('wc -l %s' %self.filepath)
        output = output.split()
        return int(output[0])

    def read(self):
        #每次读取一行内容
        content=linecache.getline(self.filepath, self.startline)
        print content

syspath = '/tmp/test1.json'
fromline = 1
readfile = File(syspath, fromline)
filelines = readfile.count()
while True:
    if filelines > fromline:
        #证明文件有新增内容需要继续读取
        for fromline in range(fromline, filelines + 1, ):
            readfile = File(syspath, fromline)
            readfile.read()
    else:
        print fromline
        time.sleep(10)
        readfile = File(syspath, fromline)
        filelines = readfile.count()


