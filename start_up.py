from new_crawl import Pixiv
from command_line import process_args
import GUI as gui
import sys


def transform(_):
    if not _: return ''
    else: return _


def main():
    data_dict = process_args()
    if data_dict['gui']:
        gui.painterid_var.set(transform(data_dict.get('painter_id')))
        gui.username_var.set(transform(data_dict.get('username')))
        gui.passwd_var.set(transform(data_dict.get('password')))
        gui.root.mainloop()
    elif data_dict.get('painter_id'):
        demo = Pixiv()
        if demo.login(data_dict.get('username'), data_dict.get('password')):
            demo.get_work_of_painter(data_dict['painter_id'])
        else:
            print('登录无法成功...')
            sys.exit(1)
    else:
        print('参数错误,无法启动...')
        sys.exit(1)


if __name__ == '__main__':
    main()
