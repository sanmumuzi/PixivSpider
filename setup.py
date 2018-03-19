# -*- coding:utf-8 -*-
from setuptools import setup, find_packages


setup(
    name='PixivSpider',
    version='0.0.5',
    description='Get picture files and related information of pixiv.',
    author='sanmumuzi',
    author_email='san332627946@gmail.com',
    url='https://github.com/sanmumuzi/pixiv_spider',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'requests=2.18.4',
        'lxml=4.1.1',
        'Pillow=5.0.0'
    ],
)
