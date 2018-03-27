# -*- coding:utf-8 -*-
import argparse
import json
import os
from pprint import pprint

from PixivSpider.PixivSpiderApi import *
from PixivSpider.setting import save_folder


# import sys
# sys.path.insert(0, os.path.abspath(os.pardir))  # only to test.


def process_args():  # 使用argparse库分析命令行参数
    parser = argparse.ArgumentParser(
        description='Download pictures for Pixiv Painter.'
    )
    # parser.add_argument('-g', '--gui', action='store_true', help='Open the GUI.')
    parser.add_argument('-u', '-account', dest='account', action='store', help='Your Pixiv_username.')
    parser.add_argument('-p', '-password', dest='password', action='store', help='Your Pixiv_password.')
    # parser.add_argument('-pid', '--painter_id', help='Painter ID', required=True)
    parser.add_argument('-painter_id', dest='painter_id', nargs='*',
                        help='Painter ID. '
                             '(If picture_id and painter_id are set at the same time, only picture_id is valid.)')
    parser.add_argument('-picture_id', dest='picture_id', nargs='*',
                        help='Picture ID. '
                             '(If picture_id and painter_id are set at the same time, only picture_id is valid.)')
    parser.add_argument('-dpic', '--download_picture', dest='download_picture', action='store_true',
                        help='download picture')
    parser.add_argument('-picInfo', dest='download_picture_info', action='store_true',
                        help='download picture information')
    parser.add_argument('-addMark', dest='add_bookmark', action='store_true', help='add bookmark')
    parser.add_argument('-addComment', dest='add_comment', action='store', help='comment')
    parser.add_argument('-addTag', dest='add_tag', action='store', help='tag')
    parser.add_argument('-paiInfo', dest='download_painter_info', action='store_true',
                        help='download painter information')
    parser.add_argument('-allPic', dest='download_all_picture', action='store_true',
                        help='download all picture of a painter')
    parser.add_argument('-o', '--outpath', dest='outpath', action='store', help='out path')
    # parser.add_argument('-df', '--dataformat', dest='data_format', action='store',
    #                     choices={'json', 'python'}, default='json', help='Data storage format')
    # note: only absolute paths are supported at this version
    # And only have a ID (picture id or painter id).
    # ...等将来完善吧...
    args = parser.parse_args()
    return args


def logic_call():
    args = process_args()
    base_args_check(args)  # 参数检查
    if args.outpath is None:
        args.outpath = save_folder  # default storage path.

    if args.picture_id is not None:  # picture_id 和 painter_id 只有一个有作用，picture_id优先
        for picture_id in args.picture_id:  # allow use multiple parameters.
            if args.download_picture:
                get_a_picture(picture_id, args.outpath, args.account, args.password)
            if args.download_picture_info:
                picture_info = get_picture_info(picture_id, args.account, args.password)
                print_picture_info(picture_info)
                save_json_data_file(os.path.join(args.outpath, 'picture_info'), picture_info)
            if args.download_painter_info:
                painter_info = get_painter_info(picture_id=picture_id, account=args.account,
                                                password=args.password)
                print_painter_info(painter_info)
                save_json_data_file(os.path.join(args.outpath, 'painter_info'), painter_info)
            if args.add_bookmark:
                add_bookmark(picture_id=picture_id, comment=args.add_comment, tag=args.add_tag,
                             account=args.account, password=args.password)
            if args.download_all_picture:
                get_all_picture_of_painter(picture_id=picture_id, account=args.account,
                                           password=args.password)
    elif args.painter_id is not None:
        for painter_id in args.painter_id:
            if args.download_painter_info:
                painter_info = get_painter_info(painter_id=painter_id, account=args.account,
                                                password=args.password)
                print_painter_info(painter_info)
                save_json_data_file(os.path.join(args.outpath, 'painter_info'), painter_info)
            if args.download_all_picture:
                get_all_picture_of_painter(painter_id=painter_id, account=args.account,
                                           password=args.password)


def print_picture_info(picture_info):
    picture_id, picture_title, picture_introduction, alreadymark = picture_info
    print('The current picture ID is {}.'.format(picture_id))
    print('The current picture\'s title is {}.'.format(picture_title))
    print('The current picture\'s introduction is {}.'.format(picture_introduction))
    if alreadymark is None:
        alreadymark = 'The feather is not yet realized.'
    print('Whether the current picture is bookmarked : {}'.format(alreadymark))


def print_painter_info(painter_info):
    pprint(painter_info)


def base_args_check(args):
    try:
        if args.painter_id is not None:
            [int(x) for x in args.painter_id]
        if args.picture_id is not None:
            [int(x) for x in args.picture_id]
    except ValueError as e:
        print('ID 必须为数字...')
        raise
    if args.outpath is not None:
        if os.path.isdir(args.outpath):
            pass
        else:
            os.makedirs(args.outpath)


def save_json_data_file(filepath, native_data):  # Append data to file.
    try:
        with open(filepath, 'rt') as f:  # Read the original data in the file
            pre_data = json.load(f)  # json -> built-in data type
            pre_data.append(native_data)
        with open(filepath, 'wt') as p:
            json.dump(pre_data, p)  # built-in data type -> json
    except FileNotFoundError as e:
        temp_list = [native_data]  # Use a list wrapper when add data firstly.
        with open(filepath, 'wt') as f:
            json.dump(temp_list, f)


if __name__ == '__main__':
    # args = process_args()
    # print('args.account: ', args.account)
    # print('args.password: ', args.password)
    # print('args.painter_id: ', args.painter_id)
    # print('args.picture_id: ', args.picture_id)
    # print('args.download_picture: ', args.download_picture)
    # print('args.download_picture_info: ', args.download_picture_info)
    # print('args.add_bookmark: ', args.add_bookmark)
    # print('args.add_comment: ', args.add_comment)
    # print('args.add_tag: ', args.add_tag)
    # print('args.download_painter_info', args.download_painter_info)
    # print('args.download_all_picture', args.download_all_picture)
    logic_call()
