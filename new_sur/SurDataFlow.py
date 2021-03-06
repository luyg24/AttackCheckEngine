# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
read from suricata log file use data flow
"""

import record_err
import json
import base64
import Attackengine
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
                        #注意字典赋值的时候，需要把字典转换成str，要不然遇到特殊字符会转义
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
                        #这里要进行判断，因为有的xff有多个
                        tmp = self.data['http']['xff']
                        #self.newdict['xffips'] = self.data['http']['xff']
                        if tmp.find(',') > 0 :
                            ip1 = tmp.split(',')[0]
                            self.newdict['xffip'] = ip1
                            self.newdict['xffips'] = self.data['http']['xff']
                        else:
                            self.newdict['xffip'] = self.data['http']['xff']
                    # self.newdict['http'] = self.data['http']
                else:
                    self.newdict['type'] = 'other_attack'
                if 'timestamp' in self.data.keys():
                    self.newdict['timestamp'] = self.data['timestamp']
                if 'payload' in self.data.keys():
                    #由于payload都是base64编码的，这里需要解码
                    if len(self.data['payload'])> 0:
                        tmp = self.data['payload']
                        self.newdict['payload'] = base64.b64decode(tmp).replace("'",'\'').replace('"','\"')
                    else :
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
                    # print self.newdict['attacktype'], self.newdict['signature']
                    match = 1
                    break
            if match == 1:
                return 1
            else:
                continue
        if match == 0:
            return 0
            # print self.newdict['signature']




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
fromline = 8996317
readfile = File(syspath, fromline)
filelines = readfile.count()
try:
    while True:
        if filelines > fromline:
            log = open('logs/log.txt', 'a')
            catfile = open('logs/catlog.txt', 'a')
            uncatfile = open('logs/uncatlog.txt', 'a')
            #证明文件有新增内容需要继续读取,fromline＋1代表上次执行到了fromline行，这次从＋1行开始
            for fromline in range(fromline + 1, filelines + 1, ):
                readfile = File(syspath, fromline)
                content = readfile.read()
                #使用eval将原本数据外面的引号去除，这里因为原来的数据是dict，所以新的content现在是dict
                try:
                    #content = eval(content)
                    content = json.loads(content)
                    #进行下一步处理，流量整形,获取到最新的数据
                    dataflow = DataFlow(content)
                    newcontent = dataflow.createdict()
                    # print newcontent['xffip']
                    # 判断分类之后的数据，如果分类完毕返回1，否则返回0！
                    check_cat = dataflow.catagory()
                    if check_cat == 0:
                        #这里给攻击一个其他攻击类型
                        newcontent['attacktype'] = 'other attack'
                        #这里要把dict数据反序列化
                        newcontent = json.dumps(newcontent)
                        uncatfile.write(newcontent + '\n')
                        log.write('uncatagory attack: '+ newcontent['signature'] + '\n')
                    #开始进行攻击检测,未进行攻击分类的不检测
                    else:
                        newcontent = json.dumps(newcontent)
                        catfile.write(newcontent + '\n')
                        #写入分析后的数据到redis和文本
                except:
                    log.write(str(fromline) + 'line is finished!\n')
                    continue
            log.close()
            catfile.close()
            uncatfile.close()
        else:
            log = open('logs/log.txt', 'a')
            log.write(str(fromline) + '\n')
            # print fromline
            time.sleep(10)
            readfile = File(syspath, fromline)
            filelines = readfile.count()
except Exception as e:
    record_err.logrecord()