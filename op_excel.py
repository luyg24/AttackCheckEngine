# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
process excel
"""
import xlwt
import xlrd
import commands
import datetime
from xlutils.copy import copy
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
        if add_red == 'out':
            news.write(row, 3, port)
        elif add_red == 'red':
            news.write(row, 4, port)
        else:
            pass
        news.write(row, 7, in_out)
        row += 1
    newwb.save(date_filename)


create_excel('guanxing_result.txt')