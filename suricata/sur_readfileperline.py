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
import json
import datetime


def readfile(content):
    # change str to dict
    try:
        new_dict = {}
        # if content is json str, convert to dict
        con_dict = json.loads(content)
        # check if content is http or not
        conkey = con_dict.keys()
        if u'http' in conkey:
            new_dict['http'] = con_dict[u'http']
            if u'src_ip':
                new_dict['src_ip'] = con_dict[u'src_ip']
            if u'src_port' in conkey:
                new_dict['src_port'] = con_dict[u'src_port']
            if u'dest_ip' in conkey:
                new_dict['dest_ip'] = con_dict[u'dest_ip']
            if u'dest_port' in conkey:
                new_dict['dest_port'] = con_dict[u'dest_port']
            if u'timestamp' in conkey:
                new_dict['datetime'] = con_dict[u'timestamp']
            if u'alert' in conkey:
                new_dict['alert'] = con_dict[u'alert'][u'signature']

            print new_dict
        else:
            print conkey
        # get http attack type and info
        if con_dict[u'subproto']:
            if con_dict[u'subproto'] == 'http':
                new_dict[u'attack_type'] = con_dict[u'attack_type']
                new_dict[u'hostname'] = con_dict[u'hostname']
                new_dict[u'url'] = con_dict[u'url']
                new_dict[u'method'] = con_dict[u'method']
                new_dict[u'status'] = con_dict[u'status']
                if con_dict[u'method'] == 'POST':
                    new_dict[u'post'] = con_dict[u'postdata']
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
            file_record = open('file_no.txt', 'w')
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
    fileinfo('abc.txt', 2)