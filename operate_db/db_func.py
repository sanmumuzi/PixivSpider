import sqlite3
from functools import wraps

from operate_db.create_db import create_table_tuple
from setting import db_path

__all__ = ['create_db_and_table', 'insert_picture_base_info_from_download', 'insert_picture_info_from_PixivPictureInfo',
           'insert_painter_base_info_from_picture_detail_page', 'search_picture_base_info', 'search_picture_info']


def pre_connect(func):
    @wraps(func)
    def inner(*args):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        try:
            result = func(c, conn, *args)
        except sqlite3.Error:
            raise
        finally:
            conn.close()
        return result
    return inner


@pre_connect
def create_db_and_table(cursor, connect):  # try的重复代码太多了...
    for table in create_table_tuple:
        try:
            cursor.execute(table)
        except sqlite3.Error:
            print('Error: create table: {}.'.format(table.split(' (')[0]))
            raise
    try:
        connect.commit()
    except sqlite3.Error:
        print('Error: commit data.')
        raise


@pre_connect
def insert_picture_base_info_from_download(cursor, connect, *args):
    # picture_id, p, date, file_type = args
    try:
        cursor.execute("INSERT INTO PICTURE (ID, P, DATE, TYPE, PID) VALUES (?, ?, ?, ?, ?)", args)
    except sqlite3.IntegrityError as e:
        print(e)
        pass
        # raise
    except sqlite3.Error:
        print('Error: commit data.')
        raise
    else:
        connect.commit()


@pre_connect
def insert_picture_info_from_PixivPictureInfo(cursor, connect, *args):
    try:
        print(args)
        if len(args) == 3:
            cursor.execute('INSERT INTO PICTURE_INFO (ID, Title, Introduction) VALUES (?, ?, ?)', args)
        elif len(args) == 2:
            cursor.execute('INSERT INTO PICTURE_INFO (ID, Title) VALUES (?, ?)', args)
    except sqlite3.IntegrityError as e:
        print(e)
        pass
        # raise
    except sqlite3.Error:
        raise
    else:
        connect.commit()


@pre_connect
def insert_painter_base_info_from_picture_detail_page(cursor, connect, *args):
    try:
        cursor.execute('INSERT INTO PAINTER (ID, Nickname) VALUES (?, ?)', args)
    except sqlite3.IntegrityError as e:
        print(e)
        pass
    except sqlite3.Error:
        print('Error: commit data.')
        raise
    else:
        connect.commit()


@pre_connect
def search_picture_base_info(cursor, connect, picture_id):
    try:
        cursor.execute('SELECT * FROM PICTURE WHERE ID = {}'.format(picture_id))
    except sqlite3.Error:
        raise
    else:
        picture_base_info = cursor.fetchone()
        connect.commit()
        return picture_base_info


@pre_connect
def search_picture_info(cursor, connect, picture_id):
    try:
        cursor.execute('SELECT * FROM PICTURE_INFO WHERE ID = {}'.format(picture_id))
    except sqlite3.Error:
        raise
    else:
        picture_info = cursor.fetchone()
        connect.commit()
        return picture_info


if __name__ == '__main__':
    picture_base_info = search_picture_base_info(60778836)
    picture_info = search_picture_info(60778836)
    print(picture_base_info, picture_info)
