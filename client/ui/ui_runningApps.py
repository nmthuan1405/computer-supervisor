import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askokcancel, showerror, showinfo
from services.count import Count
import ui.label as lb
import ui.constraints as const
import queue

class UI_runningApps(tk.Toplevel):
    def __init__(self, parent, socket_queue, ui_queues):
        self.ui_queue = queue.Queue()
        self.socket_queue = socket_queue
        self.ui_queues = ui_queues
        ui_queues['app'] = self.ui_queue

        super().__init__(parent)
        self.title = lb.APP_TITLE
        self.resizable(False, False)
        self['padx'] = const.WINDOW_BORDER_PADDING
        self['pady'] = const.WINDOW_BORDER_PADDING

        self.btn_start = tk.Button(self, text = lb.APP_START, width = 15, height = 2, command = self.start)
        self.btn_start.grid(row = 0, column = 0, sticky = tk.EW)

        self.btn_kill = tk.Button(self, text = lb.APP_KILL, width = 15, height = 2, command = self.kill)
        self.btn_kill.grid(row = 0, column = 1, sticky = tk.EW)

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

        self.trv_apps.grid(row = 1, column = 0, pady = (5,0), columnspan = 2, sticky='nsew')

        # add a scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient = tk.VERTICAL, command = self.trv_apps.yview)
        self.trv_apps.configure(yscroll = self.scrollbar.set)
        self.scrollbar.grid(row = 1, column = 2, padx = 0, pady = (5,0), sticky = 'ns')

        self.update_counting = Count(10, self.socket_cmd, 'get-running-app')
        self.update_counting.count_up(-1)
        self.after(const.UPDATE_TIME, self.periodic_call)

    def update(self, data):
        selected =  self.trv_apps.item(self.trv_apps.focus())['values']
        self.clear()
        for line in data:
            self.trv_apps.insert('', tk.END, values = line)
            
            if selected != '' and str(selected[1]) == str(line[1]):
                last_element = self.trv_apps.get_children()[-1]
                self.trv_apps.focus(last_element)
                self.trv_apps.selection_set(last_element)

    def clear(self):
        self.trv_apps.delete(*self.trv_apps.get_children())

    def start(self):
        window = UI_startAvailApp(self, self.socket_queue, self.ui_queues)
        
        window.grab_set()
        window.focus()

    def kill(self):
        selected = self.trv_apps.item(self.trv_apps.focus())['values']
        if selected == '':
            showinfo(lb.ERR, lb.APP_SELECT_APP, parent = self)
            return

        if askokcancel(lb.APP_KILL, lb.APP_KILL_CONFIRM, parent = self):
            self.socket_cmd('kill-process', (selected[1], 'app'))

    def update_ui(self, task):
        DEBUG("task", task)
        cmd, ext = task

        if cmd == 'update-running':
            self.update(ext)
        elif cmd == 'ok':
            showinfo(lb.APP_KILL, lb.APP_KILL_OK, parent = self)
        elif cmd == 'err':
            showerror(lb.APP_KILL, lb.APP_KILL_ERR, parent = self)

    def periodic_call(self):
        self.update_counting.count_up()

        while True:
            try:
                task = self.ui_queue.get_nowait()
                self.update_ui(task)
                
            except queue.Empty:
                break
        
        self.after(const.UPDATE_TIME, self.periodic_call)
    
    def socket_cmd(self, cmd, ext = None):
        self.socket_queue.put((cmd, ext))

