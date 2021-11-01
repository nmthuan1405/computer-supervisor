import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askokcancel, showerror, showinfo
from turtle import st
import ui.label as lb
import queue

class UI_runningApps(tk.Toplevel):
    def __init__(self, parent):
        self.ui_queue = queue.Queue()
        self.socket_queue = None

        super().__init__(parent)
        self.title = lb.APP_TITLE
        self.resizable(False, False)
        self['padx'] = 10
        self['pady'] = 10

        self.btn_start = tk.Button(self, text = lb.APP_START, width = 15, height = 2, command = self.start)
        self.btn_start.grid(row = 0, column = 0)

        self.btn_kill = tk.Button(self, text = lb.APP_KILL, width = 15, height = 2, command = self.kill)
        self.btn_kill.grid(row = 0, column = 1)

        # columns
        columns = ('#1', '#2', '#3')
        self.trv_apps = ttk.Treeview(self, columns = columns, show = 'headings', height = 20)

        #config column width
        self.trv_apps.column("#1", minwidth = 50, width = 200)
        self.trv_apps.column("#2", minwidth = 50, width = 100)
        self.trv_apps.column("#3", minwidth = 50, width = 100)

        # define headings
        self.trv_apps.heading('#1', text=lb.APP_NAME)
        self.trv_apps.heading('#2', text=lb.APP_ID)
        self.trv_apps.heading('#3', text=lb.APP_THREAD_COUNT)

        self.trv_apps.grid(row = 1, column = 0, pady = (10,0), columnspan = 2, sticky='nsew')

        # add a scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient = tk.VERTICAL, command = self.trv_apps.yview)
        self.trv_apps.configure(yscroll = self.scrollbar.set)
        self.scrollbar.grid(row = 1, column = 2, padx = 0, pady = (10,0), sticky = 'ns')

        # add data
        # self.insert()

        self.after(200, self.periodic_call)

    def insert(self, data):
        try:
            for line in data:
                self.trv_apps.insert('', tk.END, values = line)
        except:
            print('Error: Unable to get process list')
            self.clear()

    def clear(self):
        for row in self.trv_apps.get_children():
            self.trv_apps.delete(row)

    def start(self):
        window = UI_startAvailApp(self)
        window.grab_set()
        window.focus()

    def kill(self):
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

class UI_startAvailApp(tk.Toplevel):
    def __init__(self, parent):
        self.ui_queue = queue.Queue()
        self.socket_queue = None

        super().__init__(parent)
        self.title = lb.START_APP_TITLE
        self.resizable(False, False)
        self['padx'] = 10
        self['pady'] = 10

        self.lbl_avail_apps = tk.Label(self, text = lb.START_APP_AVAIL_APPS)
        self.lbl_avail_apps.grid(row = 0, column = 0, sticky = tk.W)

        # columns
        columns = ('#1', '#2')
        self.trv_apps = ttk.Treeview(self, columns = columns, show = 'headings', height = 15)

        #config column width
        self.trv_apps.column("#1", minwidth = 50, width = 50)
        self.trv_apps.column("#2", minwidth = 50, width = 300)

        # define headings
        self.trv_apps.heading('#1', text=lb.APP_ICON)
        self.trv_apps.heading('#2', text=lb.APP_NAME)

        self.trv_apps.grid(row = 1, column = 0, pady = (5,0), columnspan = 2, sticky='nsew')

        # add a scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient = tk.VERTICAL, command = self.trv_apps.yview)
        self.trv_apps.configure(yscroll = self.scrollbar.set)
        self.scrollbar.grid(row = 1, column = 2, padx = 0, pady = (10,0), sticky = 'ns')

        # add data
        # self.insert()

        self.btn_start = tk.Button(self, text=lb.START_APP_START, width = 15, height = 2, command = self.startApp)
        self.btn_start.grid(row = 2, column = 0, columnspan = 2, pady = (10,0))

        self.btn_custom = tk.Button(self, text=lb.START_APP_CUSTOM, width = 8, command = self.customApp)
        self.btn_custom.grid(row = 2, column = 0, sticky = tk.W, pady = (10,0))

        self.after(200, self.periodic_call)

    def startApp(self):
        # if (self.services.sendStartProcess(self.txt_name_input.get()) == 'OK'):
        #     showinfo("Sucess", "Start application successful!", parent = self)
        # else:
            showerror("Error", "Unable to start this application", parent = self)

    def customApp(self):
        window = UI_startCustomApp(self)
        window.grab_set()
        window.focus()

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

class UI_startCustomApp(tk.Toplevel):
    def __init__(self, parent):
        self.ui_queue = queue.Queue()
        self.socket_queue = None

        super().__init__(parent)
        self.title = lb.START_APP_TITLE
        self.resizable(False, False)
        self['padx'] = 10
        self['pady'] = 10

        self.lbl_app_name = tk.Label(self, text = lb.START_APP_NAME)
        self.lbl_app_name.grid(column = 0, row = 0)

        self.txt_name_input = tk.Entry(self)
        self.txt_name_input.focus()
        self.txt_name_input.grid(column = 1, row = 0, padx = 10)

        self.btn_start = tk.Button(self, text=lb.START_APP_START, command = self.startApp)
        self.btn_start.grid(column=2, row=0, sticky = tk.W, padx = 0, pady = 0, ipadx = 10)

        self.after(200, self.periodic_call)

    def startApp(self):
        # if (self.services.sendStartProcess(self.txt_name_input.get()) == 'OK'):
        #     showinfo("Sucess", "Start application successful!", parent = self)
        # else:
            showerror("Error", "Unable to start this application", parent = self)

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