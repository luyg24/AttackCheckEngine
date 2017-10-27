#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-


import redis
import json
import requests
import sys


reload(sys)
sys.setdefaultencoding('utf8')




def attackcheck(ncontent):
    if 'status' in ncontent.keys():
        if ncontent['attacktype'] == u'sql注入':
            print '%s need check' %(ncontent['attacktype'])
        else:
            if ncontent['status'] > 199 and ncontent['status'] < 300:
                if 'hostname' in ncontent.keys() and 'url' in ncontent.keys() and 'method' in ncontent.keys():
                    if ncontent['method'].lower() == 'get':
                        print 'http attack checking'
                    elif ncontent['method'].lower() == 'post':
                        print 'http attack checking'
                    else:
                        print '%s need check' %(ncontent['attacktype'])
                else:
                    print ncontent['attacktype']
            else:
                return 'Fail'
                # print '%s:%s attack fail' %(ncontent['attacktype'], ncontent['status'])
    else:
        print '%s no status need check!' %(ncontent['attacktype'])



def pagecheck(ncontent):
    r1 = ''
    r2 = ''
    header = {'user-agent': 'Chrome/60.0.3112.113 Safarids24/537.36'}
    httpurl = 'http://' + ncontent['hostname'] + ncontent['url']
    httpsurl = 'https://' + ncontent['hostname'] + ncontent['url']
    result = 0
    # 以下白名单如果匹配上了，则攻击失败
    whitelist = ['请求异常,请查证后再试', '系统错误，请稍后再试', '服务器异常', 'Welcome to nginx', '页面未找到']
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

def httpcheck(ncontent):
    result = 0
    #这里判断页面是否能打开，是否需要登录
    if 'hostname' in ncontent.keys() and 'url' in ncontent.keys() and 'method' in ncontent.keys():
        if ncontent['method'].lower() == 'get':
            result = pagecheck(ncontent)
        elif ncontent['method'].lower() == 'post':
            pass
            # pagecheck(ncontent)
            # print 'checking'
        else:
            pass
            # print 'need check'
    else:
        pass
        # print 'missing parameter'

    return result




pool = redis.ConnectionPool(host='100.109.70.76', port=6379, password = 'idsredis', db = 1)
r = redis.Redis(connection_pool = pool)
#print r.llen('ids')
length = r.llen('ids')
file = open('loglog.txt', 'a')
for i in range(length):
    attack_result = 'unknown'
    content =  r.lrange('ids',i,i)[0]
    ncontent = json.loads(content)
    # 判断是否sql注入，如果非sql注入，通过status即可判断是否成功，否则再转入检测
    if ncontent['attacktype'] == u'sql注入':
        #result 返回页面是否能打开，是否需要登录（0：不能打开，1：能打开；0:不需要登录，1:需要登录）
        pass
        #result = httpcheck(ncontent)
        #这里进行攻击检测

    elif ncontent['attacktype'] = u'文件读取':
        pass
    elif ncontent['attacktype'] = u'xss攻击'
        pass
    else:
        if 'status' in ncontent.keys():
            if ncontent['status'] > 199 and ncontent['status'] < 300:
                attack_result = httpcheck(ncontent)
            else:
                attack_result = 'fail'

        else:
            result = httpcheck(ncontent)
    if attack_result == 'fail' or result == 'fail':
        #这里检测结束
        file.write('fail\n')
        # print 'fail'
    else:
        file.write('need check \n')
        print ncontent
    #attackcheck(ncontent)

#a = AttackCheck.Attack(ncontent)
#result = a.basic_check()
#print result

#print ncontent, type(ncontent)
#print ncontent['status']
#print ncontent['url']