# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
read from file by line, flow data!
"""

import linecache
import commands
import time
import datetime


def readfile(line):
    pass


def filename(logfile, file_count, startline=1):
    try:
        #控制读取次数
        for i in range(file_count- startline + 1):
            print linecache.getline(logfile, startline)
            startline += 1
        #已处理到多少行
        linecache.clearcache()
        return startline - 1
    except Exception as e:
        logfile = open('log.txt', 'a')
        localtime = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
        logfile.write('%s:%s:%s.processed_line:%d\n' % (localtime, Exception, e, startline-1))
        logfile.close()

def filecount(logfile):
    stats, output = commands.getstatusoutput('wc -l %s' % (logfile))
    count = int(output.split()[0])
    return count

logfile = 'test_data.txt'
# 获取文件行数
file_count = filecount(logfile)
processed_line = filename(logfile, file_count, 1)
while 1:
    file_count = filecount(logfile)
    if file_count > processed_line:
        processed_line = filename(logfile, file_count, processed_line+1)
    time.sleep(3)