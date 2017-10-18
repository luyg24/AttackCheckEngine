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


# reload(sys)
# sys.setdefaultencoding('utf8')


class Attack(object):
    def __init__(self):
        pass




class DataFlow(object):
    def __init__(self, data):
        self.data = data

    def createdict(self):
        self.newdict = {}
        if isinstance(self.data, dict):
            if len(self.data) > 1:
                if 'http' in self.data.keys():
                    self.newdict['type'] = 'http_attack'
                    if 'status' in self.data['http'].keys():
                        self.newdict['status'] = self.data['http']['status']
                    if 'length' in self.data['http'].keys():
                        self.newdict['length'] = self.data['http']['length']
                    if 'http_user_agent' in self.data['http'].keys():
                        self.newdict['user_agent'] = self.data['http']['http_user_agent']
                    if 'http_method' in self.data['http'].keys():
                        self.newdict['method'] = self.data['http']['http_method']
                    if 'request_body' in self.data['http'].keys():
                        self.newdict['request_body'] = self.data['http']['request_body']
                    if 'http_refer' in self.data['http'].keys():
                        self.newdict['http_refer'] = self.data['http']['http_refer']
                    if 'url' in self.data['http'].keys():
                        self.newdict['url'] = self.data['http']['url']
                    if 'hostname' in self.data['http'].keys():
                        self.newdict['hostname'] = self.data['http']['hostname']
                    if 'xff' in self.data['http'].keys():
                        self.newdict['xffip'] = self.data['http']['xff']
                    # self.newdict['http'] = self.data['http']
                else:
                    self.newdict['type'] = 'other_attack'
                if 'timestamp' in self.data.keys():
                    self.newdict['timestamp'] = self.data['timestamp']
                if 'payload' in self.data.keys():
                    self.newdict['payload'] = self.data['payload']
                if 'src_ip' in self.data.keys():
                    self.newdict['srcip'] = self.data['src_ip']
                if 'src_port' in self.data.keys():
                    self.newdict['srcport'] = self.data['src_port']
                if 'dest_ip' in self.data.keys():
                    self.newdict['destip'] = self.data['dest_ip']
                if 'dest_port' in self.data.keys():
                    self.newdict['destport'] = self.data['dest_port']
                if 'alert' in self.data.keys():
                    # self.newdict['alert'] = self.data['alert']
                    if 'signature' in self.data['alert'].keys():
                        self.newdict['signature'] = self.data['alert']['signature']
        else:
            print 'not dict type!'
        return self.newdict

    def catagory(self):
        attackcat = open('conf/attack_method.txt', 'r')
        matchrule = eval(attackcat.read())
        match = 0
        for k, v in matchrule.items():
            for i in range(len(v)):
                if v[i] in self.newdict['signature']:
                    self.newdict['attacktype'] = k
                    print self.newdict['attacktype'], self.newdict['signature']
                    match = 1
                    break
            if match == 1:
                break
            else:
                continue
        if match == 0:
            print self.newdict['signature']




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

# syspath = '/tmp/test1.json'
syspath = '/data/public/suricata/log/eve-httpids.json'
fromline = 5000000
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
                    dataflow = DataFlow(content)
                    newcontent = dataflow.createdict()
                    dataflow.catagory()
                    log.write(str(fromline) + 'line is finished!\n')
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


