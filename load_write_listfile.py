# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
test file
"""
import os
import commands


def checkfile():
    readfilepath = '/tmp/readfile.txt'
    xssfilepath = '/tmp/xss.txt'
    sqlfilepath = '/tmp/sqli.txt'
    filelist = [readfilepath, xssfilepath, sqlfilepath]
    count = 0
    filecount = len(filelist)
    # a = ['abc', 'def']
    # file1 = open('/tmp/testttt.txt', 'w')
    # file1.write(str(a))
    # file1.close()
    # file1 = open('/tmp/testttt.txt', 'r')
    # content = file1.readlines()
    # list1 = content[0]
    # list2 = eval(list1)
    # print list2, type(list2)
    for i in range(len(filelist)):
        result = os.path.exists(filelist[i])
        if result is False:
            commands.getstatusoutput('touch %s' % filelist[i])
            result = os.path.exists(filelist[i])
            if result is True:
                count += 1
        elif result is True:
            count += 1
    if count == filecount:
        loadlist(filelist)

def loadlist(filelist):
    readfilelist = []
    xsslist = []
    sqlilist = []
    # print filelist
    for i in range(len(filelist)):
        file1 = open(filelist[i])
        content = file1.readlines()
        if len(content) != 0:
            tmp = content[0]
            urllist = eval(tmp)
            if i == 0:
                readfilelist = urllist
            elif i == 1:
                xsslist = urllist
            elif i == 2:
                sqlilist = urllist
            else:
                pass
    return readfilelist, xsslist, sqlilist

    # print content


if __name__ == '__main__':
    checkfile()
    # print __name__
