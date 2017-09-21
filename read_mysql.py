# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
read from mysql
"""

import mysql.connector
import record_err
import base64


filename = 'ids_mysql.conf'
def countsql():
    try:
        config = getinfo(filename)
        conn = mysql.connector.connect(**config)
        cur = conn.cursor()
        count = 'select count(*) from ids_info'
        cur.execute(count)
        linenumber = cur.fetchall()
        print linenumber
    except Exception as e:
        record_err.logrecord()

def readfile(startline = 1):
    try:
        config = getinfo(filename)
        conn = mysql.connector.connect(**config)
        cur = conn.cursor()
        readsql = 'select * from ids_info'
        cur.execute(readsql)
        result = cur.fetchall()
        print result, type(result)
        id = result[0][0]
        print id, type(id)
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

def getuntestline():
    try:
        config = getinfo(filename)
        conn = mysql.connector.connect(**config)
        cur = conn.cursor()
        readsql = 'select id from ids_info where vul is NULL limit 0,1'
        cur.execute(readsql)
        result = cur.fetchall()
        print result
    except Exception as e:
        record_err.logrecord()


if __name__ == '__main__':
    # print __name__
    getuntestline()
