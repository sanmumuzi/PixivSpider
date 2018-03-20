import sys
import os

from PixivSpider.setting import db_path
from PixivSpider.db_func import create_db_and_table
from PixivSpider.command_line import process_args
from PixivSpider.gui_var import root


def transform(_):
    if not _: return ''
    else: return _


def main():
    data_dict = process_args()
    if data_dict['gui']:
        root.mainloop()
        # GUI.painterid_var.set(transform(data_dict.get('painter_id')))
        # GUI.username_var.set(transform(data_dict.get('username')))
        # GUI.passwd_var.set(transform(data_dict.get('password')))
        # GUI.root.mainloop()
        pass
    # elif data_dict.get('painter_id'):
    #     demo = Pixiv()
    #     if demo.login(data_dict.get('username'), data_dict.get('password')):
    #         demo.get_work_of_painter(data_dict['painter_id'])
    #     else:
    #         print('登录无法成功...')
    #         sys.exit(1)
    else:
        root.mainloop()  # only for test !!!
        # print('参数错误,无法启动...')
        # sys.exit(1)


def pre_test():  # 这里以后要改，对于各种文件，eg: artist_work, cookies, token这些文件一开始都是没有的，要先创建！
    if not os.path.exists(db_path):
        print('初始化数据库...{}'.format(db_path))
        create_db_and_table()
    else:
        print('数据库存在...{}'.format(db_path))


if __name__ == '__main__':
    pre_test()
    main()
