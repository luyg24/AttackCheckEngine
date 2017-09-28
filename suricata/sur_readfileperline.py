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
reload(sys)
sys.setdefaultencoding('utf8')


def deldupl(idsdata):
    try:
        duplicatedfile = 'logs/duplicate_attack.txt'
        dupedfile = open(duplicatedfile, 'a')
        # load list
        # print load_write_listfile.checkfile()
        filereadlist, xsslist, sqlilist = sur_load_listfile.checkfile()
        count = 0
        # tmp means hostname and url, join the new url+host and match if it is in the loaded list
        if 'hostname' in idsdata.keys() and 'url' in idsdata.keys():
            tmp = idsdata['url'] + idsdata['hostname']
        else:
            print idsdata
        # use status check success is success or not
        if idsdata['catagory'] == 'read_file' and idsdata['status'] == '200':
            # global filereadlist
            if tmp not in filereadlist:
                filereadlist.append(tmp)
                # write_todb.writedb(attack_data)
                dupedfile.write(str(idsdata) + '\n')
                count += 1
        elif idsdata['catagory'] == 'xss_attack' and idsdata['status'] == '200':
            # global filereadlist
            if tmp not in xsslist:
                xsslist.append(tmp)
                # write_todb.writedb(attack_data)
                dupedfile.write(str(idsdata) + '\n')
                count += 1

        # can not use status check attack is success or not
        elif idsdata['catagory'] == 'sql_inject' :
            # global filereadlist
            if tmp not in sqlilist:
                sqlilist.append(tmp)
                # write_todb.writedb(attack_data)
                dupedfile.write(str(idsdata) + '\n')
                count += 1
        else:
            pass
        if count > 0:
            # write the new list to file
            dupedfile.close()
            sur_load_listfile.writelist(filereadlist, xsslist, sqlilist)

    except Exception as e:
        record_err.logrecord()


def catagory(idsdata):
    try:
        other_alert = open('logs/other_alert.txt', 'a')
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
        elif 'Access to /phppath/php' in alert:
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
            other_alert.write(str(idsdata))
            other_alert.write('\n')
            return
            # here need back to the next line
        deldupl(idsdata)

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
            catagory(new_dict)
        else:
            otherattackfile.write(str(new_dict))
            otherattackfile.write('\n')
            otherattackfile.close()
            return
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