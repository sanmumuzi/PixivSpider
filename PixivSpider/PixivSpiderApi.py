# -*- coding:utf-8 -*-

import json
# import sys, os
# sys.path.insert(0, os.path.abspath(os.pardir))  # only to test.
import logging
from typing import Dict

from PixivSpider.base import ProgrammingError
from PixivSpider.decorators import timethis
from PixivSpider.pixiv_spider import *

logging.basicConfig(level=logging.DEBUG)

__all__ = ['get_a_picture', 'get_picture_info', 'get_painter_info', 'get_all_picture_of_painter', 'add_bookmark',
           'get_painter_id']


def init_class(cls, account=None, password=None, **kwargs):  # Initialize all classes that need to be logged in.
    instance = cls(**kwargs)
    instance.login(account, password)
    return instance


@timethis
def check_login_status(account=None, password=None, enforce=False, cookies_dict=None, token_str=None,
                       return_auth_info=False):
    """
    Test whether you can log in pixiv.net or not.

    :param account: Website account of pixiv.net.
    :param password: Website password of pixiv.net.
    :param enforce: bool type: Force login with account and password
    :return: Dict type: If login_status is True, return_dict have 'auth_info' key. Otherwise, don't have the key.
    """
    instance = Pixiv(cookies_dict=cookies_dict, token_str=token_str)
    return_dict = {}
    if enforce:
        login_status = instance.login_with_account(account, password)  # Force login with account and password
    else:
        instance.login(account, password)  # normal login. Ignore return value.
        login_status = instance.already_login()
    return_dict['login_status'] = login_status
    if return_auth_info and login_status:  # If login_status is True, return_dict['auth_info'] is invalid.
        return_dict['auth_info'] = {'ps_user_id': instance.get_my_id(),
                                    'cookies': json.dumps(instance.get_cookies_dict()),
                                    'token': instance.get_token(enforce_update=True)}
    return return_dict


@timethis
def get_illust_base_info(picture_id, p=None, account=None, password=None, cookies_dict=None, token_str=None) -> Dict:
    x = init_class(PixivDownload, account, password, picture_id=picture_id, cookies_dict=cookies_dict,
                   token_str=token_str)
    illust_base_info = x.get_illust_base_info()
    resp_text = x.get_resp_text()
    return {'illust_base_info': illust_base_info, 'resp_text': resp_text}


@timethis
def get_a_picture(picture_id, p=None, dirname=None, account=None, password=None, cookies_dict=None, token_str=None,
                  info_dict=None):
    """
    Download illust from pixiv.net.
    :param dirname: illust saved directory
    :param info_dict: Dict: download illust directly by using info_dict
    :return: Dict
    """
    x = init_class(PixivDownload, account, password, picture_id=picture_id, cookies_dict=cookies_dict,
                   token_str=token_str)  # 使用下载类
    if info_dict is None:
        if dirname is not None:
            save_path_list = x.download_picture(p, dirname)  # 用户自己特定路径
        else:
            save_path_list = x.download_picture(p)  # 下载图片，获取图片保存路径
    else:
        if dirname is not None:
            save_path_list = x.download_picture_directly(dirname, **info_dict)  # 用户自己特定路径
        else:
            save_path_list = x.download_picture_directly(**info_dict)  # 下载图片，获取图片保存路径
    if save_path_list:
        logging.debug('Illust save successful: {}'.format(picture_id))
        logging.info('Picture save path: {}'.format(save_path_list))
    else:
        logging.error('Download failed: {}...'.format(picture_id))
    resp_text = x.get_resp_text()  # 只是为了能够减少访问次数，可用于其他功能
    return {'illust_base_info': x.picture_base_info, 'save_path_list': save_path_list, 'resp_text': resp_text}
    # illust base information:
    # four elements dict: picture_id, p, date, picture file type


@timethis
def get_picture_info(picture_id=None, resp: str = None, account=None, password=None, cookies_dict=None, token_str=None):
    """
    Get illust information.
    :param resp: str: html text about illust detail page
            (https://www.pixiv.net/member_illust.php?mode=medium&illust_id={picture_id})
    :return: Dict: illust information is consist of illust_id, title, introduction, bookmark_num, user_id
    """
    x = init_class(PixivPictureInfo, account, password, picture_id=picture_id, cookies_dict=cookies_dict,
                   token_str=token_str)  # 使用图片信息类
    return x.get_picture_info(resp=resp)  # 优先使用resp,如果没有再使用picture_id


@timethis
def add_bookmark(picture_id, comment='', tag='', account=None, password=None, cookies_dict=None, token_str=None):
    try:
        comment, tag = str(comment), str(tag)  # Detect whether tags and comments are strings.
    except Exception as e:
        logging.error(e)
        comment = tag = ''  # If the conversion fails, it is '' by default.
    finally:
        x = init_class(PixivOperatePicture, account, password, picture_id=picture_id, cookies_dict=cookies_dict,
                       token_str=token_str)  # 使用操作图片类
        return x.bookmark_add(comment, tag)
        # return x.bookmark_add(comment, tag)
        # return whether to add a bookmark successfully via http status code.
        # code:200 -> success -> True, code: not 200 -> failure -> False


