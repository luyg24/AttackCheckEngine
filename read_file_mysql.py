# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
read from file by line, flow data!
usage: give a filename, and start line
fileinfo(filename, startline)
"""

import record_err
import attack_deliver
import linecache
import commands
import time
import json
import datetime


def readfile(content):
    # change str to dict
    try:
        print content, type(content)
        # dict_cont = json.loads(content)
        # attack_deliver.catagory(new_dict)
        # else , pass
    except Exception as e:
        record_err.logrecord()


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
    try:
        stats, output = commands.getstatusoutput('wc -l %s' % (logfile))
        count = int(output.split()[0])
        return count
    except Exception as e:
        record_err.logrecord()


def fileinfo(logfile, start_line=1):
    try:
    # 获取文件行数
        file_count = filecount(logfile)
        processed_line = filename(logfile, file_count, start_line)
        while 1:
            file_record = open('/tmp/file_no.txt', 'a')
            file_count = filecount(logfile)
            if file_count > processed_line:
                processed_line = filename(logfile, file_count, processed_line+1)
                # record the last processed line number
                file_record.write(str(processed_line))
                file_record.close()
            time.sleep(3)
    except Exception as e:
        record_err.logrecord()


if __name__ == '__main__':
    fileinfo('/tmp/attackinfo.txt', 1)