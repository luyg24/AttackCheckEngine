# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
read from file by line, flow data!
"""

import linecache
import commands


def readfile(line):
    pass


def filename(logfile, startline=1):
    # print logfile, startline
    print linecache.getline(logfile, startline)
    #return startline

def filecount(logfile):
    stats, output = commands.getstatusoutput('wc -l %s' % (logfile))
    count = int(output.split()[0])
    return count

logfile = 'test_data.txt'
# 获取文件行数
file_count = filecount(logfile)
filename(logfile, 1)