@timethis
def get_painter_id(picture_id=None, resp=None, account=None, password=None, cookies_dict=None, token_str=None):
    """
    Only get painter id via picture id or picture detail page.

    :param picture_id: Use this picture to get its creator.
    :param resp: html text of picture detail page
    :param account: Website account of pixiv.net
    :param password: Website password of pixiv.net
    :return:
    """
    if resp is None and picture_id is None:
        raise ProgrammingError('参数不够...')
    else:
        if resp is not None:
            x = init_class(PixivPainterInfo, account, password, cookies_dict=cookies_dict, token_str=token_str)
            painter_id = x.get_painter_id_from_work_detail_page(resp=resp)
        else:
            x = init_class(PixivPainterInfo, account, password, picture_id=picture_id, cookies_dict=cookies_dict,
                           token_str=token_str)
            painter_id = x.get_painter_id_from_work_detail_page()
        return painter_id


@timethis
def get_painter_info(painter_id=None, picture_id=None, resp=None, account=None, password=None, cookies_dict=None,
                     token_str=None):
    """
    Get user information.
    :return: Dict: {'user_id': ..., 'Profile': {...}}
    """
    x = init_class(PixivPainterInfo, account, password, painter_id=painter_id, picture_id=picture_id,
                   cookies_dict=cookies_dict, token_str=token_str)
    # use painter information class.
    if painter_id is not None or picture_id is not None or resp is not None:
        if resp is not None:
            x.get_painter_id_from_work_detail_page(resp=resp)
        if painter_id is None:
            x.get_painter_id_from_work_detail_page()  # get painter id via picture id, modify self.painter_id
        return x.get_painter_info()  # get painter information via painter id
        # The data returned is a dictionary.
    else:
        raise ProgrammingError('painter id and picture id have at least one.')


# 不知道当初为什么会写这个接口，感觉好傻逼，根本用不到，再者就算用到，这
# 么长的执行时间，还不知道怎么办，单纯用，肯定直接就卡死了，这个接口也没什么可使用
# 的必要，拆开来一样可以用，不知道为什么搞了个这么没用的接口
# 该接口暂时废弃，不再更新
@timethis
def get_all_picture_of_painter(painter_id=None, picture_id=None, account=None, cookies_dict=None, token_str=None,
                               password=None):
    if painter_id is not None or picture_id is not None:
        if painter_id is None:
            x = init_class(PixivPainterInfo, account, password, picture_id=picture_id, cookies_dict=cookies_dict,
                           token_str=token_str)
            # get painter id via picture id.
            painter_id = x.get_painter_id_from_work_detail_page()
        x = init_class(PixivAllPictureOfPainter, account, password, painter_id=painter_id, cookies_dict=cookies_dict,
                       token_str=token_str)
        x.get_work_of_painter()  # download all picture of the painter.
    else:
        raise ProgrammingError('painter id and picture id have at least one.')


@timethis
def get_bookmarks(painter_id=None, picture_id=None, account=None, password=None, cookies_dict=None, token_str=None):
    """
    Get all the bookmarks of a specified user.

    :param painter_id: Specified user.
    :param picture_id: Use this picture to get its creator.
    :param account: Website account of pixiv.net.
    :param password: Website password of pixiv.net.
    :return:
        A generator yield bookmark_list is consist of many bookmark_dict.
        bookmark_dict: illust_id, illust_title, illust_tags_list, user_id, user_name, bookmark_num.
    """

    if painter_id is not None or picture_id is not None:
        if painter_id is None:
            x = init_class(PixivPainterInfo, account, password, picture_id=picture_id, cookies_dict=cookies_dict,
                           token_str=token_str)
            painter_id = x.get_painter_id_from_work_detail_page()
        y = init_class(PixivBookmark, account, password, painter_id=painter_id, cookies_dict=cookies_dict,
                       token_str=token_str)
        return y.get_bookmarks_info()  # return a generator
    else:
        raise ProgrammingError('painter id and picture id have at least one.')


if __name__ == '__main__':
    # get_a_picture(58501385)
    # print(get_picture_info(58501385))
    # print(add_bookmark(60732070))
    # print(get_painter_info(picture_id=58501385))
    # get_all_picture_of_painter(picture_id=58501385)
    # print(get_a_picture.__module__, get_a_picture.__class__, get_a_picture.__name__)
    # x = get_bookmarks(painter_id=1980643)
    # x = get_a_picture(picture_id=68698234, cookies_dict=cookies_dict, return_auth_info=True)
    # from pprint import pprint
    # pprint(x)
    # t = json.loads(x['auth_info']['cookies'])
    # print(t)
    # 仰望高端操作，看看能不能把测试写进注释里
    pass
