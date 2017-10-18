# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
read from suricata log file use data flow
"""

import record_err
import commands
import time
import datetime
import sys


reload(sys)
sys.setdefaultencoding('utf8')


class DataFlow(object):
    def __init__(self, data):

        print data.keys()


class File(object):
    def __init__(self, filepath, startline=1):
        self.filepath = filepath
        self.startline = startline
        print filepath, startline

    def count(self):
        status, output = commands.getstatusoutput('wc -l %s' %self.filepath)
        output = output.split()
        return int(output[0])

    def read(self):
        print 'reading file per line'


syspath = '/tmp/test1.json'
fromline = 1
readfile = File(syspath, fromline)
print readfile.count()
readfile.read()


