# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
process excel
"""

import xlwt
import xlrd


wbk = xlrd.open_workbook('test.xls')
worksheet = wbk.sheet_by_name('test')
num_rows = worksheet.nrows
print num_rows

file = open('guanxing_result.txt', 'r')
wbk = xlwt.Workbook()
sheet = wbk.add_sheet('test')
sheet.write(0, 1, 'test')
wbk.save('test.xlxs')