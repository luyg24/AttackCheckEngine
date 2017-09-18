# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
read from file by line, flow data!
usage: give a filename, and start line
fileinfo(filename, startline)
"""

import record_err
import linecache
import commands
import time
import datetime


def readfile(content):
    print content


def filename(logfile, file_count, startline):
    try:
        # 控制读取次数
        for i in range(file_count-startline+1):
            content = linecache.getline(logfile, startline)
            readfile(content)
            startline += 1
        # 已处理到多少行
        linecache.clearcache()
        return startline - 1
    except Exception as e:
        record_err.logrecord()


def filecount(logfile):
    stats, output = commands.getstatusoutput('wc -l %s' % (logfile))
    count = int(output.split()[0])
    return count


def fileinfo(logfile, start_line=1):
    # 获取文件行数
    file_count = filecount(logfile)
    processed_line = filename(logfile, file_count, start_line)
    while 1:
        file_count = filecount(logfile)
        if file_count > processed_line:
            processed_line = filename(logfile, file_count, processed_line+1)

        time.sleep(3)


#fileinfo('abc.txt', 2)