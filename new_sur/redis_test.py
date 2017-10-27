#!/usr/bin/env python
# -*- coding:utf-8 -*-

#import redis
import json
#import requests
import sys
import record_err

# reload(sys)
# sys.setdefaultencoding('utf8')


class OpRedis(object):
    #给一个缺省值
    #prostatus 代表几种状态: http, unhttp
    def __init__(self, currentline, totalline, ncontent):
        self.currentline = currentline
        self.totalline = totalline
        self.content = ncontent
        self.prostatus = self.getprostatus()

    def __str__(self):
        msg = "协议状态:%s,当前行:%d,总共:%d,数据:%s" %(self.prostatus, self.currentline, self.totalline, \
                                           json.dumps(self.content))
        return msg

    def getprostatus(self):
        if 'hostname' in self.content.keys() and 'url' in self.content.keys() and 'method' in self.content.keys() :
            #说明是一个http攻击类型
            return 'http'
        else:
            return 'unhttp'
        #这个方法用户获取这个数据是否被检测，checked, uncheck, 给出一个变量，判断这个变量的值即可


    def openpage(self):
        pass
        #这里获取页面返回的内容

class OpCelery(object):
    def __init__(self):
        pass
    def __str__(self):
        pass



