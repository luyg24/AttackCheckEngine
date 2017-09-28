# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
test file
"""
import record_err
import os
import commands


readfilepath = 'logs/readfile.txt'
xssfilepath = 'logs/xss.txt'
sqlfilepath = 'logs/sqli.txt'
filelist = [readfilepath, xssfilepath, sqlfilepath]


def checkfile():
    try:
        count = 0
        filecount = len(filelist)
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
            return loadlist(filelist)
    except Exception as e:
        record_err.logrecord()

def loadlist(filelist):
    try:
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
    except Exception as e:
        record_err.logrecord()

def writelist(readfilelist, xsslist, sqlilist):
    """
    write the new list to file!
    """
    try:
        for i in range(len(filelist)):
            file1 = open(filelist[i], 'w')
            if i == 0:
                file1.write(str(readfilelist))
            elif i == 1:
                file1.write(str(xsslist))
            elif i == 2:
                file1.write(str(sqlilist))
            else:
                pass
    except Exception as e:
        record_err.logrecord()
    # print content


if __name__ == '__main__':
    checkfile()
    # print __name__
