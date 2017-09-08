# !/usr/bin/env python
#  -*- coding: UTF-8 -*-

import MySQLdb
import json
import string
import random
import commands
import re
import time

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
        # checksql = 'select content_type  from capture where id = %d' % (startline)
        checkmethod = 'select method from capture where id = %d' % (startline)
        getsql = 'select method,url,host,request_header from capture where (id = %d and content_type = "text/html")' \
                % (startline)
        postsql = 'select method,url,host,request_header,request_content from capture \
                where (id = %d and content_type = "text/html")' % (startline)
        checkext = 'select extension from capture where id = %d' %(startline)
        # cursor.execute(checkext)
        # result = cursor.fetchall()
        startline += 1
        #过滤掉一些静态页面
        cursor.execute(checkmethod)
        method = cursor.fetchall()
        # print method
        method = method[0][0]
        if method == 'GET':
            cursor.execute(getsql)
            data = cursor.fetchall()
            if len(data) > 0:
                data = data[0]
        elif method == 'POST':
            cursor.execute(postsql)
            data = cursor.fetchall()
            if len(data) > 0:
                data = data[0]
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
            continue
    cursor.close()
    startline = startline - 1
    return startline

sql_count = check_lines()
startline = get_sqlline(sql_count, 1)
while 1:
    sql_count = check_lines()
    startline = get_sqlline(sql_count, startline)
    time.sleep(3)