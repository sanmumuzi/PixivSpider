from GUI.var import *


content.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.W, tk.E))
frame.grid(column=0, row=0, columnspan=30, rowspan=60, sticky=(tk.N, tk.S, tk.W, tk.E))
img_lbox.grid(column=0, row=0, columnspan=10, rowspan=60, sticky=(tk.N, tk.S, tk.W, tk.E))
list_frame.grid(column=0, row=0, columnspan=10, rowspan=60, sticky=(tk.N, tk.S, tk.W, tk.E))
logo_lbl.grid(column=10, row=0, columnspan=20, rowspan=60, sticky=(tk.N, tk.S, tk.W, tk.E))
option_frame.grid(column=30, row=0, columnspan=10, rowspan=60, sticky=(tk.N, tk.S, tk.W, tk.E))


idlbl.grid(columnspan=20, rowspan=5, sticky=(tk.N,), padx=5)
id.grid(columnspan=20, rowspan=5, sticky=(tk.N, tk.E, tk.W), padx=5)

usernamelbl.grid(columnspan=20, rowspan=5, sticky=(tk.N,), padx=5)
username.grid(columnspan=20, rowspan=5, sticky=(tk.N, tk.E, tk.W), padx=5)
passwordlbl.grid(columnspan=20, rowspan=5, sticky=(tk.N,), padx=5)
password.grid(columnspan=20, rowspan=5, sticky=(tk.N, tk.E, tk.W), padx=5)

status_lbl.grid(columnspan=20, rowspan=5, sticky=(tk.W, tk.S), padx=5)
work_message_frame.grid(column=0, row=35, columnspan=20, rowspan=10, sticky=(tk.W, tk.E))
work_message_bar.grid(sticky=(tk.N, tk.W))


ok_button.grid(column=0, row=45, columnspan=10, rowspan=5, sticky=(tk.W, tk.E))
quit_button.grid(column=10, row=45, columnspan=10, rowspan=5, sticky=(tk.W, tk.E))

pic_idlbl.grid(columnspan=20, rowspan=5, sticky=(tk.N,), padx=5)
pic_id.grid(columnspan=20, rowspan=5, sticky=(tk.N, tk.W, tk.E), padx=5)
get_an_work_button.grid(columnspan=20, rowspan=5, sticky=(tk.W, tk.E))

painter_info_frame.grid(column=0, row=65, columnspan=20, rowspan=10, sticky=(tk.W, tk.E))
painter_info_widget.grid(sticky=(tk.N, tk.W))

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)  # good !!!
content.rowconfigure(0, weight=1)
content.columnconfigure(0, weight=1)

# content.rowconfigure(10, weight=1)
# # content.rowconfigure(2, weight=1)
# # content.rowconfigure(3, weight=1)
# # content.rowconfigure(4, weight=1)
# content.rowconfigure(50, weight=1)
# content.columnconfigure(0, weight=5)
# content.columnconfigure(10, weight=5)
# content.columnconfigure(20, weight=5)  # weight 是不是指拉伸时候的比重
# content.columnconfigure(30, weight=1)
# content.columnconfigure(40, weight=1)

frame.columnconfigure(0, minsize=200, weight=1)
frame.rowconfigure(0, weight=1)
list_frame.columnconfigure(0, weight=1)  # 不写这个，listbox 扩不出来
list_frame.rowconfigure(0, weight=1)
work_message_frame.rowconfigure(0, weight=1, minsize=200)
work_message_frame.columnconfigure(0, weight=1)
painter_info_frame.rowconfigure(0, weight=1, minsize=200)
painter_info_frame.columnconfigure(0, weight=1)

if __name__ == '__main__':
    # root.mainloop()
    print(img_list)
    # print(temp_list)

# 动态图片大小
# 框体固定大小, 分几种情况
# 参数优化, 有的参数没啥意思...width , height的...
