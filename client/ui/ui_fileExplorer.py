import tkinter as tk
from tkinter import ttk

import ui.label as lb
import ui.constraints as const
import queue

class UI_fileExplorer(tk.Toplevel):
    def __init__(self, parent):
        self.ui_queue = queue.Queue()
        self.socket_queue = None

        super().__init__(parent)
        self.title = lb.FILE_EXPLORER_TITLE
        self.resizable(False, False)
        self['padx'] = const.WINDOW_BORDER_PADDING
        self['pady'] = const.WINDOW_BORDER_PADDING

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=30)

        self.btn_up = tk.Button(self, text = lb.FILE_EXP_UP, width = 10, command = self.upFolder)
        self.btn_up.grid(row = 0, column = 0, pady = (0,5), sticky = tk.W)

        self.txt_path_input = tk.Entry(self)
        self.txt_path_input.grid(row = 0, column = 1, pady = (0,5), sticky = tk.EW)

        # create a treeview
        columns = ('#1', '#2', '#3', '#4')
        self.trv_fileExp = ttk.Treeview(self, columns = columns, show = 'headings', height = 20)

        # config columns width
        self.trv_fileExp.column('#1',minwidth = 50, width = 300, anchor = tk.W)
        self.trv_fileExp.column('#2',minwidth = 50, width = 200, anchor = tk.W)
        self.trv_fileExp.column('#3',minwidth = 50, width = 200, anchor = tk.W)
        self.trv_fileExp.column('#4',minwidth = 50, width = 100, anchor = tk.E)

        # define headings
        self.trv_fileExp.heading('#1', text = lb.FILE_EXP_TRV_NAME)
        self.trv_fileExp.heading('#2', text = lb.FILE_EXP_TRV_DATEMOD)
        self.trv_fileExp.heading('#3', text = lb.FILE_EXP_TRV_TYPE)
        self.trv_fileExp.heading('#4', text = lb.FILE_EXP_TRV_SIZE)

        self.trv_fileExp.grid(row = 1, column = 0, rowspan = 10, columnspan = 2, sticky = tk.NSEW)

        # add a scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient = tk.VERTICAL, command = self.trv_fileExp.yview)
        self.trv_fileExp.configure(yscroll = self.scrollbar.set)
        self.scrollbar.grid(row = 1, column = 2, rowspan = 10, sticky = 'ns')

        # adding data
        self.trv_fileExp.insert('', tk.END, values = ('Folder 1','1/1/2020 1:30 AM','File folder',''))
        self.trv_fileExp.insert('', tk.END, values = ('Folder 2','1/1/2020 1:30 AM','File folder',''))
        self.trv_fileExp.insert('', tk.END, values = ('Folder 3','1/1/2020 1:30 AM','File folder',''))
        self.trv_fileExp.insert('', tk.END, values = ('file1.txt','1/1/2020 1:30 AM','Text Document','400 B'))
        self.trv_fileExp.insert('', tk.END, values = ('file1.docx','1/1/2020 1:30 AM','Microsoft Word Document','10 KB'))
        self.trv_fileExp.insert('', tk.END, values = ('file3.pdf','1/1/2020 1:30 AM','Foxit Reader PDF Document','20340 KB'))

        self.btn_copy = tk.Button(self, text = lb.FILE_EXP_COPY, width = 10, height = 6, command = self.copyFile)
        self.btn_copy.grid(row = 1, column = 3, padx = (10,0))

        self.btn_delete = tk.Button(self, text = lb.FILE_EXP_DELETE, width = 10, height = 6, command = self.deleteFile)
        self.btn_delete.grid(row = 2, column = 3, padx = (10,0))

        self.after(const.UPDATE_TIME, self.periodic_call)

    def upFolder(self):
        return

    def copyFile(self):
        return

    def deleteFile(self):
        return

    def update_ui(self, task):
        DEBUG("task", task)
        cmd, ext = task

    def periodic_call(self):
        while True:
            try:
                task = self.ui_queue.get_nowait()
                self.update_ui(task)
                
            except queue.Empty:
                break
        
        self.after(const.UPDATE_TIME, self.periodic_call)

    def add_socket_queue(self, socket_queue):
        self.socket_queue = socket_queue
    
    def socket_cmd(self, cmd, ext = None):
        self.socket_queue.put((cmd, ext))

def DEBUG(*args,**kwargs):
    print("UI:", *args,**kwargs)