from datetime import datetime
import logging

logging.basicConfig(level=logging.DEBUG)


def test_rank(date, p=1):
    from PixivSpider.pixiv_spider import PixivRank
    x = PixivRank()
    rank_json_data = x.get_daily_rank(date, p)
    return rank_json_data

def start_test_rank():
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

# # 我们根本没法在这里测试, info_folder 的目录不一样，请求是没意义的
# def test_get_a_picture(picture_id=68698234):
#     from PixivSpider.PixivSpiderApi import get_a_picture
#     illust_base_info, save_path_list, resp_text = get_a_picture(picture_id=picture_id)
#     return illust_base_info, save_path_list
#
# def start_test_get_a_picture():
#     print(test_get_a_picture())


if __name__ == '__main__':
    # start_test_rank()
    # start_test_get_a_picture()
    pass