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
    print result
    # for i in range(result):
    #     sql = 'select extension from capture where id = %d' %i
    #     cursor.execute(sql)
    #     result = cursor.fetchall()
    #     if len(result) == 1:
    #         ext = result[0][0]
    #         if ext in ['php', 'PHP', 'CGI', 'cgi', 'jsp', 'JSP', 'asp', 'ASP', 'aspx', 'ASPX']:
    #             check_record(i)