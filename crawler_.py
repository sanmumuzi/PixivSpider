import sqlite3

conn = sqlite3.connect('example.db')
c = conn.cursor()

# Do this instead
# t = ('RHAT',)
# c.execute('SELECT * FROM stocks WHERE symbol=? and xxx=xxx', t)

# c.execute(
#     '''CREATE TABLE PAINTER
#     (ID INT PRIMARY KEY NOT NULL,
#     NAME TEXT           NOT NULL
#     );'''
# )

# c.execute(
#     '''CREATE TABLE PICTURE
#     (ID INT PRIMARY KEY NOT NULL,
#     DATE TEXT           NOT NULL,
#     TYPE TEXT           NOT NULL
#     );'''
# )

# id = 123
# name = 'name++++'
# c.execute("INSERT INTO PAINTER VALUES (?,?)", (id, name))
#
# conn.commit()
# conn.close()


# c.execute("DELETE FROM PAINTER WHERE ID=?", (123,))
#
# conn.commit()
# conn.close()

from setting import dir_list, img_list
import os

# print(dir_list)
# print(img_list)
# for x in img_list:
#     temp_list = os.path.basename(x).replace('_p0', '').split('.')
#     c.execute("INSERT INTO PICTURE (ID, DATE, TYPE) VALUES (?, ?, ?)", (temp_list[0], 'xxx', temp_list[1]))


# print(os.path.basename(x).split('.'))

for x in c.execute("SELECT * FROM PICTURE"):
    print(x)

for y in dir_list:
    print(os.path.basename(y))
    c.execute("INSERT INTO PAINTER (ID, NAME) VALUES (?, ?)", ())

conn.commit()
conn.close()
