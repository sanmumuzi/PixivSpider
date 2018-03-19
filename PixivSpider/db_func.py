import sqlite3
from functools import wraps

from setting import db_path

__all__ = ['create_db_and_table', 'insert_picture_base_info_from_download', 'insert_picture_info_from_PixivPictureInfo',
           'insert_painter_base_info_from_picture_detail_page', 'search_picture_base_info', 'search_picture_info',
           'insert_picture_info_from_picture_detail_page', 'insert_painter_info', 'search_painter_info',
           'update_picture_base_info']


create_table_tuple = (
    # 图片基本信息数据表
    'CREATE TABLE PICTURE (ID INT PRIMARY KEY NOT NULL, PID INT , DATE TEXT NOT NULL, TYPE TEXT NOT NULL , P INT)',
    # 画师基本信息数据表
    'CREATE TABLE PAINTER (ID INT PRIMARY KEY NOT NULL, Nickname TEXT, Website TEXT, "Self introduction" TEXT)',
    # 画师标签表
    'CREATE TABLE "PAINTER_TAG" (ID INTEGER PRIMARY KEY AUTOINCREMENT, NAME TEXT NOT NULL UNIQUE)',
    # 图片标签表
    'CREATE TABLE "PICTURE_TAG" (ID INTEGER PRIMARY KEY AUTOINCREMENT, NAME TEXT NOT NULL UNIQUE)',
    # 画师标签关联表
    'CREATE TABLE PAINTER_TAG_RELATION (PAINTER_ID INT NOT NULL, TAG_ID INT NOT NULL)',
    # 图片标签关联表
    'CREATE TABLE PICTURE_TAG_RELATION (PICTURE_ID INT NOT NULL, TAG_ID INT NOT NULL)',
    # 画师联系方式表
    'CREATE TABLE CONTACTS ( PAINTER_ID INT PRIMARY KEY NOT NULL, Twitter TEXT, Instagram TEXT, Tumblr TEXT, '
    'Facebook TEXT, Skype TEXT, "Windows Live" TEXT, "Google Talk" TEXT, "Yahoo! Messenger" TEXT, Circlems TEXT)',
    # 画师英文个人信息表
    'CREATE TABLE EN_PERSONAL_INFO (ID INT PRIMARY KEY NOT NULL, Gender TEXT, Location TEXT, '
    'Age TEXT, Birthday TEXT, Occupation TEXT)',
    # 画师中文个人信息表
    'CREATE TABLE ZH_PERSONAL_INFO (ID INT PRIMARY KEY NOT NULL, Gender TEXT, Location TEXT, '
    'Age TEXT, Birthday TEXT, Occupation TEXT)',
    'CREATE TABLE PICTURE_INFO (ID INT PRIMARY KEY NOT NULL, '
    'Title TEXT, Introduction TEXT, Bookmark INT)',
    # ...想加入用户表，然后加入mark关系和follow关系，绝望
    # 'CREATE TABLE USER (ID INT PRIMARY KEY NOT NULL, )'
)


def pre_connect(func):
    @wraps(func)
    def inner(*args, **kwargs):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        try:
            result = func(c, conn, *args, **kwargs)
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
        cursor.execute("INSERT INTO PICTURE (ID, PID, P, DATE, TYPE) VALUES (?, ?, ?, ?, ?)", args)
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
def update_picture_base_info(cursor, connect, picture_id, painter_id):
    try:
        cursor.execute('UPDATE PICTURE SET PID = {} WHERE ID = {}'.format(painter_id, picture_id))
    except sqlite3.Error:
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


@pre_connect
def insert_picture_info_from_picture_detail_page(cursor, connect, *args):
    try:
        cursor.execute('INSERT INTO PICTURE_INFO (ID, Title, Introduction, Bookmark) VALUES (?, ?, ?, ?)', args)
    except sqlite3.IntegrityError as e:
        print(e)
        # we should use UPDATE statement.
    except sqlite3.Error:
        raise
    else:
        connect.commit()


@pre_connect
def insert_painter_info(cursor, connect, *args, **kwargs):
    try:
        print(kwargs)
        cursor.execute('INSERT INTO PAINTER (ID, Nickname, Website, "Self introduction") VALUES (?, ?, ?, ?)',
                       (kwargs.get('ID'), kwargs.get('Nickname'), kwargs.get('Website'),
                        kwargs.get('Self introduction')))
        cursor.execute(
            'INSERT INTO EN_PERSONAL_INFO (ID, Gender, Location, Age, Birthday, Occupation) VALUES (?, ?, ?, ?, ?, ?)',
            (kwargs.get('ID'), kwargs.get('Gender'), kwargs.get('Location'), kwargs.get('Age'), kwargs.get('Birthday'),
             kwargs.get('Occupation'))
        )
        cursor.execute(
            'INSERT INTO CONTACTS (PAINTER_ID, Twitter, Instagram, Tumblr, Facebook, Skype, "Windows Live",'
            '"Google Talk", "Yahoo! Messenger", Circlems) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (kwargs.get('ID'), kwargs.get('Twitter'), kwargs.get('Instagram'), kwargs.get('Tumblr'),
             kwargs.get('Facebook'), kwargs.get('Skype'), kwargs.get('Windows Live'), kwargs.get('Google Talk'),
             kwargs.get('Yahoo! Messenger'), kwargs.get('Circlems'))
        )
    except sqlite3.IntegrityError as e:
        print(e)
    except sqlite3.Error:
        raise
    else:
        connect.commit()  # the function should be to close the cursor.


@pre_connect
def search_painter_info(cursor, connect, *args, painter_id):
    try:
        cursor.execute('SELECT * FROM PAINTER INNER JOIN EN_PERSONAL_INFO ON PAINTER.ID = EN_PERSONAL_INFO.ID '
                       'INNER JOIN CONTACTS ON PAINTER.ID = CONTACTS.PAINTER_ID WHERE PAINTER.ID = {}'.format(
            painter_id))
    except sqlite3.Error:
        raise
    else:
        painter_info = cursor.fetchone()
        connect.commit()
        return painter_info


@pre_connect
def delete_picture_base_info(cursor, connect, picture_id):
    try:
        cursor.execute('DELETE FROM PICTURE WHERE ID = {}'.format(picture_id))
    except sqlite3.Error:
        raise
    else:
        connect.commit()


if __name__ == '__main__':
    # picture_base_info = search_picture_base_info(60778836)
    # picture_info = search_picture_info(60778836)
    # print(picture_base_info, picture_info)
    # delete_picture_base_info(picture_id=67313183)
    pass

