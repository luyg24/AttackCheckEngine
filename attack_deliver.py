# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
attack catagory
"""

import record_err
import linecache
import commands
import time


def catagory(attack_data):
    if attack_data[u'attack_type'] == u'文件读取' and attack_data[u'status'] == 200:
        print attack_data