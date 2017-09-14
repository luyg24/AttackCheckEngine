# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
可以提前做好一个excel模版, 基于这个模版填充要写的excel数据
"""
import xlwt
import xlrd
import commands
import datetime
from xlutils.copy import copy
import sendmail_v2
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def create_excel(filename):
    date_filename = str(datetime.date.today())
    oldwb = xlrd.open_workbook('tmp_gx.xls', formatting_info=True);
    newwb = copy(oldwb);
    news = newwb.get_sheet(0);
    file = open(filename, 'r')
    content = file.readlines()
    ncontent = []
    #print content
    row = 2
    for i in range(len(content)):
        tmp = content[i].split('$$')
        ip = tmp[0]
        port = tmp[1]
        add_red = tmp[2].lower()
        in_out = tmp[3]
        #中文需要转换成unicode，否则无法写入，会报错
        addr = unicode(tmp[5])
        bus = unicode(tmp[6])
        # 写入数据
        news.write(row, 0, ip)
        news.write(row, 1, bus)
        news.write(row, 2, addr)
        if add_red == 'add':
            news.write(row, 3, port)
        elif add_red == 'red':
            news.write(row, 4, port)
        else:
            pass
        news.write(row, 7, in_out)
        row += 1
        if in_out.lower() != 'out':
            ncontent.append(content)
    newwb.save(date_filename)
    content = '\n'.join(ncontent)
    return(content, date_filename)

status, output = commands.getstatusoutput('wc -l guanxing_result.txt')
line = output.split()
line =  int(line[0])
if line > 0:
    content, filename = create_excel('guanxing_result.txt')
    sendmail_v2.get_conf(content, filename)

else:
    print 'nothing!'
