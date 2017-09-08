# !/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb
import json
import string
import random
import commands
import re

# connect
conn = MySQLdb.connect(host = '127.0.0.1', user = 'xxxxxx', passwd = 'xxxxxx' , db = 'xxxxxxx')
cursor = conn.cursor()

# check lines
def check_lines():
    sql = 'select count(*) from capture '
    cursor.execute(sql)
    result = cursor.fetchall()
    result = int(result[0][0])
    for i in range(result):
        sql = 'select extension from capture where id = %d' %i
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) == 1:
            ext = result[0][0]
            if ext in ['php', 'PHP', 'CGI', 'cgi', 'jsp', 'JSP', 'asp', 'ASP', 'aspx', 'ASPX']:
                check_record(i)
#check new line
def check_record(number):
    data = ''
    post = ''
    checksql = 'select content_type  from capture where id = %d' %(number)
    checkmethod = 'select method from capture where id = %d' %(number)
    getsql = 'select method,url,host,request_header from capture where id = %d' %(number)
    postsql = 'select method,url,host,request_header,request_content from capture where id = %d' %(number)
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
    if len(data) > 0 :
        method = data[0]
        url = data[1]
        host = data[2]
        header = data[3]
        if len(data) > 4:
            post = data[4]
        create_request(method, url, host, header, post)
    else:
        print 'no match'

    return data
    #print content_type
    #cursor.execute(sql)
    #print cursor.fetchall()
    cursor.close()

#create file
def create_request ( method, url, host, header, post ):
    # create file name
    filename = salt = ''.join(random.sample(string.ascii_letters + string.digits, 16))
    filepath = '/tmp/sqlmap/' + str(filename)
    dictheader = json.loads(header)
    f = open(filepath, 'a')
    line1 = method + ' ' + url + ' HTTP/1.1'
    line2 = 'Host: '+ host
    f.write(line1 +'\n')
    f.write(line2 +'\n')
    for k,v in dictheader.items():
        f.write(k + ': ' + v + '\n')
    if post > 0:
        line4 = post
        f.write('\n')
        f.write(line4 + '\n')
    f.close()
    runsqlmap(filepath)

def runsqlmap(filepath):
    sqlcheck = 'python /data/github/sqlmap/sqlmap.py -r' + filepath + ' --level=3 --dbs  --answers="quit=N,follow=N"  \
    --batch --flush-session --purge-output'
    sqlfile = open('sqlresult.txt', 'a')
    sqlresult = 'available databases'
    (status, output) = commands.getstatusoutput(sqlcheck)
    # print output
    if re.search(sqlresult, output):
        print filepath + 'found sql injection!'
        sqlfile.write(filepath + ': found sql injection')
        sqlfile.close()
    # print filename


check_lines()
# return_data = check_record(119)
