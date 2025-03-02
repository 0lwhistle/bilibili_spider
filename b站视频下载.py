import My_Own_Python_Package.Video_spider_package
import tkinter as tk
from pyperclip import paste

def get_video_info():
    url = my_entry.get()
    save_path = path_entry.get() or None
    My_Own_Python_Package.Video_spider_package.video_spider(url=url, retain=False, root_path=save_path)

def reset_entry():
    my_entry.delete(0, "end")
    path_entry.delete(0, "end")

def update_clipboard():
    global last_clipboard_content
    current_clipboard_content = paste()
    if current_clipboard_content != last_clipboard_content:
        reset_entry()
        my_entry.insert(tk.END, current_clipboard_content)
        last_clipboard_content = current_clipboard_content
        is_topmost = root.attributes('-topmost')
        root.attributes('-topmost', not is_topmost)

    root.after(1000, update_clipboard)

root = tk.Tk()
root.geometry("300x150")
root.title("视频获取")

tk.Label(root, text="请输入b站视频网址:").pack()
my_entry = tk.Entry(root)
my_entry.pack(side="top", pady=0)

tk.Label(root, text="请输入视频保存路径(不输入则默认保存到桌面):").pack()
path_entry = tk.Entry(root)
path_entry.pack()

tk.Button(root, text="获取视频", command=get_video_info).pack(side=tk.RIGHT, pady=0, padx=40)
tk.Button(root, text="清空输入", command=reset_entry).pack(side=tk.LEFT, pady=0, padx=40)

last_clipboard_content = None
update_clipboard()

root.mainloop()
