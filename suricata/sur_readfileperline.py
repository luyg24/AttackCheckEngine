# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
read from file by line, flow data!
usage: give a filename, and start line
fileinfo(filename, startline)
"""

import record_err
import sur_load_listfile
import linecache
import commands
import time
import json
import datetime
import sys
import sur_writedb
reload(sys)
sys.setdefaultencoding('utf8')


def deldupl(idsdata):
    try:
        duplicatedfile = 'logs/duplicate_attack.txt'
        duplicateother = 'logs/duplicate_otheratt.txt'
        dupedfile = open(duplicatedfile, 'a')
        # load list
        # print load_write_listfile.checkfile(), here get a large list!
        attackedlist = sur_load_listfile.checkfile()
        # filereadlist, xsslist, sqlilist, cvelist, iislist, urlscanlist, cmdexelist, scanlist, xxelist = \
        #    sur_load_listfile.checkfile()

        count = 0
        # tmp means hostname and url, join the new url+host and match if it is in the loaded list
        if 'hostname' in idsdata.keys() and 'url' in idsdata.keys():
            tmp = idsdata['hostname'] + idsdata['url']
            if tmp not in attackedlist:
                attackedlist.append(tmp)
                dupedfile.write(str(idsdata) + '\n')
                dupedfile.close()
                sur_load_listfile.writelist(attackedlist)
        else:
            dupofile = open(duplicateother, 'a')
            dupofile.write(str(idsdata) + '\n')
            dupofile.close()


    except Exception as e:
        record_err.logrecord()


def catagory(idsdata):
    try:
        attack_type = 0
        other_alert = open('logs/other_alert.txt', 'a')
        httpcatafile = open('logs/http_cat.txt', 'a')
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
        elif 'idq attempt' in alert:
            idsdata['catagory'] = 'read_file'
        elif 'ida attempt' in alert:
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
        elif 'executable downloader high likelihood' in alert:
            idsdata['catagory'] = 'read_file'
        elif '.cnf access' in alert:
            idsdata['catagory'] = 'read_file'
        elif 'Tomcat directory traversal attempt' in alert:
            idsdata['catagory'] = 'read_file'
        elif 'phpinfo access' in alert:
            idsdata['catagory'] = 'read_file'
        elif 'cnf access' in alert:
            idsdata['catagory'] = 'read_file'
        # xxe
        elif 'XXE' in alert:
            idsdata['catagory'] = 'xxe_attack'
        # iis
        elif 'EXPLOIT iisadmpwd' in alert:
            idsdata['catagory'] = 'iis_attack'
        elif 'iissamples access' in alert:
            idsdata['catagory'] = 'iis_attack'
        elif 'ASP file access' in alert:
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
        elif 'Access to /phppath/php' in alert:
            idsdata['catagory'] = 'cmd_execute'
        elif 'System Command' in alert:
            idsdata['catagory'] = 'cmd_execute'
        elif 'PHP config option' in alert:
            idsdata['catagory'] = 'cmd_execute'
        elif 'PHP tags in HTTP' in alert:
            idsdata['catagory'] = 'cmd_execute'
        elif 'perl command attempt' in alert:
            idsdata['catagory'] = 'cmd_execute'
        # scanner
        elif 'SCAN Nessus' in alert:
            idsdata['catagory'] = 'scanner'


        else:
            attack_type = 1
            #"这里记录的是没有被规则命中的"
            other_alert.write(str(idsdata))
            other_alert.write('\n')
            return
            # here need back to the next line
        if attack_type == 0:
            httpcatafile.write(str(idsdata))
            httpcatafile.write('\n')
        # deldupl(idsdata)

    except Exception as e:
        record_err.logrecord()


def readfile(content):
    # change str to dict
    try:
        #"otherattackfile 记录的是非http流量"
        otherattackfile = open('logs/other_attack.txt', 'a')
        new_dict = {}
        new_dict['status'] = ''
        new_dict['postdata'] = ''
        new_dict['payload'] = ''
        new_dict['method'] = ''
        new_dict['length'] = ''
        # if content is json str, convert to dict
        con_dict = json.loads(content)
        # otherattackfile.write(str(con_dict))
        # otherattackfile.write('\n')
        # check if content is http or not
        conkey = con_dict.keys()
        if u'http' in conkey:
            new_dict['http'] = (con_dict[u'http'])
            if u'status' in new_dict['http'].keys():
                new_dict['status'] = str(new_dict[u'http'][u'status'])
            if u'http_user_agent' in new_dict['http'].keys():
                new_dict['useragent'] = str(new_dict[u'http'][u'http_user_agent'])
            if u'url' in new_dict['http'].keys():
                new_dict['url'] = str(new_dict[u'http'][u'url'])
            if u'hostname' in new_dict['http'].keys():
                new_dict['hostname'] = str(new_dict[u'http'][u'hostname'])
            if u'xff' in new_dict['http'].keys():
                new_dict['xff'] = str(new_dict[u'http'][u'xff'])
            if u'http_method' in new_dict['http'].keys():
                new_dict['method'] = str(new_dict[u'http'][u'http_method'])
            if u'request_body' in new_dict['http'].keys():
                new_dict['postdata'] = str(new_dict[u'http'][u'request_body'])
            if u'length' in new_dict['http'].keys():
                new_dict['length'] = str(new_dict[u'http'][u'length'])
            if u'src_ip' in conkey:
                new_dict['src_ip'] = str(con_dict[u'src_ip'])
            if u'src_port' in conkey:
                new_dict['src_port'] = str(con_dict[u'src_port'])
            if u'dest_ip' in conkey:
                new_dict['dest_ip'] = str(con_dict[u'dest_ip'])
            if u'dest_port' in conkey:
                new_dict['dest_port'] = str(con_dict[u'dest_port'])
            if u'timestamp' in conkey:
                new_dict['datetime'] = str(con_dict[u'timestamp'])
            if u'alert' in conkey:
                new_dict['alert'] = str(con_dict[u'alert'][u'signature'])
            if u'payload' in conkey:
                new_dict['payload'] = str(con_dict[u'payload'])

            new_dict.pop('http')
            # debug test
            catagory(new_dict)
            # debug leave @ 20170930
            # httpattackfile.write(str(con_dict))
            # httpattackfile.write('\n')
            # httpattackfile.close()
        else:
            pass
            # print con_dict
            otherattackfile.write(str(con_dict))
            otherattackfile.write('\n')
            otherattackfile.close()
            # return
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
            file_record = open('logs/file_no.txt', 'a')
            file_count = filecount(logfile)
            file_record.write(str(processed_line))
            file_record.write('\n')
            file_record.close()
            if file_count > processed_line:
                processed_line = filename(logfile, file_count, processed_line + 1)
                # record the last processed line number
            time.sleep(3)
    except Exception as e:
        record_err.logrecord()

if __name__ == '__main__':
    fileinfo('abc.txt', 2)