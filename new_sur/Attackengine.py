# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Attack Engine
"""

import record_err
import requests
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

        def statuscheck(self):
            #状态检查，如果返回1则代表返回非200，否则返回0，没有status或者返回200
            #1 代表非200等，页面无法正常返回，一般代表页面无法打开，0代表需要进一步测试
            if 'status' in self.data.keys():
                print self.data['status']
                #判断status是否为空值
                if len(self.data['status']) > 0 :
                    if self.data['status'] < 200 or self.data['status'] > 299:
                        print '!Failed'
                        return 1
                    else :
                        return 0
                else:
                    return 0
            else:
                return 0
        def scancheck(self):
            pass
        def cvecheck(self):
            pass
        def iischeck(self):
            pass
        def xsscheck(self):
            pass
        def readfile(self):
            status = self.statuscheck()
            if status == 1 :
                print self.data['status'], 'attack failed'
                self.data['result'] = 'failed'
                return self.data
            else:
                url = self.data['url']
                header = {'user-agent':'Chrome/60.0.3112.113 Safarids24/537.36'}
                hostname = self.data['hostname']
                httpurl = 'http://' + hostname + url
                httpsurl = 'https://' + hostname + url
                #需要进行实际测试，先判断方法
                if self.data['method'].lower() == 'get':
                    r1 = requests.get(httpurl, headers=header)
                    r2 = requests.get(httpsurl, headers = header, verify = False)
                    print r1.content, r2.text
                    pass
                elif self.data['method'].lower() == 'post':
                    pass
                else:
                    pass
                    print self.data['method']
                    self.data['result'] = 'uncheck'
            #return self.data


    except Exception as e:
        record_err.logrecord()
