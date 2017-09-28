# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Check file read attack!
"""

import sur_readfileperline
import record_err
import commands
import time
import datetime


def getlog():
    pass

if __name__ == '__main__':
    idslog_path = '/data/public/suricata/log/eve-httpids.json'
    sur_readfileperline.fileinfo(idslog_path, 4995110)
    # print 'hello'