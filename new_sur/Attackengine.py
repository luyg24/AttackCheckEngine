# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Attack Engine
"""

import record_err
import commands
import linecache
import time
import datetime
import sys


reload(sys)
sys.setdefaultencoding('utf8')


class Attack(object):
    try:
        def __init__(self, data):
            self.data = data
            self.data['result'] = ''
            # 结果有攻击成功(succesd)、攻击失败(failed)、未检测(uncheck)

        def whitecheck(self):
            file = open('conf/whitelist.txt','r')
            rule = eval(file.readline())
            if 'hostname' in self.data.keys():
                if self.data['hostname'] in rule['whitelist']:
                    self.data['result'] = 'uncheck'
                    return self.data
                else:
                    return 0
            else:
                return 0

            # print type(self.data), self.data
        def result(self):
            pass
            #返回检测结果
        def scancheck(self):
            pass
        def cvecheck(self):
            pass
        def iischeck(self):
            pass
        def xsscheck(self):
            pass
        def readfile(self):
            if self.data['status'] > 199 and self.data['status'] < 300:
                self.data['result'] = 'failed'
            else:
                print 'need check'
                self.data['result'] = 'uncheck'
            return self.data









    except Exception as e:
        record_err.logrecord()
