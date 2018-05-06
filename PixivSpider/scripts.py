# -*-coding:utf-8 -*-

"""
This file is just a separate script
"""

import requests
from datetime import datetime, timedelta
import logging
from functools import wraps

from PixivSpider.setting import (mode_set, daily_rank_info_mode, male_rank_info_mode, female_rank_info_mode)


logging.basicConfig(level=logging.DEBUG)

# 这里获取的是当前的中国时间，如果P站按照日本时间进行更新，那么这里时间会出现偏差，
# 但应该不会报错，因为北京时间比东京时间晚一个小时，所以应该只会慢，而不会出现超前报错。


class TimeContentError(Exception):
    pass


class NoModeError(Exception):
    pass


# def check_rank_argument(func):
#     @wraps(func)
#     def wrapper(mode, date):
#         if mode not in mode_set:
#             logging.error('No {} mode.'.format(mode))
#             raise NoModeError
#         elif len(date) != 3:
#             logging.error('The len of date should be 3')
#             raise ValueError('The len of start_date should be 3.')
#         else:
#             result = func(mode, date)
#         return result
#     return wrapper


def check_rank_argument(func):
    @wraps(func)
    def wrapper(mode, start_date, **kwargs):
        if mode not in mode_set:
            logging.error('No {} mode.'.format(mode))
            raise NoModeError
        elif len(start_date) != 3:
            logging.error('The len of start_date should be 3.')
            raise ValueError('The len of start_date should be 3.')
        else:
            year, month, day = start_date
            start_date = datetime(year, month, day)

            try:
                end_date = kwargs['end_date']
            except KeyError as e:
                end_date = datetime.now() - timedelta(days=2)
                # Use the day before yesterday because there may be an error if use yesterday.

            if type(end_date) != datetime:
                if len(end_date) != 3:
                    logging.error('The len of start_date should be 3.')
                    raise ValueError('The len of start_date should be 3.')
                else:
                    end_date = datetime(*end_date)
            logging.debug('start_date: {}, end_date: {}'.format(start_date, end_date))

            if end_date < start_date:
                logging.error('start_date > end_date')
                raise TimeContentError
        result = func(mode, start_date, end_date=end_date)
        return result
    return wrapper


def convert_date_format(yesterday):
    """
    Convert a datetime.datetime object to a string.
    eg: 2018-05-04 21:11:46.316617 -> 20180504
    :param yesterday: a datetime.datetime object
    :return: str
    """
    return str(yesterday.year), str(yesterday.month).zfill(2), str(yesterday.day).zfill(2)


@check_rank_argument
def get_rank_script(mode, start_date, **kwargs):
    """
    A script that get rank data from start_date to end_date.
    :param mode: rank mode
    :param start_date: ranking from start_date
    :param kwargs: If end_date is not in kwargs,
        the default value of end_date is the day before yesterday.
    :return: None
    """
    query_date = start_date
    end_date = kwargs['end_date']
    i = 1
    while True:
        if query_date <= end_date:
            year, month, day = convert_date_format(query_date)
            date_str = year + month + day
            # Note: It can be optimized!
            while True:
                url = daily_rank_info_mode.format(date=date_str, p=i)

                r = requests.get(url)
                if r.status_code == 200:
                    with open('{}_rank_{}_part_{}.json'.format(mode, date_str, i), 'wt', encoding='utf-8') as f:
                        f.write(r.text)
                    i += 1
                else:
                    logging.error('{}, {}: {}'.format(url, r.status_code, r.text))
                    break
            query_date += timedelta(days=1)
        else:
            break


if __name__ == '__main__':
    # get_rank_script('daily', start_date=(2018, 5, 1), end_date=(2018, 5, 4))
    get_rank_script('daily', start_date=(2018, 5, 3))
