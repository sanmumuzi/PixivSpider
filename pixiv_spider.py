# -*- coding=utf-8 -*-
import re
import requests
import pickle
from lxml import etree
from time import sleep
import math
import os
import atexit


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
        self.after_str_mode = 'https://i.pximg.net/img-original/img/{date}/{filename}'
        self.works_of_a_page_num = 20
        self.works_params = {'type': 'all', 'p': None}
        self.file_type = '.png'
        self.dir_name = None
        self.artist_id = None
        self.port = 1080
        self.interval = 10
        self.work_list_file = 'work_list.txt'
        self.work_list = []

    def get_post_key(self):
        login_url = 'https://accounts.pixiv.net/login'
        login_content = self.session.get(login_url, params=self.params)
        re_post_key = re.compile(r'name="post_key" value="(.*?)">')
        self.form_data['post_key'] = re_post_key.findall(login_content.text)[0]

    def save_cookies(self):
        with open('cookies', mode='wb') as f:
            pickle.dump(self.session.cookies, f)

    def get_cookies(self):
        try:
            with open('cookies', mode='rb') as f:
                self.session.cookies = pickle.load(f)
        except FileNotFoundError:
            print('cookies文件不存在,开始进行模拟登陆...')
            self.login_enter()

    def save_work(self, filename, real_img, id_str):
        file_path = os.path.join(self.dir_name, filename + self.file_type)
        with open(file=file_path, mode='wb') as q:  # 存储文件
            q.write(real_img.content)
            print('{}图片存储完成'.format(filename + self.file_type))
            with open(self.work_list_file, mode='at', encoding='utf-8') as f:
                f.write(id_str + '\n')

    def create_folder(self):
        """创建文件夹"""
        if os.path.isdir(self.dir_name):  # dir_name is absolute path.
            pass
        else:
            os.makedirs(self.dir_name)

    def type_conversion(self):
        """转换文件格式"""
        if self.file_type == '.png':
            self.file_type = '.jpg'
        elif self.file_type == '.jpg':
            self.file_type = '.png'

    def login(self, pixiv_id, password):
        """login function"""
        post_url = 'https://accounts.pixiv.net/api/login?lang=zh'
        self.form_data['pixiv_id'] = pixiv_id
        self.form_data['password'] = password

        self.get_post_key()
        result = self.session.post(post_url, data=self.form_data).status_code
        if result == 200:
            self.save_cookies()
            return True
        else:
            return False

    def enter_port_and_interval(self):
        port = input('Please enter your ss/ssr local listen port(default 1080): ')
        if port:
            self.port = port
        self.session.proxies = {
            'http': 'socks5h://127.0.0.1:{}'.format(self.port),
            'https': 'socks5h://127.0.0.1:{}'.format(self.port)
        }
        interval = input('Please enter the time interval for get the picture(default 10): ')
        while interval:
            if float(interval) >= 3:
                self.interval = float(interval)
                break
            else:
                interval = float(input('interval should >= 3: '))

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

    def artist_id_enter(self):
        while True:
            try:
                self.artist_id = int(input('请输入画师ID: '))
                return True
            except ValueError:
                print('请输入正确的画师ID...')

    def check_work_list(self):
        if os.path.isfile(self.work_list_file):
            with open(self.work_list_file, mode='rt', encoding='utf-8') as f:
                for item in f:
                    self.work_list.append(item.strip())
        else:
            with open(self.work_list_file, 'w', encoding='utf-8'):
                pass

    def get_artist_work(self, number=10):
        list_of_works = self.session.get(self.list_of_works_mode.format(self.artist_id))
        selector = etree.HTML(list_of_works.text)
        user_name = selector.xpath('//a[@class="user-name"]/text()')[0]
        self.dir_name = os.path.join(os.path.abspath('.'), 'artist_work', user_name + ' ' + str(self.artist_id))
        self.create_folder()

        """ 通过作品总数计算页数 """
        # 现在有BUG, 如果该作者没有作品...就很GG
        work_num = selector.xpath('//span[@class="count-badge"]/text()')[0]
        print('该用户有{}作品...'.format(work_num))
        real_work_num = self.re_num.findall(work_num)[0]
        page_num = math.ceil(int(real_work_num) / self.works_of_a_page_num)  # 通过作品数,计算出页数
        # print(work_num, page_num)

        self.works_of_page(selector=selector)  # 下载第一页的内容

        if page_num >= 2:
            for each_page in range(2, int(page_num + 1)):
                self.works_params['p'] = each_page
                list_of_works = self.session.get(self.list_of_works_mode.format(self.artist_id),
                                                 params=self.works_params)
                selector = etree.HTML(list_of_works.text)
                self.works_of_page(selector=selector)

            # https://i.pximg.net/c/150x150/img-master/img/2017/08/31/13/35/28/64711378_p0_master1200.jpg
            # https://i.pximg.net/img-original/img/2017/08/31/13/35/28/64711378_p0.jpg
            # https://i.pximg.net/img-original/img/2017/09/06/00/12/53/64809736_p0.png

    def works_of_page(self, selector):
        """对单页的作品进行处理"""
        original_img_url = selector.xpath('//img[@data-src]/@data-src')  # 使用xpath从html页面中获取每个作品的url
        for item in original_img_url:
            date_str = self.re_date.findall(item)[0]  # 取出url中的日期部分
            id_str = self.re_id.findall(item)[0]  # 取出url中的作品id部分
            # ---------------------------------------------------------------------
            if id_str in self.work_list:
                print('ID: {} already download.'.format(id_str))
                continue
            # ------------------------------------------------------------
            filename = item.split('/')[-1].replace('_master1200.jpg', '')  # 取出url中的作品文件名
            print('filename = ', filename)
            self.headers_original_img['referer'].format(id_str)  # 修改session的headers
            work_img_url = self.after_str_mode.format(date=date_str, filename=filename + self.file_type)  # 拼接出真正的url
            real_img = self.session.get(work_img_url, headers=self.headers_original_img)
            print(work_img_url)  # 打印出图片原始页面
            if real_img.status_code == 200:
                print('访问页面成功...')
                self.save_work(filename=filename, real_img=real_img, id_str=id_str)
            else:
                print('访问页面失败...')
                print('转化文件格式类型,再次访问...')
                self.type_conversion()
                work_img_url = self.after_str_mode.format(date=date_str, filename=filename + self.file_type)
                real_img = self.session.get(work_img_url, headers=self.headers_original_img)
                print(work_img_url)
                if real_img.status_code == 200:
                    print('访问页面成功...')
                    self.save_work(filename=filename, real_img=real_img, id_str=id_str)
                else:
                    print('访问页面失败...')

            sleep(self.interval)  # 图片爬取间隔....

    def main_control(self):
        self.get_cookies()
        self.enter_port_and_interval()
        self.check_work_list()

        if self.already_login():
            print('user already login.')
            if self.artist_id_enter():
                self.get_artist_work()
        else:
            print('Use cookies failure.')
            if self.login_enter():
                if self.artist_id_enter():
                    self.get_artist_work()
            else:
                print('account or password incorrect.')


@atexit.register
def exit_pixiv_spider():
    print('exit....')


if __name__ == '__main__':
    pixiv_spider = PixivSpider()
    pixiv_spider.main_control()

# duan dian download
# qu chong
# huancunzhuangtai
# threading
# guan dao
