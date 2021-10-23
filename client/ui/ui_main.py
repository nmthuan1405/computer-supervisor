import tkinter as tk
import ui.label as lb
import queue

class UI_main(tk.Tk):
    def __init__(self):
        self.ui_queue = queue.Queue()
        self.socket_queue = None

        super().__init__()
        self.title(lb.MAIN_TITLE)
        # self.protocol("WM_DELETE_WINDOW", self.close)

        
        self.after(200, self.periodic_call)

    
    
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