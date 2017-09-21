# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
update  mysql vul
"""

import mysql.connector
import record_err


filename = 'ids_mysql.conf'


def getinfo(filename):
    try:
        file = open(filename, 'r')
        config = {}
        content = file.readlines()
        for i in range(len(content)):
            tmp = content[i].split(':')
            key = tmp[0]
            value = tmp[1].split('\n')[0]
            config[key] = value
        return config
    except Exception as e:
        record_err.logrecord()

def updatevul(id, vul):
    #give mysql id and vul status, update mysql
    getinfo(filename)
    sql = 'update ids_info set vul = "%s" where id = %d' % (vul, id)
    print sql