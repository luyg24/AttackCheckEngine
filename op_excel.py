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

def create_excel(filename):
    file = open(filename, 'r')
    content = file.readlines()
    for i in range(len(content)):
        tmp = content[i].split('$$')
        print tmp
    #print content
    # date_filename = str(datetime.date.today())
    # oldwb = xlrd.open_workbook('tmp_gx.xls', formatting_info=True);
    # newwb = copy(oldwb);
    # news = newwb.get_sheet(0);
    # news.write(3,3,"33test")
    # news.write(4,3,"43test")
    # newwb.save(date_filename);

create_excel('guanxing_result.txt')