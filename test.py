# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
test file,yes all kinds of tests
"""

import record_err
import datetime
import traceback

def test2():
    print 'I am test2'

def test():
    try:
        print 'hello'
        print '似懂非懂分sdfdfdf' \
            'sabc', \
            'sdf'
        content = ('hello sdfsdf'
                   '2sdf')
        print content

    except Exception as e:
        record_err.logrecord()
        test2()

def test3():
    try:
        try:
            b = a
        except:
            b = ''
        print b
    except Exception as e:
        print 'error', e
test3()