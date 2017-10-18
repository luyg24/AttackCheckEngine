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
        if type(data) == "<type 'dict'>":
            if len(data) > 1:
                print data.keys()
        else:
            print 'not dict type!'


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
        return content

syspath = '/tmp/test1.json'
fromline = 0
readfile = File(syspath, fromline)
filelines = readfile.count()
while True:
    if filelines > fromline:
        #证明文件有新增内容需要继续读取,fromline＋1代表上次执行到了fromline行，这次从＋1行开始
        for fromline in range(fromline + 1, filelines + 1, ):
            readfile = File(syspath, fromline)
            content = readfile.read()
            #使用eval将原本数据外面的引号去除，这里因为原来的数据是dict，所以新的content现在是dict
            content = eval(content)
            #进行下一步处理，流量整形,获取到最新的数据
            newcontent = DataFlow(content)
    else:
        print fromline
        time.sleep(10)
        readfile = File(syspath, fromline)
        filelines = readfile.count()


