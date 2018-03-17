import re
import os
from collections import namedtuple

Url_namedtuple = namedtuple('Url', 'login_url post_url setting_url')
RE_namedtuple = namedtuple('RE_dict', 'post_key date pid p num p_from_source')

url_tuple = Url_namedtuple(
    login_url='https://accounts.pixiv.net/login',
    post_url='https://accounts.pixiv.net/api/login?lang=en',
    setting_url='https://www.pixiv.net/setting_profile.php',
)

re_tuple = RE_namedtuple(
    post_key=re.compile(r'name="post_key" value="(.*?)">'),
    date=re.compile(r'img/(.*)/'),  # 贪婪匹配
    pid=re.compile(r'/([0-9]+)_'),
    num=re.compile(r'^([0-9]*) results'),  # 放到外文页面上必炸
    p=re.compile(r'_p(\d+)_'),
    p_from_source=re.compile(r'_p(\d)\.')
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


def get_tt():
    token_path = os.path.join(os.path.dirname(__file__), 'cookies', 'token')
    with open(token_path, 'rt') as f:
        tt = f.read()
        print(tt)
    return tt


bookmark_add_form_data = {
    'mode': 'add',
    'tt': get_tt(),
    'id': '',
    'type': 'illust',
    'from_sid': '',
    'comment': '',  # 最多140个字符
    'tag': '',  # 最多十项， 最多1024个字符
    'restrict': '0',
}

pic_detail_page_mode = 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id={pid}'
list_of_works_mode = 'https://www.pixiv.net/member_illust.php?id={pid}'
# after_str_mode = 'https://i.pximg.net/img-original/img/{date}/{filename}.{file_type}'
after_str_mode = 'https://i.pximg.net/img-original/img/{date}/{pid}_p{p}.{file_type}'
personal_info_mode = 'https://www.pixiv.net/member.php?id={pid}'

work_num_of_each_page = 20
img_file_path = os.path.join(os.path.dirname(__file__), 'artist_work')
save_folder = img_file_path
uncategorized_save_folder = os.path.join(img_file_path, 'uncategorized_picture')

# dir_list = [os.path.abspath(os.path.join(img_file_path, relative_path)) for relative_path in
#             os.listdir(img_file_path) if os.path.isdir(os.path.abspath(os.path.join(img_file_path, relative_path)))]
#
# img_list = [os.path.join(dir_name, img)
#             for dir_name in dir_list for img in os.listdir(dir_name) if img.endswith(('.png', '.jpg'))]

img_list = [img_path for img_path in os.listdir(img_file_path) if img_path.endswith(('.png', '.jpg'))]
picture_id_list = [file_name.split('_')[0] for file_name in img_list]

# sqlite database config
db_path = os.path.join(os.path.dirname(__file__), 'db', '_pixiv.db')  # 'db\_pixiv.db'

# cookie config
COOKIE_FILE = os.path.join(os.path.dirname(__file__), 'cookies', 'cookies')  # 'cookies\cookies'

# base dir name
base_dir_name = os.path.abspath(os.path.dirname(__file__))


if __name__ == '__main__':
    print(img_list)
