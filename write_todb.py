# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
write info to db, url and post convert to base64 before write
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
        attacktype = data[u'attack_type']
        hostname = data[u'hostname']
        status = data[u'status']
        method = data[u'method']
        url = data[u'url']
        if method.lower == 'post':
            post = data[u'post']
        print attacktype, hostname, status, method, url
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