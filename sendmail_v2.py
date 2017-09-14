# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
调用发邮件
"""
import email
import smtplib
import imaplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send(user, password, to_list, cc_list, tag, msg, doc):
    '''
    发送邮件
    '''
    try:
        server = smtplib.SMTP_SSL("smtp.exmail.qq.com", port=465)
        server.login(user, password)
        server.sendmail("<%s>" % user, to_list + cc_list, get_attach(user, password, to_list, cc_list, tag, msg, doc))
        server.close()
        print "send email successful"
    except Exception, e:
        print "send email failed %s" % e


def get_attach(user, password, to_list, cc_list, tag, msg, doc):
    '''
    构造邮件内容
    '''
    attach = MIMEMultipart()
    mail_txt = MIMEText("你好,a test mail!")
    attach.attach(mail_txt)
    if tag is not None:
        # 主题,最上面的一行
        attach["Subject"] = tag
    if user is not None:
        # 显示在发件人
        attach["From"] = "<%s>" % user
    if to_list:
        # 收件人列表
        attach["To"] = ";".join(to_list)
    if cc_list:
        # 抄送列表
        attach["Cc"] = ";".join(cc_list)
    if doc is not None:
        # 估计任何文件都可以用base64，比如rar等
        # 文件名汉字用gbk编码代替
        for i in range(len(doc)):
            file = doc[i]
            print file
            name = os.path.basename(file).encode("gbk")
            f = open(file, "rb")
            doc = MIMEText(f.read(), "base64", "gb2312")
            doc["Content-Type"] = 'application/octet-stream'
            doc["Content-Disposition"] = 'attachment; filename="' + name + '"'
            attach.attach(doc)
            f.close()
    return attach.as_string()

def get_conf(filename = None):
    file = open('mail.conf','r')
    content = file.readlines()
    to_list = []
    cc_list = []
    tmp = [1, 2, 3, 4]
    for i in range(len(content)):
        # print content[i]
        tmp1 = content[i].split('=')
        tmp[i] = tmp1[1]
        #tmp[i] = tmp1[1]
        #print tmp[i]
    tmp_tolist = tmp[0].split(',')
    if len(tmp_tolist) == 1:
        to_list.append(tmp[0].strip())
    else:
        for i in range(len(tmp_tolist)):
            to_list.append(tmp_tolist[i].strip())
    tmp_cclist = tmp[1].split(',')
    if len(tmp_cclist) == 1:
        cc_list.append(tmp[1].strip())
    else:
        for i in range(len(tmp_cclist)):
            cc_list.append(tmp_cclist[i].strip())
            #print tmp_tolist

    user = tmp[2].strip()
    password = tmp[3].strip()
    to_list = to_list
    cc_list = cc_list
    tag = "个人测试"
    msg = MIMEText(u'hello你好,send by Python...', 'plain', 'utf-8')
    doc = []
    #doc = ['2017-09-13']
    # my.doc = ['abc.doc','bcd.doc']
    doc.append(filename)
    send(user, password, to_list, cc_list, tag, msg, doc)