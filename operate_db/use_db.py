import sqlite3
from setting import db_path

conn = sqlite3.connect(db_path, check_same_thread=False)


def insert_picture_data(connection, id, p, date, file_type, pid=None):
    c = connection.cursor()
    try:
        c.execute("INSERT INTO PICTURE (ID, P, PID, DATE, TYPE) VALUES (?, ?, ?, ?, ?)", (id, p, pid, date, file_type))
    except sqlite3.OperationalError:
        print('这里应该有一系列的操作......')
    connection.commit()


def find_all_picture_id(connection):
    c = connection.cursor()
    return set((__ for _ in c.execute("SELECT ID FROM PICTURE") for __ in _))


# c = conn.cursor()
# for x in c.execute("SELECT * FROM PICTURE"):
#     print(x)
# print(find_all_picture_id(connection=conn))








# def _test(connection):
#     import random
#     for temp in range(20):
#         insert_picture_data(connection, random.randint(0, 100000), random.random(), random.random())
#     print(find_all_picture_id(connection))
#     c = connection.cursor()
#     c.execute("DELETE FROM PICTURE")
#     connection.commit()


# _test(conn)
# print(find_all_picture_id(connection=conn))
# c = conn.cursor()
# for x in c.execute("SELECT * FROM PICTURE"):
#     print(x)
