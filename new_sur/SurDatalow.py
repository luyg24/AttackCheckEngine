# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
read from suricata log file use data flow
"""

import record_err
import commands
import linecache
import time
import datetime
import sys


reload(sys)
sys.setdefaultencoding('utf8')


class DataFlow(object):
    def __init__(self, data):
        try:
            #生成一个新的dict
            newdict = {}
            if isinstance(data, dict):
                if len(data) > 1:
                    if 'http' in data.keys():
                        newdict['http'] = data['http']
                    if 'timestamp' in data.keys():
                        newdict['timestamp'] = data['timestamp']
                    if 'alert' in data.keys():
                        newdict['alert'] = data['alert']
                    if len(newdict) > 0:
                        return newdict
                    else:
                        return None
            else:
                print 'not dict type!'
        except:
            return None


    def createdict(self):
        pass



class File(object):
    def __init__(self, filepath, startline=0):
        self.filepath = filepath
        self.startline = startline

    def count(self):
        #返回文件行数
        try:
            status, output = commands.getstatusoutput('wc -l %s' %self.filepath)
            output = output.split()
            return int(output[0])
        except Exception as e:
            record_err.logrecord()

    def read(self):
        #更新一下缓存,避免新增内容获取不到
        linecache.checkcache(self.filepath)
        #每次读取一行内容
        content=linecache.getline(self.filepath, self.startline)
        return content

syspath = '/tmp/test1.json'
fromline = 0
readfile = File(syspath, fromline)
filelines = readfile.count()
try:
    while True:
        if filelines > fromline:
            log = open('logs/log.txt', 'a')
            #证明文件有新增内容需要继续读取,fromline＋1代表上次执行到了fromline行，这次从＋1行开始
            for fromline in range(fromline + 1, filelines + 1, ):
                readfile = File(syspath, fromline)
                content = readfile.read()
                #使用eval将原本数据外面的引号去除，这里因为原来的数据是dict，所以新的content现在是dict
                try:
                    content = eval(content)
                    #进行下一步处理，流量整形,获取到最新的数据
                    newcontent = DataFlow(content)
                    log.write(str(fromline) + 'line is finished!\n')
                    print newcontent
                except:
                    continue
            log.close()
        else:
            print fromline
            time.sleep(10)
            readfile = File(syspath, fromline)
            filelines = readfile.count()
except Exception as e:
    record_err.logrecord()


