from tkinter.messagebox import askokcancel, showerror
import tkinter as tk
import ui.label as lb
import queue

class UI_main(tk.Tk):
    def __init__(self):
        self.ui_queue = queue.Queue()
        self.socket_queue = None

        super().__init__()
        self.title(lb.MAIN_TITLE)
        self.protocol("WM_DELETE_WINDOW", self.close)

        self.btn_start_stt = tk.StringVar(self, lb.START)
        self.btn_start = tk.Button(textvariable = self.btn_start_stt, width = 20, height = 5, command = self.start)
        self.btn_start.grid(row = 0, column = 0)

        self.btn_close = tk.Button(text = lb.EXIT, width = 20, height = 2, command = self.close)
        self.btn_close.grid(row = 1, column = 0)

        self.after(200, self.periodic_call)

    def start(self):
        if self.btn_start_stt.get() == lb.START:
            self.socket_cmd('start')
        else:
            self.socket_cmd('stop')

        self.btn_start_stt.set(lb.WAIT)

    def close(self):
        if self.btn_start_stt.get() == lb.STOP:
            if askokcancel(lb.QUIT, lb.ASK_QUIT):
                self.socket_cmd("stop")
            else:
                return

        self.socket_cmd('exit')
        self.destroy()
    
    def update_ui(self, task):
        DEBUG("task", task)
        cmd, ext = task
        if cmd == "start":
            self.btn_start_stt.set(lb.START)
        elif cmd == "stop":
            self.btn_start_stt.set(lb.STOP)
        elif cmd == "err":
            if ext == "cannot start":
                showerror(lb.ERR, lb.CANNOT_START)

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