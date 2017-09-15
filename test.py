# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
test file,yes all kinds of tests
"""

import record_err
import datetime

def test():
    try:
        print 'hello'
    except Exception as e:
        logfile = record_err.logging()
        print logfile
        reclog = open(logfile, 'a')
        localtime = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
        reclog.write('%s  %s, %s\n' %(localtime, Exception, e))
        reclog.close()