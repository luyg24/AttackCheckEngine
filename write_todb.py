# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
write info to db
"""

import mysql.connector
import record_err
import linecache
import commands
import time

def getinfo(filename):
    file = open(filename, 'r')
    content = file.readlines()
    print content


if __name__ == '__main__':
    print __name__
    getinfo('ids_mysql.conf')