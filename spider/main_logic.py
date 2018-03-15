from operate_db.db_func import *
from spider.pixiv_spider import *

__all__ = ('get_a_picture', 'get_all_pictures_of_painter', 'add_bookmark', 'button_of_get_a_picture')


def get_a_picture(picture_id, account=None, password=None):
    x = PixivDownload(picture_id)
    x.login()
    x.download_picture()
    insert_picture_base_info_from_download(x.picture_bse_info)


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


def button_of_get_a_picture(picture_id, account, password):  # 主控函数
    x = PixivDownload(picture_id)  # 使用下载类
    x.login(account, password)
    save_path = x.download_picture()  # 下载，返回保存路径
    resp = x.get_resp_object()  # 获取resp object

    picture_base_info = search_picture_base_info(picture_id)  # 通过数据库查询获取图片基本信息
    if picture_base_info is not None:
        pass

    picture_info = search_picture_info(picture_id=picture_id)  #
    y = PixivPictureInfo(work_id=picture_id, resp=resp)  # 使用图片信息类
    y.login()
    picture_info = y.get_picture_info()  # 获取图片信息

    z = PixivPainterInfo(picture_id=picture_id)
    # 通过图片ID访问图片具体信息页面，获取画师基本信息
    painter_id, painter_name = z.get_painter_info_from_work_detail_page(resp=resp)

    # 向数据库中插入数据
    insert_picture_base_info_from_download(*x.picture_base_info, painter_id)
    insert_painter_base_info_from_picture_detail_page(painter_id, painter_name)

    if picture_info['introduction'] is None:
        insert_picture_info_from_PixivPictureInfo(y.work_id, painter_id, picture_info.get('title'))
    else:
        insert_picture_info_from_PixivPictureInfo(y.work_id, painter_id, picture_info.get('title'),
                                                  picture_info.get('introduction'))

    return save_path, picture_info  # 返回信息，以供GUI使用


if __name__ == "__main__":
    pass
