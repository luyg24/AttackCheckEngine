# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
test file,yes all kinds of tests
"""

import record_err
import datetime
import traceback

def test():
    try:
        print 'hello'
        print ae
    except Exception as e:
        record_err.logrecord()