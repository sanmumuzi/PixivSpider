# -*- coding:utf-8 -*-
from setuptools import find_packages, setup

setup(
    name='PixivSpider',
    version='0.2.7',
    description='Get picture files and related information of pixiv.',
    author='sanmumuzi',
    author_email='san332627946@gmail.com',
    url='https://github.com/sanmumuzi/PixivSpider',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'requests>=2.18.4',
        'lxml>=4.1.1',
    ],
    entry_points={
        'console_scripts': [
            'PixivSpider = PixivSpider.command_line:logic_call'
        ]
    },
    license='GNU General Public License v3.0',
    classifiers=[
        'Programming Language :: Python',
    ]
)
