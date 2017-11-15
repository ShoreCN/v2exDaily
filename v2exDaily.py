#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
The python tool works for v2ex daily sign up.
'''

import getpass
import requests
from bs4 import BeautifulSoup
from PIL import Image
import pytesseract

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"

class v2ex(object):
    url = "https://www.v2ex.com/signin"
    headers = {
        'User-Agent' : UA,
        'Origin' : 'https://www.v2ex.com',
        'Referer' : url,
    }

    #未避免重复登录，初始化时创建session用于整个程序的使用
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
        password_element = bs.find('input', {'type' : 'password'})['name']
        once_element = bs.find('input', {'name' : 'once'})['value']

        #若出现验证码，通过tesseract识别，验证码图片url规则固定，加上once参数即可
        captcha_input = bs.find('input', {'placeholder' : '请输入上图中的验证码'})
        if captcha_input is not None:
            print('Parse captcha...')
            captch_page = self.session.get('https://www.v2ex.com/_captcha?once='+once_element, headers = self.headers)

            if captch_page.status_code == 200:
                with open('captcha.jpg', 'wb') as f:
                    f.write(captch_page.content)
                captch_img = Image.open('captcha.jpg')
                captch_str = pytesseract.image_to_string(captch_img)
            else:
                print('Failed to get the captcha image.')

            captcha_element = captcha_input['name']
            print('captcha element [%s] , captcha str[%s]'%(captcha_element,captch_str))
            captcha_by_man = input('Please input below if you want to recognize the captcha yourself, otherwise return directly:')
            if captcha_by_man != '':
                captch_str = captcha_by_man

        #构造表单数据并进行登陆
        form_data = {
            user_element : self.user,
            password_element : self.password,
            'once' : once_element,
            'next' : '/',
            captcha_element : captch_str,
        }        
        p = self.session.post(self.url, form_data, headers = self.headers)

        #根据response里是否存在'登出'字样判断用户是否已经成功登陆
        bs = BeautifulSoup(p.content, 'lxml')
        if bs.find(text = '登出') is None:
            print('Login failed.')
            return False
        else:
            print('Login successful.')
            return True

    #进行每日签到任务获取金币
    def daily(self):
        #打印每日签到任务标题
        daily_url = "https://www.v2ex.com/mission/daily"
        daily_content = self.session.get(daily_url, headers = self.headers)
        daily_bs = BeautifulSoup(daily_content.content, 'lxml')
        if daily_bs.find('li', {'class':'fa fa-ok-sign'}) is None:
            print('%s' % daily_bs.find('h1').text)
        else:
            print('Mission completed already.')
            print('%s' % daily_bs.find('li', {'class':'fa fa-ok-sign'}).parent.parent.next_sibling.next_sibling.text)
            return

        #因为签到按钮链接存在变量，此处根据获取到的实际元素拼接签到任务的URL,并根据最后的页面显示判断是否成功签到
        mission_url = "https://www.v2ex.com" + daily_bs.find('input', {'class':'super normal button'})['onclick'].split("'")[1]
        res_daily = self.session.get(mission_url, headers = self.headers)
        if BeautifulSoup(res_daily.content, 'lxml').find('li', {'class':'fa fa-ok-sign'}) is None:
            print('Daily mission failed.')
        else:
            print('Daily mission successful.')

    #获取账户余额情况
    def balance(self):
        pass

if __name__ == '__main__':
    user = input('Please input the user name:')
    password = getpass.getpass('Please input the password:')

    v = v2ex(user, password)
    result = v.login()
    if result is True:
        v.daily()
    else:
        print('V2ex daily task failed, please check the user or password.')