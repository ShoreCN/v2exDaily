#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
The python tool works for v2ex daily sign up.
'''

import getpass
import requests
from bs4 import BeautifulSoup

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"

class v2ex(object):
    url = "https://www.v2ex.com/signin"
    headers = {
        'User-Agent' : UA,
        'Origin' : 'https://www.v2ex.com',
        'Referer' : url,
    }

    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.session = requests.Session()

    def login(self):
        print('user[%s] password[%s] Login[%s]...'%(self.user, self.password, self.url))
        #获取登陆页面的代码并使用BeautifulSoup进行解析，用于取出需要的元素
        r = self.session.get(self.url, headers = self.headers)
        bs = BeautifulSoup(r.content, 'lxml', from_encoding='utf-8')

        #获取登陆网页中的用户名密码元素变量值
        user_element = bs.find('input', {'class' : 'sl', 'type':'text'})['name']
        password_elemnt = bs.find('input', {'type' : 'password'})['name']
        print(password_elemnt)
        print('user[%s]'%user_element)
        print('password[%s]'%password_elemnt)

if __name__ == '__main__':
    user = input('Please input the user name:')
    password = getpass.getpass('Please input the password:')

    v = v2ex(user, password)
    result = v.login()