# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
read from mysql
"""

import update_msyql_vul
import check_fileread_attack
import mysql.connector
import record_err
import base64


filename = 'ids_mysql.conf'


def catfileread(id, hostname, url, method, status, postdata):
    # unicode change to str
    hostname = str(hostname)
    url = str(url)
    method = str(method)
    postdata = str(postdata)
    if status == 200:
        check_fileread_attack.check(id, hostname, url, method, status, postdata)
        # status is 200 check or no check!
    elif status != 200:
        print status
        vul = 'N'
        update_msyql_vul.updatevul(id, vul)

    else:
        print 'what?'


def readfile(startid = 1):
    try:
        id = startid
        config = getinfo(filename)
        conn = mysql.connector.connect(**config)
        cur = conn.cursor()
        readsql = 'select  attack_type, hostname, url, method, status, postdata from  ids_info where id = %d' % startid
        cur.execute(readsql)
        # get info
        result = cur.fetchall()
        if len(result) > 0:
            attack_type = result[0][0]
            hostname = result[0][1]
            url = result[0][2]
            method = result[0][3]
            status = result[0][4]
            postdata = result[0][5]
        else:
            print 'mysql info error'
        if attack_type == u'文件读取':
            catfileread(id, hostname, url, method, status, postdata)
        else:
            # process other attack_type
            pass


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

def getcount():
    try:
        # get msyql line number
        config = getinfo(filename)
        conn = mysql.connector.connect(**config)
        cur = conn.cursor()
        linecount = 'select count(id) from ids_info '
        cur.execute(linecount)
        result = cur.fetchall()
        return int(result[0][0])
        cur.close()
        conn.close()
    except Exception as e:
        record_err.logrecord()


def getuntestline():
    try:
        # get the untest id
        count = getcount()
        for i in range(count):
            config = getinfo(filename)
            conn = mysql.connector.connect(**config)
            cur = conn.cursor()
            readsql = 'select id from ids_info where vul is NULL limit %d,1' % i
            cur.execute(readsql)
            result = cur.fetchall()
            id = result[0][0]
            # return id
            cur.close()
            conn.close()
            readfile(id)
    except Exception as e:
        record_err.logrecord()


if __name__ == '__main__':
    # print __name__
    getuntestline()
    # print startid

