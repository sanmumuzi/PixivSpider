from PIL import Image
from spider.pixiv_spider import *


def resize_img(file_name, width, height):
    img = Image.open(file_name)
    (x, y) = img.size
    temp_x = x / width  # 放大倍数
    temp_y = y / height
    print(temp_x, temp_y)
    if temp_x > temp_y:
        print(width, int(y / temp_x))
        return img.resize((width, int(y / temp_x)), Image.ANTIALIAS)
    else:
        print(int(x / temp_y), height)
        return img.resize((int(x / temp_y), height), Image.ANTIALIAS)


def get_a_picture(picture_id, account=None, password=None):
    x = PixivDownload(picture_id)
    x.login()
    x.download_picture()
    y = PixivPictureInfo(work_id=picture_id, resp=x.get_html())
    y.login()
    print(y.get_picture_info())


def add_bookmark(picture_id, comment, tag):
    x = PixivOperatePicture(picture_id)
    x.login()
    x.bookmark_add(comment, tag)


def get_all_pictures_of_painter(painter_id):
    x = PixivAllPictureOfPainter(painter_id)
    x.login()
    x.get_work_of_painter()


