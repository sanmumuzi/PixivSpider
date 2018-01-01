import re
import os
from collections import namedtuple

Url_namedtuple = namedtuple('Url', 'login_url post_url setting_url')
RE_namedtuple = namedtuple('RE_dict', 'post_key date id num')

url_tuple = Url_namedtuple(
    login_url='https://accounts.pixiv.net/login',
    post_url='https://accounts.pixiv.net/api/login?lang=en',
    setting_url='https://www.pixiv.net/setting_profile.php',
)

re_tuple = RE_namedtuple(
    post_key=re.compile(r'name="post_key" value="(.*?)">'),
    date=re.compile(r'img/(.*)/'),  # 贪婪匹配
    id=re.compile(r'/([0-9]+)_'),
    num=re.compile(r'^([0-9]*)件'),
)

User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/63.0.3239.84 Safari/537.36'

form_data = {
    'pixiv_id': '',
    'password': '',
    'captcha': '',
    'g_recaptcha_response': '',
    'post_key': '',
    'source': 'pc',
    'ref': 'wwwtop_accounts_index',
    'return_to': 'https://www.pixiv.net/'
}

COOKIE_FILE = 'cookies'
work_num_of_each_page = 20
save_folder = os.path.join(os.path.abspath(os.curdir), 'artist_work')
