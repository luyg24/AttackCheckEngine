# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
read from mysql
"""

# import update_msyql_vul
# import check_fileread_attack
import mysql.connector
import record_err
import base64



def catfileread(id, hostname, url, method, status, postdata):
    # unicode change to str
    hostname = str(hostname)
    url = str(base64.b64decode(url))
    method = str(method)
    if method.lower() == 'post':
        if len(method)>0:
            postdata = str(base64.b64decode(postdata))
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
        config = getinfo(myconf)
        conn = mysql.connector.connect(**config)
        cur = conn.cursor()
        readsql = 'select  catagory, hostname, url, method, status, postdata, payload, dstport from httpattack where id = %d' % startid
        cur.execute(readsql)
        # get info
        result = cur.fetchall()
        if len(result) > 0:
            # "get data from db is unicode"
            catagory = str(result[0][0])
            hostname = str(base64.b64decode(result[0][1]))
            url = str(base64.b64decode(result[0][2]))
            method = str(result[0][3])
            status = str(result[0][4])
            postdata = str(result[0][5])
            payload = str(result[0][6])
            dstport = str(result[0][7])
            if len(payload) > 0:
                payload = str(base64.b64decode(payload))
            if method.lower() == 'post':
                if len(postdata) > 0:
                    postdata = str(base64.b64decode(postdata))
        else:
            print 'mysql info error'
        if catagory == u'read_file':
            #需要判断是否需要登录
            print hostname, url, dstport, method, postdata, status
            if method.lower() == 'get':
                pass
                # catfileread(id, hostname, url, method, status, postdata)
            elif method.lower() == 'post':
                pass
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
        config = getinfo(myconf)
        conn = mysql.connector.connect(**config)
        cur = conn.cursor()
        linecount = 'select count(id) from httpattack '
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
            config = getinfo(myconf)
            conn = mysql.connector.connect(**config)
            cur = conn.cursor()
            readsql = 'select id from httpattack where attack_status is NULL limit %d,1' % i
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
    myconf = 'ids_mysql.conf'
    # print __name__
    getuntestline()
    # print startid