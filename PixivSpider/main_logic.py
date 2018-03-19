import os

from db_func import *
from setting import picture_id_list, img_file_path
from pixiv_spider import *


__all__ = ('get_a_picture', 'get_all_pictures_of_painter', 'add_bookmark', 'button_of_get_a_picture')


def init_class(cls, account=None, password=None, **kwargs):
    print(kwargs)
    item = cls(**kwargs)
    item.login(account, password)
    return item


def get_a_picture(picture_id, account=None, password=None):
    x = PixivDownload(picture_id)
    x.login()
    x.download_picture()
    insert_picture_base_info_from_download(x.picture_base_info)


def get_picture_info(picture_id):
    x = PixivPictureInfo(work_id=picture_id)
    x.login()
    x.get_picture_info()


def add_bookmark(picture_id, comment, tag):
    x = PixivOperatePicture(picture_id)
    x.login()
    x.bookmark_add(comment, tag)


def get_all_pictures_of_painter(painter_id):
    x = PixivAllPictureOfPainter(painter_id)
    x.login()
    x.get_work_of_painter()


def button_of_get_a_picture(picture_id, account, password):  # 主控函数，使用tuple的兼容性简直爆炸。
    picture_base_info_sign = False
    related_painter_sign = False
    picture_info_sign = False  # 暂时无用
    resp = None
    if picture_id in picture_id_list:
        print('该图片已经下载完成:{}...'.format(picture_id))
    else:
        pass

    picture_base_info = search_picture_base_info(picture_id=picture_id)  # 通过数据库查询图片基本参数信息
    if picture_base_info is None:  # 没有找到对应图片ID的行
        x = init_class(PixivDownload, account, password, work_id=picture_id)
        save_path = x.download_picture()  # 下载，返回保存路径
        resp = x.get_resp_object()  # 获取 resp object
        picture_base_info = x.picture_base_info  # 获取访问基础页面所得的图片基础信息--tuple(id, p, date, file_type)
        # insert_picture_base_info_from_download()  # 当我们获取painter_id之后，再插入数据库
    else:
        file_name = str(picture_id) + '_p' + str(picture_base_info[4]) + '.' + picture_base_info[3]  # 绝望的兼容性，爆炸
        save_path = os.path.join(img_file_path, file_name)
        picture_base_info_sign = True

    if picture_base_info[1] is None:  # relation of painter and picture.
        y = init_class(PixivPainterInfo, account, password,
                       picture_id=picture_id)  # get painter info about this picture.
        painter_id = y.get_painter_info_from_work_detail_page(resp=resp)
        # 拿到了painter_id,现在查询数据库，获取画师详细信息，如若无有信息，则使用Painter类去获取，然后插入
    else:
        painter_id = picture_base_info[1]  # get painter id
        related_painter_sign = True

    # 这里其实有问题：如果连图片基本信息都没有，这条查询必然是None，这里再查询就是浪费资源。
    picture_info = search_picture_info(picture_id=picture_id)  # 通过数据库查询图片的简介类信息
    if picture_info is not None:
        picture_info_sign = True
    else:
        # 使用图片信息类
        picture_info_instance = init_class(PixivPictureInfo, account, password, work_id=picture_id, resp=resp)  # 使用图片信息类
        picture_info = picture_info_instance.get_picture_info()  # 获取图片信息
        insert_picture_info_from_picture_detail_page(*picture_info)

    if not picture_base_info_sign and not related_painter_sign:
        picture_base_info[1] = painter_id
        # insert picture_base_info
        insert_picture_base_info_from_download(*picture_base_info)
    elif picture_base_info_sign and not related_painter_sign:
        # update picture_base_info
        update_picture_base_info(picture_id=picture_id, painter_id=painter_id)

    # 查询具体的画室信息，如果有就返回，没有就通过painter_id，再获取。
    painter_info = search_painter_info(painter_id=painter_id)
    if painter_info is None:
        painter_info_instance = init_class(PixivPainterInfo, account, password, painter_id=painter_id)
        painter_info_dict = painter_info_instance.get_painter_id_info()
        painter_id = painter_info_dict['ID']
        profile_info_dict = painter_info_dict['Profile']
        insert_painter_info(ID=painter_id, **profile_info_dict)
    else:
        print(painter_info)  # should be a tuple of data

    return save_path, picture_info  # 返回信息给GUI使用...

    # picture_base_info = search_picture_base_info(picture_id=picture_id)  # 通过数据库查询获取图片基本信息
    # if picture_base_info is not None:
    #     pass
    # else:
    #     insert_picture_base_info_from_download(*x.picture_base_info)  # 这里迟早要优化，要用户可以直接拼接重要信息访问源页面

    # picture_base_info = search_picture_base_info(picture_id=picture_id)  # 通过数据库查询获取图片基本信息
    # if picture_base_info is not None:
    #     pass
    # else:  # 如果没画师的话，这里直接传个None进去
    #     insert_picture_base_info_from_download(*x.picture_base_info, painter_id)
    #     # 这里迟早要优化，要用户可以直接拼接重要信息访问源页面
    #
    # # 通过图片ID访问图片具体信息页面，获取画师基本信息
    # if painter_id is not None:
    #     painter_info = search_painter_info(painter_id=painter_id)
    #     print(painter_info)
    #     if painter_info is None:
    #         z = init_class(PixivPainterInfo, account, password, picture_id=picture_id)
    #         painter_info_dict = z.get_painter_info_from_work_detail_page(resp=resp)
    #         painter_id = painter_info_dict['ID']
    #         profile_info_dict = painter_info_dict['Profile']
    #         insert_painter_info(ID=painter_id, **profile_info_dict)
    # else:
    #     pass
    #
    # # 向数据库中插入数据
    # # insert_picture_base_info_from_download(*x.picture_base_info, painter_id)
    # # insert_painter_base_info_from_picture_detail_page(painter_id, painter_name)
    #
    # # save_path = r'D:\gitcode\pixiv_spider\artist_work\1499614\48588325_p0.jpg'
    # return save_path, picture_info  # 返回信息，以供GUI使用


if __name__ == "__main__":
    pass
