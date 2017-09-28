# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
read from file by line, flow data!
usage: give a filename, and start line
fileinfo(filename, startline)
"""

import record_err
import linecache
import commands
import time
import json
import datetime


def catagory(idsdata):
    try:
        idsdata['catagory'] = ''
        alert = idsdata['alert']
        # CVE
        if 'CVE' in alert:
            idsdata['catagory'] = 'cve_attack'
        # read file
        elif 'read File' in alert:
            idsdata['catagory'] = 'read_file'
        elif 'aexp2.htr access' in alert:
            idsdata['catagory'] = 'read_file'
        elif 'EXPLOIT .htr access' in alert:
            idsdata['catagory'] = 'read_file'
        elif '.htaccess access' in alert:
            idsdata['catagory'] = 'read_file'
        elif '.ida access' in alert:
            idsdata['catagory'] = 'read_file'
        elif '.idq access' in alert:
            idsdata['catagory'] = 'read_file'
        elif '.asa access' in alert:
            idsdata['catagory'] = 'read_file'
        elif 'viewcode access' in alert:
            idsdata['catagory'] = 'read_file'
        elif 'printenv access' in alert:
            idsdata['catagory'] = 'read_file'
        elif 'fpcount access' in alert:
            idsdata['catagory'] = 'read_file'
        elif 'mod_gzip_status access' in alert:
            idsdata['catagory'] = 'read_file'
        # xxe
        elif 'XXE' in alert:
            idsdata['catagory'] = 'xxe_attack'
        # iis
        elif 'EXPLOIT iisadmpwd' in alert:
            idsdata['catagory'] = 'iis_attack'
        elif 'iissamples access' in alert:
            idsdata['catagory'] = 'iis_attack'
        # xss
        elif 'Cross Site Scripting' in alert:
            idsdata['catagory'] = 'xss_attack'
        # url scan
        elif 'administrator access' in alert:
            idsdata['catagory'] = 'url_scan'
        # sql inject
        elif 'SQL Errors in HTTP 200' in alert:
            idsdata['catagory'] = 'sql_inject'

        # command execute
        elif 'Access to /phppath/php':
            idsdata['catagory'] = 'cmd_execute'
        elif 'System Command' in alert:
            idsdata['catagory'] = 'cmd_execute'
        elif 'PHP config option' in alert:
            idsdata['catagory'] = 'cmd_execute'
        elif 'PHP tags in HTTP' in alert:
            idsdata['catagory'] = 'cmd_execute'
        # scanner
        elif 'SCAN Nessus' in alert:
            idsdata['catagory'] = 'scanner'

        else:
            print alert
        print idsdata['catagory']


    except Exception as e:
        record_err.logrecord()


def readfile(content):
    # change str to dict
    try:
        otherattackfile = open('logs/other_attack.txt', 'a')
        new_dict = {}
        new_dict['status'] = ''
        new_dict['postdata'] = ''
        new_dict['payload'] = ''
        new_dict['method'] = ''
        # if content is json str, convert to dict
        con_dict = json.loads(content)
        # check if content is http or not
        conkey = con_dict.keys()
        if u'http' in conkey:
            new_dict['http'] = con_dict[u'http']
            if u'status' in new_dict['http'].keys():
                new_dict['status'] = new_dict[u'http'][u'status']
            if u'http_user_agent' in new_dict['http'].keys():
                new_dict['useragent'] = new_dict[u'http'][u'http_user_agent']
            if u'url' in new_dict['http'].keys():
                new_dict['url'] = new_dict[u'http'][u'url']
            if u'hostname' in new_dict['http'].keys():
                new_dict['hostname'] = new_dict[u'http'][u'hostname']
            if u'xff' in new_dict['http'].keys():
                new_dict['xff'] = new_dict[u'http'][u'xff']
            if u'http_method' in new_dict['http'].keys():
                new_dict['method'] = new_dict[u'http'][u'http_method']
            if u'request_body' in new_dict['http'].keys():
                new_dict['postdata'] = new_dict[u'http'][u'request_body']
            if u'src_ip' in conkey:
                new_dict['src_ip'] = con_dict[u'src_ip']
            if u'src_port' in conkey:
                new_dict['src_port'] = con_dict[u'src_port']
            if u'dest_ip' in conkey:
                new_dict['dest_ip'] = con_dict[u'dest_ip']
            if u'dest_port' in conkey:
                new_dict['dest_port'] = con_dict[u'dest_port']
            if u'timestamp' in conkey:
                new_dict['datetime'] = con_dict[u'timestamp']
            if u'alert' in conkey:
                new_dict['alert'] = con_dict[u'alert'][u'signature']
            if u'payload' in conkey:
                new_dict['payload'] = con_dict[u'payload']
            new_dict.pop('http')
            catagory(new_dict)
        else:
            otherattackfile.write(str(new_dict))
            otherattackfile.write('\n')
            otherattackfile.close()
        # get http attack type and info
        # if con_dict[u'subproto']:
        #     if con_dict[u'subproto'] == 'http':
        #         new_dict[u'attack_type'] = con_dict[u'attack_type']
        #         new_dict[u'hostname'] = con_dict[u'hostname']
        #         new_dict[u'url'] = con_dict[u'url']
        #         new_dict[u'method'] = con_dict[u'method']
        #         new_dict[u'status'] = con_dict[u'status']
        #         if con_dict[u'method'] == 'POST':
        #             new_dict[u'post'] = con_dict[u'postdata']
        # attack_deliver.catagory(new_dict)
        # else , pass
    except Exception as e:
        record_err.logrecord()


def filename(logfile, file_count, startline):
    try:
        # 控制读取次数
        for i in range(file_count-startline+1):
            content = linecache.getline(logfile, startline)
            readfile(content)
            startline += 1
        # 已处理到多少行
        linecache.clearcache()
        return startline - 1
    except Exception as e:
        record_err.logrecord()


def filecount(logfile):
    try:
        stats, output = commands.getstatusoutput('wc -l %s' % (logfile))
        count = int(output.split()[0])
        return count
    except Exception as e:
        record_err.logrecord()


def fileinfo(logfile, start_line=1):
    try:
    # 获取文件行数
        file_count = filecount(logfile)
        processed_line = filename(logfile, file_count, start_line)
        while 1:
            file_record = open('file_no.txt', 'w')
            file_count = filecount(logfile)
            if file_count > processed_line:
                processed_line = filename(logfile, file_count, processed_line+1)
                # record the last processed line number
                file_record.write(str(processed_line))
                file_record.close()
            time.sleep(3)
    except Exception as e:
        record_err.logrecord()

if __name__ == '__main__':
    fileinfo('abc.txt', 2)