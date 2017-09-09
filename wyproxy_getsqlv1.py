# !/usr/bin/env python
#  -*- coding: UTF-8 -*-

import MySQLdb
import json
import string
import random
import commands
import re
import time
import create_requestheader


# connect
# conn = MySQLdb.connect(host = host, user = user, passwd = passwd , db = db)
# cursor = conn.cursor()

def check_lines(host, user, passwd, db):
    conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
    cursor = conn.cursor()
    sql = 'select count(*) from capture '
    cursor.execute(sql)
    result = cursor.fetchall()
    result = int(result[0][0])
    cursor.close()
    conn.close()
    return result
    # for i in range(result):
    #     sql = 'select extension from capture where id = %d' %i
    #     cursor.execute(sql)
    #     result = cursor.fetchall()
    #     if len(result) == 1:
    #         ext = result[0][0]
    #         if ext in ['php', 'PHP', 'CGI', 'cgi', 'jsp', 'JSP', 'asp', 'ASP', 'aspx', 'ASPX']:
    #             check_record(i)

def get_sqlline(host, user, passwd, db, endline, startline = 1):
    conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
    cursor = conn.cursor()
    #控制次数
    for i in range(endline - startline + 1):
        data = ''
        post = ''
        request_header = {}
        # checksql = 'select content_type  from capture where id = %d' % (startline)
        checkmethod = 'select method from capture where id = %d' % (startline)
        reqsql = 'select method,url,host,request_header from capture where (id = %d and content_type = "text/html")' \
                % (startline)
        postsql = 'select request_content from capture where (id = %d and content_type = "text/html")' % (startline)
        checkext = 'select extension from capture where id = %d' %(startline)
        startline += 1
        #过滤掉一些静态页面
        cursor.execute(checkmethod)
        method = cursor.fetchall()
        # print method
        if len(method) > 0:
            method = method[0][0]
            cursor.execute(reqsql)
            data = cursor.fetchall()
            if len(data) > 0:
                data = data[0]
        if len(data) > 0:
            method = data[0]
            url = data[1]
            host = data[2]
            header = data[3]
            # if len(data) > 4:
            #     post = data[4]
            # print method, url, host, header, post
            # 字符串转换成dict,组装成新的dict
            request_header = json.loads(header)
            request_header['method'] = method
            request_header['url'] = url
            request_header['protocol'] = 'HTTP/1.1'
            #create_request(method, url, host, header, post)
        if method == 'POST':
            cursor.execute(postsql)
            data = cursor.fetchall()
            if len(data) > 0:
                post = data[0][0]
                request_header['postdata'] = post
        if len(request_header)> 0:
            # print request_header
            create_requestheader(request_header)
    cursor.close()
    conn.close()
    startline = startline - 1
    return startline

#获取mysql参数
file = open('mysql.conf','r')
content = file.read()
content = content.split('\n')

# print content, len(content)
for i in range(len(content)):
    if i > 3:
        break
    else:
        tmp = content[i].split(':')
        if tmp[0] == 'host':
            host = tmp[1]
        elif tmp[0] == 'user':
            user = tmp[1]
        elif tmp[0] == 'pass':
            passwd = tmp[1]
        elif tmp[0] == 'db':
            db = tmp[1]
        else:
            'error'
sql_count = check_lines(host, user, passwd, db)
startcount = get_sqlline(host, user, passwd, db, sql_count, 77)
while 1:
    sql_count = check_lines(host, user, passwd, db)
    print sql_count, startcount
    if sql_count > startcount:
        startcount = get_sqlline(host, user, passwd, db, sql_count, startcount + 1)
    time.sleep(3)