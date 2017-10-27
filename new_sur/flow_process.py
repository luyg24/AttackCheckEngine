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


# reload(sys)
# sys.setdefaultencoding('utf8')

pool = redis.ConnectionPool(host='100.109.70.76', port=6379, password = 'idsredis', db = 1)
r = redis.Redis(connection_pool = pool)
#print r.llen('ids')
# length = r.llen('ids')
# file = open('loglog.txt', 'a')
startline = 9000
totalline = r.llen('ids')
while True:
    if totalline > startline:
        content = r.lrange('ids', startline, startline)[0]
        ncontent = json.loads(content)
        getdata = redis_test.OpRedis(startline, totalline, ncontent)
        if getdata.getprostatus() == 'http':
            # 调用celery获取页面内容
            getcontent.delay(ncontent)
        else:
            #非http流量暂不处理
            pass
        startline += 1
    else:
        time.sleep(10)
        totalline = r.llen('ids')
        print startline, totalline
