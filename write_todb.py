# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
write info to db, url and post convert to base64 before write
"""

import mysql.connector
import record_err
import base64
import linecache
import commands
import time


filename = 'ids_mysql.conf'


def writedb(data):
    try:
        config = getinfo(filename)
        conn = mysql.connector.connect(**config)
        cur = conn.cursor()
        # sql = 'desc ids_info'
        attacktype = data[u'attack_type']
        hostname = data[u'hostname']
        status = int(data[u'status'])
        method = data[u'method']
        url = data[u'url']
        baseurl = base64.b64encode(url)
        if method.lower() == 'post':
            post = data[u'post']
            basepost = base64.b64encode(post)
        # write to db
        if method.lower() == 'get':
            insertsql1 = 'insert into  ids_info(attack_type, hostname, status, method, url ) ' \
                         'values("%s", "%s", %d, "%s", "%s")' % (attacktype, hostname, status, method, baseurl)
            cur.execute(insertsql1)
            conn.commit()
        elif method.lower() == 'post':
            insertsql2 = 'insert into  ids_info(attack_type, hostname, status, method, url, postdata ) ' \
                         'values("%s", "%s", %d, "%s", "%s", "%s")' % (attacktype, hostname, status, method, baseurl, basepost)
            # print insertsql2
            cur.execute(insertsql2)
            conn.commit()
        else:
            print 'what?'
        # result_set = cur.fetchall()
        # print result_set
        conn.close()
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