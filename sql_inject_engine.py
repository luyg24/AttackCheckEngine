# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
sql注入检测引擎
"""
import re
import commands



def runsqlmap(filepath):
    sqlcheck = 'python /home/program/github/sqlmap/sqlmap.py -r' + filepath + ' --level=3 --dbs \
     --answers="quit=N,follow=N"  --batch --flush-session --purge-output'
    sqlfile = open('sqlresult.txt', 'a')
    sqlresult = 'available databases'
    (status, output) = commands.getstatusoutput(sqlcheck)
    # print output
    if re.search(sqlresult, output):
        print filepath + 'found sql injection!'
        sqlfile.write('1' + filepath + ': found sql injection!\n')
    else:
        sqlfile.write('0' + filepath + ': maybe no vul!\n')
        sqlfile.close()