class UI_startAvailApp(tk.Toplevel):
    def __init__(self, parent, socket_queue, ui_queues):
        self.ui_queue = queue.Queue()
        self.socket_queue = socket_queue
        self.ui_queues = ui_queues
        ui_queues['start-app'] = self.ui_queue

        super().__init__(parent)
        self.title = lb.START_APP_TITLE
        self.resizable(False, False)
        self['padx'] = const.WINDOW_BORDER_PADDING
        self['pady'] = const.WINDOW_BORDER_PADDING

        self.lbl_avail_apps = tk.Label(self, text = lb.START_APP_AVAIL_APPS)
        self.lbl_avail_apps.grid(row = 0, column = 0, sticky = tk.W)

        # columns
        columns = ('#1', '#2')
        self.trv_apps = ttk.Treeview(self, columns = columns, show = 'headings', height = 15)

        #config column width
        self.trv_apps.column("#1", minwidth = 50, width = 200)
        self.trv_apps.column("#2", minwidth = 50, width = 300)

        # define headings
        self.trv_apps.heading('#1', text=lb.APP_NAME)
        self.trv_apps.heading('#2', text=lb.APP_LOCATION)

        self.trv_apps.grid(row = 1, column = 0, pady = (5,0), sticky='nsew')

        # add a scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient = tk.VERTICAL, command = self.trv_apps.yview)
        self.trv_apps.configure(yscroll = self.scrollbar.set)
        self.scrollbar.grid(row = 1, column = 1, padx = 0, pady = (10,0), sticky = 'ns')

        self.frame = tk.Frame(self)
        self.btn_start = tk.Button(self.frame, text=lb.START_APP_START, width = 8, height = 2, command = self.startApp)
        self.btn_start.grid(row = 0, column = 0, padx = (0,5))

        self.btn_custom = tk.Button(self.frame, text=lb.START_APP_CUSTOM, width = 8, height = 2, command = self.customApp)
        self.btn_custom.grid(row = 0, column = 1)
        self.frame.grid(row = 2, column = 0, pady = (5,0), sticky= tk.E)

        self.socket_cmd('get-app-list')
        self.after(const.UPDATE_TIME, self.periodic_call)

    def startApp(self):
        selected = self.trv_apps.item(self.trv_apps.focus())['values']
        if selected == '':
            showinfo(lb.ERR, lb.START_APP_SELECT_APP, parent = self)
            return

        self.socket_cmd('start-process', (selected[1], 'start-app'))

    def customApp(self):
        window = UI_startCustomApp(self, self.socket_queue, self.ui_queues)
        window.grab_set()
        window.focus()

    def clear(self):
        self.trv_apps.delete(*self.trv_apps.get_children())

    def update(self, data):
        self.clear()
        for line in data:
            self.trv_apps.insert('', tk.END, values = line)

    def update_ui(self, task):
        DEBUG("task", task)
        cmd, ext = task

        if cmd == 'update-app':
            self.update(ext)
        elif cmd == 'ok':
            showinfo(lb.START_APP_START, lb.START_APP_START_OK, parent = self)
        elif cmd == 'err':
            showerror(lb.START_APP_START, lb.START_APP_START_ERR, parent = self)

    def periodic_call(self):
        while True:
            try:
                task = self.ui_queue.get_nowait()
                self.update_ui(task)
                
            except queue.Empty:
                break
        
        self.after(const.UPDATE_TIME, self.periodic_call)

    def socket_cmd(self, cmd, ext = None):
        self.socket_queue.put((cmd, ext))

class UI_startCustomApp(tk.Toplevel):
    def __init__(self, parent, socket_queue, ui_queues):
        self.ui_queue = queue.Queue()
        self.socket_queue = socket_queue
        ui_queues['start-custom-app'] = self.ui_queue

        super().__init__(parent)
        self.title = lb.START_APP_TITLE
        self.resizable(False, False)
        self['padx'] = const.WINDOW_BORDER_PADDING
        self['pady'] = const.WINDOW_BORDER_PADDING

        self.lbl_app_name = tk.Label(self, text = lb.START_APP_NAME)
        self.lbl_app_name.grid(column = 0, row = 0)

        self.txt_name_input = tk.Entry(self)
        self.txt_name_input.focus()
        self.txt_name_input.grid(column = 1, row = 0, padx = 10)

        self.btn_start = tk.Button(self, text=lb.START_APP_START, command = self.startApp)
        self.btn_start.grid(column=2, row=0, sticky = tk.W, padx = 0, pady = 0, ipadx = 10)

        self.after(const.UPDATE_TIME, self.periodic_call)

    def startApp(self):
        self.socket_cmd('start-process', (self.txt_name_input.get(), 'start-custom-app'))

    def update_ui(self, task):
        DEBUG("task", task)
        cmd, ext = task

        if cmd == 'ok':
            showinfo(lb.START_APP_START, lb.START_APP_START_OK, parent = self)
            self.destroy()
        elif cmd == 'err':
            showerror(lb.START_APP_START, lb.START_APP_START_ERR, parent = self)

    def periodic_call(self):
        while True:
            try:
                task = self.ui_queue.get_nowait()
                self.update_ui(task)
                
            except queue.Empty:
                break
        
        self.after(const.UPDATE_TIME, self.periodic_call)
    
    def socket_cmd(self, cmd, ext = None):
        self.socket_queue.put((cmd, ext))


def DEBUG(*args,**kwargs):
    print("UI:", *args,**kwargs)