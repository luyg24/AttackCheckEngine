#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-


import redis
import json
import requests
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class Attack(object):
    def __init__(self, data):
        self.data = data
    def status(self):
        #return 0,1 0:fail 1:unknown
        r1 = ''
        r2 = ''
        header = {'user-agent': 'Chrome/60.0.3112.113 Safarids24/537.36'}
        httpurl = 'http://' + ncontent['hostname'] + ncontent['url']
        httpsurl = 'https://' + ncontent['hostname'] + ncontent['url']
        result = 1
        whitelist = ['请求异常,请查证后再试', '系统错误，请稍后再试', '服务器异常', '页面未找到']

        if ncontent['method'].lower() == 'get':
            try:
                r1 = requests.get(httpurl, headers=header, timeout=5)
                if isinstance(r1, object):
                    # 代表页面能正常打开
                    if r1.status_code > 199 and r1.status_code < 300:
                        for i in range(len(whitelist)):
                            if whitelist[i] in r1.content:
                                result = 0
                                break
                        if result == 0:
                            return result

                    else:
                        return result
                        # attack fail

                else:
                    r2 = requests.get(httpsurl, headers=header, timeout=5, verify=False)
                    if isinstance(r1, object):
                        # 代表页面能正常打开
                        if r2.status_code > 199 and r2.status_code < 300:
                            for i in range(len(whitelist)):
                                if whitelist[i] in r2.content:
                                    result = 0
                                    break
                            if result == 0:
                                return result
                        else:
                            return result
                            # attack fail

            except requests.exceptions.ConnectTimeout:
                NETWORK_STATUS = 'network error'
                return 0
            except requests.exceptions.Timeout:
                REQUEST_TIMEOUT = 'retimeout'
                return 0
            except requests.exceptions.ConnectionError:
                pagestatus = 'reset'
                return 0
        else:
            return result
            pass
            # print ncontent
            # print 'need check'

    def pagecontent(self):
        pass
    def pagesize(self):
        pass
    def sensitive(self):
        pass

def pagecheck(ncontent):
    r1 = ''
    r2 = ''
    header = {'user-agent': 'Chrome/60.0.3112.113 Safarids24/537.36'}
    httpurl = 'http://' + ncontent['hostname'] + ncontent['url']
    httpsurl = 'https://' + ncontent['hostname'] + ncontent['url']
    result = 'unknown'
    # 以下白名单如果匹配上了，则攻击失败
    whitelist = ['请求异常,请查证后再试', '系统错误，请稍后再试', '服务器异常', '页面未找到']

    if ncontent['method'].lower() == 'get':
        try:
            r1 = requests.get(httpurl, headers=header, timeout = 5)
            if isinstance(r1, object):
                #代表页面能正常打开
                if r1.status_code > 199 and r1.status_code < 300:
                    for i in range(len(whitelist)):
                        if whitelist[i] in r1.content:
                            result = 'fail'
                            break
                    if result == 'fail':
                        return 'fail'

                else:
                    return 'fail'
                    #attack fail

            else:
                r2 = requests.get(httpsurl, headers=header, timeout=5, verify = False)
                if isinstance(r1, object):
                    # 代表页面能正常打开
                    if r2.status_code > 199 and r2.status_code < 300:
                        for i in range(len(whitelist)):
                            if whitelist[i] in r2.content:
                                result = 'fail'
                                break
                        if result == 'fail':
                            return 'fail'
                    else:
                        return 'fail'
                        # attack fail

        except requests.exceptions.ConnectTimeout:
            NETWORK_STATUS = 'network error'
            return 'fail'
        except requests.exceptions.Timeout:
            REQUEST_TIMEOUT = 'retimeout'
            return 'fail'
        except requests.exceptions.ConnectionError:
            pagestatus = 'reset'
            return 'fail'
    else:
        return result
        pass
        # print ncontent
        # print 'need check'



pool = redis.ConnectionPool(host='100.109.70.76', port=6379, password = 'idsredis', db = 1)
r = redis.Redis(connection_pool = pool)
#print r.llen('ids')
length = r.llen('ids')
file = open('loglog.txt', 'a')
for i in range(length):
    attack_result = 'unknown'
    content =  r.lrange('ids',i,i)[0]
    ncontent = json.loads(content)
    a = Attack(ncontent)
    # 判断是否sql注入，如果非sql注入，通过status即可判断是否成功，否则再转入检测
    if ncontent['attacktype'] == u'sql注入':
        pass
    elif ncontent['attacktype'] == u'文件读取':
        if 'status' in ncontent.keys():
            if ncontent['status'] < 200 or ncontent['status'] > 299:
                attack_result = 'fail'
            else:
                result = a.status()
                if result == 0:
                    attack_result = 'fail'
                else:
                    #需要进行下一步判断
                    pass
        else:
            pass
            #直接检测
    elif ncontent['attacktype'] == u'xss攻击':
        if 'status' in ncontent.keys():
            if ncontent['status'] < 200 or ncontent['status'] > 299:
                attack_result = 'fail'
                break
            else:
                pass
                #检测
        else:
            pass
            #直接检测
    else:
        attack_result = 'fail'
        #这些直接默认fail
    print ncontent['attacktype'], attack_result


    #     if 'status' in ncontent.keys():
    #         if ncontent['status'] > 199 and ncontent['status'] < 300:
    #             attack_result = httpcheck(ncontent)
    #         else:
    #             attack_result = 'fail'
    #
    #     else:
    #         result = httpcheck(ncontent)
    # if attack_result == 'fail' or result == 'fail':
    #     #这里检测结束
    #     file.write('fail\n')
    #     # print 'fail'
    # else:
    #     file.write('need check \n')
    #     print ncontent