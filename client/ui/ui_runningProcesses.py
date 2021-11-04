import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askokcancel, showerror, showinfo

import ui.label as lb
import ui.constraints as const
import queue

class UI_runningProcesses(tk.Toplevel):
    def __init__(self, parent, socket_queue):
        self.ui_queue = queue.Queue()
        self.socket_queue = socket_queue

        super().__init__(parent)
        self.title = lb.PROCESS_TITLE
        self.resizable(False, False)
        self['padx'] = const.WINDOW_BORDER_PADDING
        self['pady'] = const.WINDOW_BORDER_PADDING

        self.btn_start = tk.Button(self, text = lb.PROCESS_START, width = 15, height = 2, command = self.start)
        self.btn_start.grid(row = 0, column = 0, sticky = tk.EW)

        self.btn_kill = tk.Button(self, text = lb.PROCESS_KILL, width = 15, height = 2, command = self.kill)
        self.btn_kill.grid(row = 0, column = 1, sticky = tk.EW)

        # columns
        columns = ('#1', '#2', '#3')
        self.trv_processes = ttk.Treeview(self, columns = columns, show = 'headings', height = 20)

        #config column width
        self.trv_processes.column("#1", minwidth = 50, width = 200)
        self.trv_processes.column("#2", minwidth = 50, width = 100)
        self.trv_processes.column("#3", minwidth = 50, width = 100)

        # define headings
        self.trv_processes.heading('#1', text=lb.PROCESS_NAME)
        self.trv_processes.heading('#2', text=lb.PROCESS_ID)
        self.trv_processes.heading('#3', text=lb.PROCESS_THREAD_COUNT)

        self.trv_processes.grid(row = 1, column = 0, pady = (5,0), columnspan = 2, sticky='nsew')

        # add a scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient = tk.VERTICAL, command = self.trv_processes.yview)
        self.trv_processes.configure(yscroll = self.scrollbar.set)
        self.scrollbar.grid(row = 1, column = 2, padx = 0, pady = (5,0), sticky = 'ns')

        # add data
        # self.insert(self.services.getProcessList())

        self.after(const.UPDATE_TIME, self.periodic_call)

    def insert(self, data):
        try:
            for line in data:
                self.trv_processes.insert('', tk.END, values = line)
        except:
            print('Error: Unable to get process list')
            self.clear()

    def clear(self):
        for row in self.trv_processes.get_children():
            self.trv_processes.delete(row)

    def start(self):
        window = UI_startProcess(self)
        window.grab_set()
        window.focus()

    def kill(self):
        window = UI_killProcess(self)
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
        
        self.after(const.UPDATE_TIME, self.periodic_call)

    def add_socket_queue(self, socket_queue):
        self.socket_queue = socket_queue
    
    def socket_cmd(self, cmd, ext = None):
        self.socket_queue.put((cmd, ext))

class UI_startProcess(tk.Toplevel):
    def __init__(self, parent):
        self.ui_queue = queue.Queue()
        self.socket_queue = None

        super().__init__(parent)
        self.title = lb.START_PROCESS_TITLE
        self.resizable(False, False)
        self['padx'] = const.WINDOW_BORDER_PADDING
        self['pady'] = const.WINDOW_BORDER_PADDING

        self.lbl_process_name = tk.Label(self, text = lb.START_PROCESS_NAME)
        self.lbl_process_name.grid(column = 0, row = 0)

        self.txt_name_input = tk.Entry(self)
        self.txt_name_input.focus()
        self.txt_name_input.grid(column = 1, row = 0, padx = 10)

        self.btn_start = tk.Button(self, text=lb.START_PROCESS_START, command = self.startProcess)
        self.btn_start.grid(column=2, row=0, sticky = tk.W, padx = 0, pady = 0, ipadx = 10)

        self.after(const.UPDATE_TIME, self.periodic_call)

    def startProcess(self):
        # if (self.services.sendStartProcess(self.txt_name_input.get()) == 'OK'):
        #     showinfo("Sucess", "Start process successful!", parent = self)
        # else:
            showerror("Error", "Unable to start this process", parent = self)

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

class UI_killProcess(tk.Toplevel):
    def __init__(self, parent):
        self.ui_queue = queue.Queue()
        self.socket_queue = None

        super().__init__(parent)
        self.title = lb.KILL_PROCESS_TITLE
        self.resizable(False, False)
        self['padx'] = const.WINDOW_BORDER_PADDING
        self['pady'] = const.WINDOW_BORDER_PADDING

        self.lbl_process_id = tk.Label(self, text = lb.KILL_PROCESS_ID)
        self.lbl_process_id.grid(column = 0, row = 0)

        self.txt_id_input = tk.Entry(self)
        self.txt_id_input.focus()
        self.txt_id_input.grid(column = 1, row = 0, padx = 10)

        self.btn_kill = tk.Button(self, text=lb.KILL_PROCESS_KILL, command = self.killProcess)
        self.btn_kill.grid(column=2, row=0, sticky = tk.W, padx = 0, pady = 0, ipadx = 10)

        self.after(const.UPDATE_TIME, self.periodic_call)

    def killProcess(self):
        # if (self.services.sendKillProcess(self.txt_ID_input.get()) == 'OK'):
        #     showinfo("Sucess", "Kill process successful!", parent = self)
        # else:
            showerror("Error", "Unable to kill this process", parent = self)

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