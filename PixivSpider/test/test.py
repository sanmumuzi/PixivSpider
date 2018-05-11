from datetime import datetime
import logging

logging.basicConfig(level=logging.DEBUG)


def test_rank(date, p=1):
    from PixivSpider.pixiv_spider import PixivRank
    x = PixivRank()
    rank_json_data = x.get_daily_rank(date, p)
    return rank_json_data


if __name__ == '__main__':
    rev_1 = test_rank(20160201)
    rev_2 = test_rank('20160201')
    rev_3 = test_rank(datetime(2016, 2, 1))
    try:
        assert rev_1 == rev_2 == rev_3 is not None
    except AssertionError as e:
        logging.error(e)
        raise
    else:
        logging.debug('Get rank success.')
