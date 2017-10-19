# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Attack Engine
"""

import record_err
import commands
import linecache
import time
import datetime
import sys


reload(sys)
sys.setdefaultencoding('utf8')


class Attack(object):
    try:
        def __init__(self, data):
            self.data = data
            print type(self.data), self.data



    except Exception as e:
        record_err.logrecord()
