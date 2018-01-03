import threading
import tkinter as tk
import os
from PIL import Image, ImageTk

from new_crawl import Pixiv

img_file_path = 'artist_work'
dir_list = [os.path.abspath(os.path.join(img_file_path, relative_path)) for relative_path in os.listdir(img_file_path)]
img_list = [os.path.join(dir_name, img)
            for dir_name in dir_list for img in os.listdir(dir_name) if img.endswith(('.png', '.jpg'))]


def get_info():
    def get_img(usr, passwd, status, pter_id):
        demo = Pixiv()
        if demo.login(usr, passwd):
            demo.get_work_of_painter(pter_id)
            status.set('Success...')
        else:
            status.set('Error...')

    thread_item = threading.Thread(target=get_img,
                                   args=(username_var.get(), passwd_var.get(), status_var, painterid_var.get()))
    thread_item.setDaemon(True)
    thread_item.start()
    # get_img(username_var.get(), passwd_var.get(), status_var, pter_id=painterid_var.get())


def resize_img(file_name, width, height):
    img = Image.open(file_name)
    (x, y) = img.size
    temp_x = x / width  # 放大倍数
    temp_y = y / height
    if temp_x > temp_y:
        return img.resize((width, int(y / temp_x)), Image.ANTIALIAS)
    else:
        return img.resize((int(x / temp_y), height), Image.ANTIALIAS)


root = tk.Tk()

painterid_var = tk.StringVar()
username_var = tk.StringVar()
passwd_var = tk.StringVar()
status_var = tk.StringVar()
img_var = tk.StringVar(value=img_list)
# painterid_var.set('')
# username_var.set('')
# passwd_var.set('')

root.title('Pixiv_spider')
content = tk.Frame(root, padx=3, pady=3)
frame = tk.Frame(content, borderwidth=5, relief='sunken', width=200, height=100)
img_lbox = tk.Listbox(frame, listvariable=img_var, height=10)
logo = ImageTk.PhotoImage(resize_img(file_name=img_list[36], width=600, height=800))
logo_lbl = tk.Label(frame, image=logo)

idlbl = tk.Label(content, text='painter_id')
id = tk.Entry(content, textvariable=painterid_var)
usernamelbl = tk.Label(content, text='pixiv username')
username = tk.Entry(content, textvariable=username_var)
passwordlbl = tk.Label(content, text='password')
password = tk.Entry(content, textvariable=passwd_var, show='*')

status_lbl = tk.Label(content, textvariable=status_var)

ok_button = tk.Button(content, text='Okay', command=get_info)
quit_button = tk.Button(content, text='quit!', command=root.destroy)

content.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.W, tk.E))
frame.grid(column=0, row=0, columnspan=3, rowspan=6, sticky=(tk.N, tk.S, tk.W, tk.E))
img_lbox.grid(column=0, row=0, columnspan=1, rowspan=6, sticky=(tk.N, tk.S, tk.W, tk.E))
logo_lbl.grid(column=1, row=0, columnspan=2, rowspan=6, sticky=(tk.N, tk.S, tk.W, tk.E))

idlbl.grid(column=3, row=0, columnspan=2, sticky=(tk.N,), padx=5)
id.grid(column=3, row=1, columnspan=2, sticky=(tk.N, tk.E, tk.W), padx=5)
usernamelbl.grid(column=3, row=2, columnspan=2, sticky=(tk.N,), padx=5)
username.grid(column=3, row=3, columnspan=2, sticky=(tk.N, tk.E, tk.W), padx=5)
passwordlbl.grid(column=3, row=4, columnspan=2, sticky=(tk.N,), padx=5)
password.grid(column=3, row=5, columnspan=2, sticky=(tk.N, tk.E, tk.W), padx=5)
status_lbl.grid(column=0, row=6, sticky=(tk.W, tk.S), padx=5)
ok_button.grid(column=3, row=6, sticky=(tk.W, tk.E))
quit_button.grid(column=4, row=6, sticky=(tk.W, tk.E))

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)  # good !!!
# content.rowconfigure(0, weight=1)
content.rowconfigure(1, weight=1)
# content.rowconfigure(2, weight=1)
content.rowconfigure(3, weight=1)
# content.rowconfigure(4, weight=1)
content.rowconfigure(5, weight=1)
content.columnconfigure(0, weight=3)
content.columnconfigure(1, weight=3)
content.columnconfigure(2, weight=3)
content.columnconfigure(3, weight=1)
content.columnconfigure(4, weight=1)
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)
frame.rowconfigure(1, weight=1)

if __name__ == '__main__':
    root.mainloop()


# 动态图片大小
# 框体固定大小, 分几种情况
# 参数优化, 有的参数没啥意思...width , height的...
