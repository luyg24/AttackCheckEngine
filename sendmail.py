#coding:utf8
'''
日报
'''
import email
import smtplib
import imaplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class MyEmail:
    def __init__(self):
        self.user = None
        self.passwd = None
        self.to_list = []
        self.cc_list = []
        self.tag = None
        self.doc = None
        self.msg = None

    def send(self):
        '''
        发送邮件
        '''
        try:
            server = smtplib.SMTP_SSL("smtp.exmail.qq.com", port = 465)
            server.login(self.user,self.passwd)
            server.sendmail("<%s>"%self.user, self.to_list+self.cc_list, self.get_attach())
            server.close()
            print "send email successful"
        except Exception,e:
            print "send email failed %s"%e
    def get_attach(self):
        '''
        构造邮件内容
        '''
        attach = MIMEMultipart()
        mail_txt = MIMEText("你好,a test mail!")
        attach.attach(mail_txt)
        if self.tag is not None:
            #主题,最上面的一行
            attach["Subject"] = self.tag
        if self.user is not None:
            #显示在发件人
            attach["From"] = "<%s>"%self.user
        if self.to_list:
            #收件人列表
            attach["To"] = ";".join(self.to_list)
        if self.cc_list:
            #抄送列表
            attach["Cc"] = ";".join(self.cc_list)
        if self.doc:
            #估计任何文件都可以用base64，比如rar等
            #文件名汉字用gbk编码代替
            for i in range(len(self.doc)):
                file = self.doc[i]
                print file
                name = os.path.basename(file).encode("gbk")
                f = open(file,"rb")
                doc = MIMEText(f.read(), "base64", "gb2312")
                doc["Content-Type"] = 'application/octet-stream'
                doc["Content-Disposition"] = 'attachment; filename="'+name+'"'
                attach.attach(doc)
                f.close()
        return attach.as_string()


if __name__=="__main__":
    my = MyEmail()
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

    my.user = tmp[2].strip()
    my.passwd = tmp[3].strip()
    my.to_list = to_list
    my.cc_list = cc_list
    my.tag = "个人测试"
    my.msg = MIMEText(u'hello你好,send by Python...', 'plain', 'utf-8')
    my.doc = ['2017-09-13']
    # my.doc = ['abc.doc','bcd.doc']
    my.send()