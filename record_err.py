# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
记录异常信息到logs目录
"""
import commands
import datetime
import re

def logging():
    result = ''
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    #check if exists logs folder
    status, output = commands.getstatusoutput('ls logs')
    result = re.search('No such file', output)
    if result is not None:
        status, output = commands.getstatusoutput('mkdir logs')
    # check if exists log file
    status, output = commands.getstatusoutput('ls ../logs%s' %date)
    result = re.search('No such file', output)
    if result is not None:
        status, output = commands.getstatusoutput('touch logs/%s' %date)
    status, output = commands.getstatusoutput('pwd')

    logfile = output + 'logs/' + date
    return(logfile)
    # create log file , named by date

    status, output = commands.getstatusoutput('')
print logging()