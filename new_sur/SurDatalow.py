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
    def __init__(self, filepath, startline=0):
        self.filepath = filepath
        self.startline = startline

    def count(self):
        #返回文件行数
        status, output = commands.getstatusoutput('wc -l %s' %self.filepath)
        output = output.split()
        return int(output[0])

    def read(self):
        #更新一下缓存,避免新增内容获取不到
        linecache.checkcache(self.filepath)
        #每次读取一行内容
        content=linecache.getline(self.filepath, self.startline)
        print self.startline, content

syspath = '/tmp/test1.json'
fromline = 0
readfile = File(syspath, fromline)
filelines = readfile.count()
while True:
    if filelines > fromline:
        #证明文件有新增内容需要继续读取,fromline＋1代表上次执行到了fromline行，这次从＋1行开始
        for fromline in range(fromline + 1, filelines + 1, ):
            readfile = File(syspath, fromline)
            readfile.read()
    else:
        print fromline
        time.sleep(10)
        readfile = File(syspath, fromline)
        filelines = readfile.count()


