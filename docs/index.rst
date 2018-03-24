.. PixivSpider documentation master file, created by
   sphinx-quickstart on Sat Mar 24 13:22:55 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PixivSpider's documentation!
=======================================

PixivSpider is a web spider library about Pixiv, written in Python3.

**The power of PixivSpider:**

::

    >>> from PixivSpider import PixivSpiderApi
    >>> account = 'your Pixiv account'
    >>> password = 'your Pixiv password'
    >>> r = PixivSpiderApi.get_a_picture(picture_id=67844926, dirname='D://', account=account, password=password)
    https://www.pixiv.net/member_illust.php?mode=medium&illust_id=67844926
    200
    图片源页面访问成功...67844926
    67844926 0 2018/03/21/18/00/25 jpg
    67844926 0 2018/03/21/18/00/25 jpg
    67844926_p0.jpg保存成功...
    下载成功...67844926
    Download successful: 67844926
    Picture save path: D://67844926_p0.jpg

Feature Support
---------------
- Download picture files via picture ID.
- Get picture information via picture ID.
- Get painter information via the ID of his picture or painter ID.
- Get all picture files of the painter via the ID of his picture or painter ID.
- Add or modify bookmarks via picture ID.