# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
test file
"""
import record_err
import os
import commands
import sys
reload(sys)
sys.setdefaultencoding('utf8')


filelist = 'logs/attackedlist.txt'


def checkfile():
    try:
        count = 0
        filecount = len(filelist)
        for i in range(len(filelist)):
            result = os.path.exists(filelist)
            if result is False:
                commands.getstatusoutput('touch %s' % filelist)
                result = os.path.exists(filelist)
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
        attackedlist = []
        # print filelist
        file1 = open(filelist)
        content = file1.readlines()
        if len(content) != 0:
            tmp = content[0]
            attackedlist = eval(tmp)
        return attackedlist
    except Exception as e:
        record_err.logrecord()

def writelist(attackedlist):
    """
    write the new list to file!
    """
    try:
        file1 = open(filelist, 'w')
        file1.write(str(attackedlist))
    except Exception as e:
        record_err.logrecord()
    # print content


if __name__ == '__main__':
    checkfile()
    # print __name__
