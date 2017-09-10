# !/usr/bin/env python
#  -*- coding: UTF-8 -*-


"""
this is a test python file
"""

import threading
import time

def test(thread_text):
    print time.ctime(), thread_text, '\n'

def testxc(n=3):
    threads = []
    for i in range(n):
        tmp = threading.Thread(target=test, args=(i, ))
        threads.append(tmp)
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()

testxc(4)
