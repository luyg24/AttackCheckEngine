#!/usr/bin/env python
# -*- coding:utf-8 -*-

import redis
import json
import requests
import redis_test
import time
import sys
import record_err
from celery_openurl import getcontent


reload(sys)
sys.setdefaultencoding('utf8')

pool = redis.ConnectionPool(host='100.109.70.76', port=6379, password = 'idsredis', db = 3)
r = redis.Redis(connection_pool = pool)
keylist = r.keys()
for i in range(len(keylist)):
    #首先判断status是否是success，如果是则执行完毕，否则任务还没有执行完毕
    dict_content = json.loads(r.get(keylist[i]))
    if dict_content['status'].lower() == 'success':
        #代表任务执行完毕,这里需要判断attack是否成功
        if 'pagestatus' in dict_content['result'].keys() and 'pagecontent' in dict_content['result'].keys():
            if dict_content['result']['pagestatus'] == 0:
                #代表页面打不开，攻击失败，直接赋予attackstatus = 'fail'
                dict_content['attackstatus'] = 'fail'
                #删除这个key
                r.delete(keylist[i])
            else:
                if len(dict_content['result']['pagecontent']) < 20:
                    dict_content['attackstatus'] = 'fail'
                    r.delete(keylist[i])
                elif '借贷宝官网' in dict_content['result']['pagecontent'] and '功能介绍' in dict_content['result']['pagecontent']:
                    dict_content['attackstatus'] = 'fail'
                    r.delete(keylist[i])
                elif 'Thank you for using nginx' in dict_content['result']['pagecontent']:
                    dict_content['attackstatus'] = 'fail'
                    r.delete(keylist[i])
                else:
                    print dict_content
        else:
            print dict_content
            pass
    else:
        #任务没有执行完毕
        pass
