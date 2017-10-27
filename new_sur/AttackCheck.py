import commands
import linecache
import time
import datetime
import sys
import requests

class Attack(object):
    def __init__(self, data):
        #结果：fail,success,unknown
        self.data = data
        # print self.data['attacktype']
        if self.data['attacktype'] == u'sql注入':
            self.check()
        else:
            result = self.status_check()
            if result == 0:
                self.result()
            else :
                print 'status is not 200'
                self.check()

    def check(self):
        #这里的都需要进行检测了
        print self.data['attacktype'], 'result: known'
        pass

    def result(self):
        return self.data

    def status_check(self):
        if 'status' in self.data.keys():
            if self.data['status'] > 199 and self.data['status'] < 300:
                return 1
            else :
                self.data['result'] = 'Fail'
                return 0

    def urlmake(self):
        if 'hostname' in self.data['keys']:


    def page_check(self):
        if 'method' in self.data['keys']:
            if self.data['method'].lower() == 'get':
                pass
            elif self.data['method'].lower() == 'post':
                pass
            else:
                #这里要返回结果是unknown，需要手工检查
                pass
    def otherattack(self):


    def sql_inject(self):
        pass

    def file_read(self):
        result = self.status_check()
        if result == 0:
            return self.data
        else:
            print 'checking.......'
            return 0

    def xss(self):
        result = self.status_check()
        if result == 0:
            return self.data
        else:
            print 'checking.......'
            return 0

    def scanner(self):
        result = self.status_check()
        if result == 0:
            return self.data
        else:
            print 'checking.......'
            return 0

    def cve(self):
        result = self.status_check()
        if result == 0:
            return self.data
        else:
            print 'checking.......'
            return 0