# -*- coding=utf-8 -*-
import re
import requests
import pickle
from lxml import etree
from time import sleep
import math
import os


class PixivSpider(object):
    def __init__(self):
        self.session = requests.session()
        self.login_url = 'https://accounts.pixiv.net/login'
        self.post_url = 'https://accounts.pixiv.net/api/login?lang=zh'
        self.setting_url = 'https://www.pixiv.net/setting_profile.php'
        self.session.headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Ge'
                'cko) Chrome/60.0.3112.113 Safari/537.36'
        }
        self.headers_original_img = {
            'referer': 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id={}',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
        }
        self.params = {
            'lang': 'zh',
            'source': 'pc',
            'view_type': 'page',
            'ref': 'wwwtop_accounts_index'
        }
        self.form_data = {
            'pixiv_id': '',
            'password': '',
            'captcha': '',
            'g_recaptcha_response': '',
            'post_key': '',
            'source': 'pc',
            'ref': 'wwwtop_accounts_index',
            'return_to': 'https://www.pixiv.net/'
        }
        self.list_of_works_mode = 'https://www.pixiv.net/member_illust.php?id={}'
        self.re_date = re.compile(r'img/(.*)/')  # 贪婪匹配
        self.re_id = re.compile(r'/([0-9]+)_')
        self.re_num = re.compile(r'^([0-9]*)件')
        self.after_str_mode = 'https://i.pximg.net/img-original/img/{date}/{id}_p0.jpg'
        self.works_of_a_page_num = 20
        self.works_params = {'type': 'all', 'p': None}

    def get_post_key(self):
        login_url = 'https://accounts.pixiv.net/login'
        login_content = self.session.get(login_url, params=self.params)
        re_post_key = re.compile(r'name="post_key" value="(.*?)">')
        self.form_data['post_key'] = re_post_key.findall(login_content.text)[0]

    def login(self, pixiv_id, password):
        post_url = 'https://accounts.pixiv.net/api/login?lang=zh'
        self.form_data['pixiv_id'] = pixiv_id
        self.form_data['password'] = password
        self.get_post_key()
        result = self.session.post(post_url, data=self.form_data).status_code
        if result == 200:
            with open('cookies', mode='wb') as p:
                pickle.dump(self.session.cookies, p)
            return True
        else:
            return False

    def already_login(self):
        status = self.session.post(self.setting_url, allow_redirects=False).status_code
        if status == 200:
            return True
        else:
            return False

    def login_enter(self):
        pixiv_id = input('Please enter your pixiv_id: ')
        password = input('Please enter your pixiv_password: ')
        if self.login(pixiv_id, password):
            print('模拟登陆成功...')
            return True
        else:
            print('模拟登陆失败...')
            return False

    def get_artist_work(self, artist_id, number=10):
        list_of_works = self.session.get(self.list_of_works_mode.format(artist_id))
        selector = etree.HTML(list_of_works.text)
        # self.works_of_page(selector=selector)  # 下载第一页的内容

        ''' 通过作品总数计算页数 '''
        # 现在有BUG, 如果该作者没有作品...就很GG
        work_num = selector.xpath('//span[@class="count-badge"]/text()')[0]
        print('该用户有{}作品...'.format(work_num))
        real_work_num = self.re_num.findall(work_num)[0]
        page_num = math.ceil(int(real_work_num) / self.works_of_a_page_num)  # 通过作品数,计算出页数
        print(work_num, page_num)

        if page_num >= 2:
            for each_page in range(2, int(page_num+1)):
                self.works_params['p'] = each_page
                list_of_works = self.session.get(self.list_of_works_mode.format(artist_id), params=self.works_params)
                selector = etree.HTML(list_of_works.text)
                self.works_of_page(selector=selector)

    def works_of_page(self, selector):
        original_img_url = selector.xpath('//img[@data-src]/@data-src')
        for item in original_img_url:
            date_str = self.re_date.findall(item)[0]
            id_str = self.re_id.findall(item)[0]
            self.headers_original_img['referer'].format(id_str)
            work_img_url = self.after_str_mode.format(date=date_str, id=id_str)
            real_img = self.session.get(work_img_url, headers=self.headers_original_img)
            print(work_img_url)
            print(real_img)

            filename = id_str+'.png'
            if os.path.isfile(filename):
                print('文件已经存在')
            else:
                with open(file=filename, mode='wb') as q:
                    q.write(real_img.content)
                    print('{}图片存储完成'.format(filename))
            sleep(10)


if __name__ == '__main__':
    pixiv_spider = PixivSpider()
    try:
        with open('cookies', mode='rb') as f:
            pixiv_spider.session.cookies = pickle.load(f)

        if pixiv_spider.already_login():
            print('用户已登录')
            artist_id = input('请输入画师ID: ')
            pixiv_spider.get_artist_work(artist_id)
        else:
            print('cookies已失效...')
            if pixiv_spider.login_enter():
                artist_id = input('请输入画师ID: ')
                pixiv_spider.get_artist_work(artist_id)
            else:
                print('放弃吧, 非洲人...')
    except FileNotFoundError:
        pixiv_spider.login_enter()
        artist_id = input('请输入画师ID: ')
        pixiv_spider.get_artist_work(artist_id)
