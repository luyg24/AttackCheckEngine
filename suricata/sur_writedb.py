# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
write info to db, url and post convert to base64 before write, if vul Y not N, not sure M
"""

import mysql.connector
import record_err
import base64
import linecache
import commands
import time
import json





def writedb(data):
    try:
        data = eval(data)
        config = getinfo(myfile)
        conn = mysql.connector.connect(**config)
        cur = conn.cursor()
        # sql = 'desc ids_info'
        # url, useragent, postdata, need base64code
        status = data['status']
        catagory = data['catagory']
        alert = data['alert']
        postdata = base64.b64encode(data['postdata'])
        url = base64.b64encode(data['url'])
        hostname = data['hostname']
        # datetime = data['datetime']
        method = data['method']
        # srcip = data['src_ip']
        # srcport = data['src_port']
        # dstip = data['dest_ip']
        dstport = data['dest_port']
        length = data['length']
        useragent = base64.b64encode(data['useragent'])
        xff = data['xff']
        payload = data['payload']
        insertsql = 'insert into httpattack(catagory, alert, dstport, hostname, url, method, length, useragent, \
        postdata, payload, status),  values("%s","%s" ,"%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' \
        %(catagory, alert, dstport, hostname, url, method, length, useragent, postdata, payload, status)
        print insertsql
        # if method.lower() == 'post':
        #     post = data[u'post']
        #     basepost = base64.b64encode(post)
        # # write to db
        # if method.lower() == 'get':
        #     insertsql1 = 'insert into  ids_info(attack_type, hostname, status, method, url ) ' \
        #                  'values("%s", "%s", %d, "%s", "%s")' % (attacktype, hostname, status, method, baseurl)
        #     cur.execute(insertsql1)
        #     conn.commit()
        # elif method.lower() == 'post':
        #     insertsql2 = 'insert into  ids_info(attack_type, hostname, status, method, url, postdata ) ' \
        #                  'values("%s", "%s", %d, "%s", "%s", "%s")' % (attacktype, hostname, status, method, baseurl, basepost)
        #     # print insertsql2
        #     cur.execute(insertsql2)
        #     conn.commit()
        # else:
        #     print 'what?'
        # # result_set = cur.fetchall()
        # # print result_set
        # conn.close()
    except Exception as e:
        record_err.logrecord()


def getinfo(myfile):
    try:
        file = open(myfile, 'r')
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

def readfile(content):
    print content, type(content)


def filename(logfile, file_count, startline):
    try:
        # 控制读取次数
        for i in range(file_count-startline + 1):
            content = linecache.getline(logfile, startline)
            writedb(content)
            # readfile(content)
            startline += 1
        # 已处理到多少行
        linecache.clearcache()
        return startline - 1
    except Exception as e:
        record_err.logrecord()


def filecount(logfile):
    try:
        stats, output = commands.getstatusoutput('wc -l %s' % (logfile))
        count = int(output.split()[0])
        return count
    except Exception as e:
        record_err.logrecord()



def fileinfo(logfile, start_line=1):
    try:
        # 获取文件行数
        file_count = filecount(logfile)
        print file_count
        processed_line = filename(logfile, file_count, start_line)
        while 1:
            file_record = open('logs/file_dbno.txt', 'a')
            file_count = filecount(logfile)
            file_record.write(str(processed_line))
            file_record.write('\n')
            file_record.close()
            if file_count > processed_line:
                processed_line = filename(logfile, file_count, processed_line + 1)
                # record the last processed line number
            time.sleep(3)
    except Exception as e:
        record_err.logrecord()


if __name__ == '__main__':
    # print __name__
    myfile = 'ids_mysql.conf'
    logfile = 'logs/duplicate_attack.txt'
    fileinfo(logfile, 1)

    # writedb('ids_mysql.conf')