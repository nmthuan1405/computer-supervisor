import tkinter as tk
from tkinter import ttk

import ui.label as lb
import queue

class UI_fileExplorer(tk.Toplevel):
    def __init__(self, parent):
        self.ui_queue = queue.Queue()
        self.socket_queue = None

        super().__init__(parent)
        self.title = lb.FILE_EXPLORER_TITLE
        self.resizable(False, False)
        self['padx'] = 10
        self['pady'] = 10

        # create a treeview
        columns = ('#1', '#2', '#3')
        self.trv_fileExp = ttk.Treeview(self, columns = columns, height = 30)
        # config columns width
        self.trv_fileExp.column('#0',minwidth = 50, width = 400, anchor = tk.W)
        self.trv_fileExp.column('#1',minwidth = 50, width = 200, anchor = tk.W)
        self.trv_fileExp.column('#2',minwidth = 50, width = 200, anchor = tk.W)
        self.trv_fileExp.column('#3',minwidth = 50, width = 100, anchor = tk.E)

        # define headings
        self.trv_fileExp.heading('#0', text = lb.FILE_EXP_TRV_NAME)
        self.trv_fileExp.heading('#1', text = lb.FILE_EXP_TRV_DATEMOD)
        self.trv_fileExp.heading('#2', text = lb.FILE_EXP_TRV_TYPE)
        self.trv_fileExp.heading('#3', text = lb.FILE_EXP_TRV_SIZE)

        self.trv_fileExp.grid(row = 0, column = 0, rowspan = 10, sticky = tk.NSEW)

        # add a scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient = tk.VERTICAL, command = self.trv_fileExp.yview)
        self.trv_fileExp.configure(yscroll = self.scrollbar.set)
        self.scrollbar.grid(row = 0, column = 1, rowspan = 10, sticky = 'ns')

        # adding data
        self.trv_fileExp.insert('', tk.END, text = "Folder 1", values = ('1/1/2020 1:30 AM','File folder',), iid = 0, open = True)
        self.trv_fileExp.insert('', tk.END, text = "Folder 2", values = ('1/1/2020 1:30 AM','File folder',''), iid = 1, open = False)
        # adding children
        self.trv_fileExp.insert('', tk.END, text = "Folder 3", values = ('1/1/2020 1:30 AM','File folder',''), iid = 2, open = False)
        self.trv_fileExp.move(2, 0, 0)
        self.trv_fileExp.insert('', tk.END, text = "file1.txt", values = ('1/1/2020 1:30 AM','Text Document','400 B'), iid = 3, open = False)
        self.trv_fileExp.move(3, 2, 0)
        self.trv_fileExp.insert('', tk.END, text = "file2.docx", values = ('1/1/2020 1:30 AM','Microsoft Word Document','10 KB'), iid = 4, open = False)
        self.trv_fileExp.move(4, 0, 1)
        self.trv_fileExp.insert('', tk.END, text = "file3.pdf", values = ('1/1/2020 1:30 AM','Foxit Reader PDF Document','20340 KB'), iid = 5, open = False)
        self.trv_fileExp.move(5, 1, 0)

        self.btn_copy = tk.Button(self, text = lb.FILE_EXP_COPY, width = 10, height = 6, command = self.copyFile)
        self.btn_copy.grid(row = 0, column = 2, padx = (10,0))

        self.btn_delete = tk.Button(self, text = lb.FILE_EXP_DELETE, width = 10, height = 6, command = self.deleteFile)
        self.btn_delete.grid(row = 1, column = 2, padx = (10,0))

        self.after(200, self.periodic_call)

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
        
        self.after(200, self.periodic_call)

    def add_socket_queue(self, socket_queue):
        self.socket_queue = socket_queue
    
    def socket_cmd(self, cmd, ext = None):
        self.socket_queue.put((cmd, ext))

def DEBUG(*args,**kwargs):
    print("UI:", *args,**kwargs)