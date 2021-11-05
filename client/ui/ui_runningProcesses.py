import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askokcancel, showerror, showinfo
from services.count import Count
import ui.label as lb
import ui.constraints as const
import queue

class UI_running_processes(tk.Toplevel):
    def __init__(self, parent, socket_queue, ui_queues):
        super().__init__(parent)
        self.ui_queue = queue.Queue()
        self.socket_queue = socket_queue
        self.ui_queues = ui_queues
        ui_queues['process'] = self.ui_queue

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

        self.update_counting = Count(10, self.socket_cmd, 'get-running-process')
        self.update_counting.count_up(-1)
        self.after(const.UPDATE_TIME, self.periodic_call)

    def update(self, data):
        selected =  self.trv_processes.item(self.trv_processes.focus())['values']
        self.clear()
        for line in data:
            self.trv_processes.insert('', tk.END, values = line)
            
            if selected != '' and str(selected[1]) == str(line[1]):
                last_element = self.trv_processes.get_children()[-1]
                self.trv_processes.focus(last_element)
                self.trv_processes.selection_set(last_element)

    def clear(self):
        self.trv_processes.delete(*self.trv_processes.get_children())

    def start(self):
        window = UI_start_process(self, self.socket_queue, self.ui_queues)
        window.grab_set()
        window.focus()

    def kill(self):
        selected = self.trv_processes.item(self.trv_processes.focus())['values']
        if selected == '':
            showinfo(lb.ERR, lb.PROCESS_SELECT_PROCESS, parent = self)
            return

        if askokcancel(lb.PROCESS_KILL, lb.PROCESS_KILL_CONFIRM, parent = self):
            self.socket_cmd('kill-process', (selected[1], 'process'))

    def update_ui(self, task):
        DEBUG("task", task)
        cmd, ext = task

        if cmd == 'update-running':
            self.update(ext)
        elif cmd == 'ok':
            showinfo(lb.PROCESS_KILL, lb.PROCESS_KILL_OK, parent = self)
        elif cmd == 'err':
            showerror(lb.PROCESS_KILL, lb.PROCESS_KILL_ERR, parent = self)

    def periodic_call(self):
        self.update_counting.count_up()

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

class UI_start_process(tk.Toplevel):
    def __init__(self, parent, socket_queue, ui_queues):
        super().__init__(parent)
        self.ui_queue = queue.Queue()
        self.socket_queue = socket_queue
        ui_queues['start-process'] = self.ui_queue

        self.title = lb.START_PROCESS_TITLE
        self.resizable(False, False)
        self['padx'] = const.WINDOW_BORDER_PADDING
        self['pady'] = const.WINDOW_BORDER_PADDING

        self.lbl_process_name = tk.Label(self, text = lb.START_PROCESS_NAME)
        self.lbl_process_name.grid(column = 0, row = 0)

        self.txt_name_input = tk.Entry(self)
        self.txt_name_input.focus()
        self.txt_name_input.grid(column = 1, row = 0, padx = 10)

        self.btn_start = tk.Button(self, text=lb.START_PROCESS_START, command = self.start_process)
        self.btn_start.grid(column=2, row=0, sticky = tk.W, padx = 0, pady = 0, ipadx = 10)

        self.after(const.UPDATE_TIME, self.periodic_call)

    def start_process(self):
         self.socket_cmd('start-process', (self.txt_name_input.get(), 'start-process'))

    def update_ui(self, task):
        DEBUG("task", task)
        cmd, ext = task

        if cmd == 'ok':
            showinfo(lb.START_PROCESS_TITLE, lb.START_PROCESS_START_OK, parent = self)
            self.destroy()
        elif cmd == 'err':
            showerror(lb.START_PROCESS_TITLE, lb.START_PROCESS_START_ERR, parent = self)


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