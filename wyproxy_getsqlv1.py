# !/usr/bin/env python
#  -*- coding: UTF-8 -*-

import MySQLdb
import json
import string
import random
import commands
import re

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
# connect
conn = MySQLdb.connect(host = host, user = user, passwd = passwd , db = db)
cursor = conn.cursor()

def check_lines():
    sql = 'select count(*) from capture '
    cursor.execute(sql)
    result = cursor.fetchall()
    result = int(result[0][0])
    return result
    # for i in range(result):
    #     sql = 'select extension from capture where id = %d' %i
    #     cursor.execute(sql)
    #     result = cursor.fetchall()
    #     if len(result) == 1:
    #         ext = result[0][0]
    #         if ext in ['php', 'PHP', 'CGI', 'cgi', 'jsp', 'JSP', 'asp', 'ASP', 'aspx', 'ASPX']:
    #             check_record(i)

def get_sqlline(endline, startline = 1):
    #控制次数
    for i in range(endline):
        data = ''
        post = ''
        checksql = 'select content_type  from capture where id = %d' % (startline)
        checkmethod = 'select method from capture where id = %d' % (startline)
        getsql = 'select method,url,host,request_header from capture where id = %d' % (startline)
        postsql = 'select method,url,host,request_header,request_content from capture where id = %d' % (startline)
        cursor.execute(checksql)
        content_type = cursor.fetchall()
        if content_type[0][0]:
            if content_type[0][0] in ['text/html', 'application/octet-stream']:
                cursor.execute(checkmethod)
                method = cursor.fetchall()
                method = method[0][0]
                if method == 'GET':
                    cursor.execute(getsql)
                    data = cursor.fetchall()
                    data = data[0]
                elif method == 'POST':
                    cursor.execute(postsql)
                    data = cursor.fetchall()
                    data = data[0]
                else:
                    print 'maybe error'
        else:
            print 'no match!'
        if len(data) > 0:
            method = data[0]
            url = data[1]
            host = data[2]
            header = data[3]
            if len(data) > 4:
                post = data[4]
            print method, url, host, header, post
            #create_request(method, url, host, header, post)
        else:
            print 'no match'
        cursor.close()
        startline += 1
    startline = startline - 1
    print endline, startline

sql_count = check_lines()
get_sqlline(sql_count, 1)