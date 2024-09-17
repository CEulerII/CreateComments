import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from pathlib import Path
import os
import sys
import threading
import queue
import ctypes
from tkinter import messagebox
import subprocess  # 用于替换os.system，避免控制台窗口闪烁

class CreateComments(TkinterDnD.Tk):
    def __init__(self) -> None:
        super().__init__()
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
        self.notify_queue  = queue.Queue()
        self.title('File Comments Modifier')
        self.attributes('-topmost', 1)
        self.attributes('-toolwindow', 0)
        self.attributes("-fullscreen", False)
        self.overrideredirect(False)
        self.state('normal')
        self.attributes("-alpha",1)
        self.resizable(0,0)
        self.window_width        = 500
        self.window_height       = 300
        self.screen_width        = self.winfo_screenwidth()
        self.screen_height       = self.winfo_screenheight()
        self.position_horizontal = (self.screen_width  - self.window_width )//2
        self.position_vertical   = (self.screen_height - self.window_height)//2
        self.geometry('{}x{}+{}+{}'.format(self.window_width, self.window_height, self.position_horizontal, self.position_vertical))
        self.config(background = 'white',highlightbackground = 'white',highlightcolor = 'white',highlightthickness = 0)
        self.title_label =  tk.Label(self,text='File Comments Modifier',
                                     font=('Cooper Black',20),fg='green',width=30,height=1,background = 'white')
        self.title_label.place(x=-25,y=20)
        self.DropFileLabel = tk.Label(self,text = 'Drag a File Here:',background = 'white',font=('Cooper Black',15),justify="left")
        self.DropFileLabel.place(x=25,y=70)
        self.lb = tk.Listbox(self,height=1, width=40,background = 'lightgrey',borderwidth = 3 , relief = 'solid',font=('Microsoft YaHei',13))
         
        self.scrollbar = tk.Scrollbar(self,orient="horizontal")
        self.scrollbar.pack(side='bottom', fill='x')
        self.lb.config(xscrollcommand = self.scrollbar.set)
        self.scrollbar.config(command=self.lb.xview)
        self.lb.place(x=25,y=100)
        
        self.EnterCommentsLabel = tk.Label(self,text = 'Enter File Comments Here:',background = 'white',font=('Cooper Black',15))
        self.EnterCommentsLabel.place(x=25,y=165)
        self.file_comments = tk.StringVar()
        self.entry_comments = tk.Entry(self,textvariable = self.file_comments,
                                         font=('Microsoft YaHei',13), width=40,
                                         background = 'lightgrey', foreground = 'black', relief='solid',borderwidth = 3)
        self.entry_comments.place(x=25,y=195)
        
        self.btn_start = tk.Button(self,text='[ Add Comments ]',width=15,height=2,command = self.run_add_comments, background = 'white',font=('Cooper Black',10),relief = 'groove')
        self.btn_start.place(x=50,y=240)
        
        self.btn_exit = tk.Button(self,text='[ Exit ]',width=15,height=2,command = self.destroy, background = 'white',font=('Cooper Black',10),relief = 'groove')
        self.btn_exit.place(x=265,y=240)
        
        # register the listbox as a drop target
        self.lb.drop_target_register(DND_FILES)
        self.lb.dnd_bind('<<Drop>>',self.drop_inside_list_box)
        self.path_map = {}
        self.finalfilepath=""
    #__________________________________________________________________________      
    def drop_inside_list_box(self, event):
        file_paths = self._parse_drop_files(event.data)
        self.finalfilepath = file_paths
        current_listbox_items = set(self.lb.get(0,"end"))  #Prevents users from dragging the same file twice.
        for file_path in file_paths:
            if not os.path.isdir(file_path):
                messagebox.showerror(title='Warning', message='The Path You Entered is not a Folder!')
                self.lb.delete(0)
                current_listbox_items = set("")
                self.finalfilepath = ""
            else:
                path_object = Path(file_path)
                file_name = path_object.name
                if file_name not in current_listbox_items:
                    self.lb.delete(0)
                    self.lb.insert("end", file_name)
                    self.path_map[file_name] = file_path
        
    def _parse_drop_files(self, filename):
        size = len(filename)
        res = [] # list of file paths
        name = ""
        idx = 0
        while idx < size:
            if filename[idx] == "{":
                j = idx + 1
                while filename[j] != "}":
                    name += filename[j]
                    j += 1
                res.append(name)
                name = ""
                idx = j
            elif filename[idx] == " " and name != "":
                res.append(name)
                name = ""
            elif filename[idx] != " ":
                name += filename[idx]
            idx += 1
          
        if name != "" :
            res.append(name)
        return res   
    
    def run_add_comments(self):
        th = threading.Thread(target=self.action_add_comments,args=(self.notify_queue,),daemon=True)
        th.start()

    def action_add_comments(self, _queue):
        defEncoding = sys.getfilesystemencoding()

        def sys_encode(content):
            return content.encode(defEncoding).decode(defEncoding)

        def run_command(command):
            # 使用subprocess.run代替os.system，并避免控制台窗口出现
            subprocess.run(command, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)

        def get_setting_file_path(fpath):
            return fpath + os.sep + 'desktop.ini'

        def update_folder_comment(fpath, comment):
            content = sys_encode(u'[.ShellClassInfo]' + os.linesep + 'InfoTip=')
            setting_file_path = get_setting_file_path(fpath)
            with open(setting_file_path, 'w') as f:
                f.write(content)
                f.write(sys_encode(comment + os.linesep))
            run_command(f'attrib "{setting_file_path}" +s +h')
            run_command(f'attrib "{fpath}" +s')

        def add_comment(fpath=None, comment=None):
            # 检查是否有拖入的文件夹
            if not self.finalfilepath or not self.lb.size():
                messagebox.showerror(title='Warning', message='Please Input a Folder Path!')
                return  # 没有拖入文件时，直接返回，避免报错

            fpath = self.finalfilepath[0]
            setting_file_path = get_setting_file_path(fpath)
            if os.path.exists(setting_file_path):
                run_command(f'attrib "{setting_file_path}" -s -h')
            comment = self.file_comments.get()
            update_folder_comment(fpath, comment)

        add_comment()
        self.lb.delete(0)  # 清空 Listbox 中的内容
        self.finalfilepath = ""  # 重置路径，防止多次点击错误
        _queue.put((1,))

if __name__ == "__main__":
    app = CreateComments()
    app.mainloop()
