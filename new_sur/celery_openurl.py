# -*- coding: utf-8 -*-

import time
import requests
from celery import Celery

broker =  'redis://:idsredis@100.109.70.76:6379/2'
backend = 'redis://:idsredis@100.109.70.76:6379/3'

app = Celery('task1', broker=broker, backend=backend)

@app.task
def getcontent(ncontent):
    r1 = ''
    r2 = ''
    pagestatus = 0
    pagecontent = ''
    header = {'user-agent': 'Chrome/60.0.3112.113 Safarids24/537.36'}
    httpurl = 'http://' + ncontent['hostname'] + ncontent['url']
    httpsurl = 'https://' + ncontent['hostname'] + ncontent['url']
    if ncontent['method'].lower() == 'get':
        try:
            r1 = requests.get(httpurl, headers=header, timeout = 5)
            if isinstance(r1, object):
                #代表页面能正常打开
                if r1.status_code > 199 and r1.status_code < 300:
                    pagestatus = r1.status_code
                    pagecontent = r1.content
                else:
                    #status 是0代表这个页面无法打开
                    pagestatus = 0
                    pagecontent = ''
            else:
                r2 = requests.get(httpsurl, headers=header, timeout=5, verify = False)
                if isinstance(r2, object):
                    # 代表页面能正常打开
                    pagestatus = r2.status_code
                    pagecontent = r2.content
                else:
                    pagestatus = 0
                    pagecontent = ''

        except requests.exceptions.ConnectTimeout:
            pagestatus = 0
            pagecontent = ''
        except requests.exceptions.Timeout:
            pagestatus = 0
            pagecontent = ''
        except requests.exceptions.ConnectionError:
            pagestatus = 0
            pagecontent = ''
    elif ncontent['method'].lower() == 'post':
        pass
    else:
        #其他的方法暂时不管
        pass
    ncontent['pagestatus'] = pagestatus
    ncontent['pagecontent'] = pagecontent
    return ncontent