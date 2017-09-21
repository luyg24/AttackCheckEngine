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


filename = 'ids_mysql.conf'


def writedb(data):
    try:
        config = getinfo(filename)
        conn = mysql.connector.connect(**config)
        cur = conn.cursor()
        sql = 'desc ids_info'
        print data
        cur.execute(sql)
        result_set = cur.fetchall()
        # print result_set
    except Exception as e:
        record_err.logrecord()


def getinfo(filename):
    try:
        file = open(filename, 'r')
        config = {}
        content = file.readlines()
        for i in range(len(content)):
            tmp = content[i].split(':')
            key = tmp[0]
            value = tmp[1].split('\n')[0]
            config[key] = value
        return config
    except Exception as e:
        record_err.logrecord()


if __name__ == '__main__':
    # print __name__
    writedb('ids_mysql.conf')