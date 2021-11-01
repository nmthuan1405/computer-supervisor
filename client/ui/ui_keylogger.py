import tkinter as tk
import tkinter.scrolledtext as st
import ui.label as lb
import ui.constraints as const
import queue

class UI_keylogger(tk.Toplevel):
    def __init__(self, parent):
        self.ui_queue = queue.Queue()
        self.socket_queue = None

        super().__init__(parent)
        self.title = lb.KEYLOGGER_TITLE
        self.resizable(False, False)
        self['padx'] = const.WINDOW_BORDER_PADDING
        self['pady'] = const.WINDOW_BORDER_PADDING

        self.btn_hook_stt = tk.StringVar(self, lb.KEYLOGGER_HOOK)
        self.btn_hook = tk.Button(self, textvariable = self.btn_hook_stt, width = 15, height = 2, command = self.hook)
        self.btn_hook.grid(row = 0, column = 0, padx = 10)

        self.btn_clear = tk.Button(self, text = lb.KEYLOGGER_CLEAR, width = 15, height = 2, command = self.clear)
        self.btn_clear.grid(row = 1, column = 0, padx = 10)

        self.btn_block_stt = tk.StringVar(self, lb.KEYLOGGER_BLOCK)
        self.btn_block = tk.Button(self, textvariable = self.btn_block_stt, width = 15, height = 4, command = self.block)
        self.btn_block.grid(row = 0, column = 1, rowspan = 2, padx = 10, sticky = tk.NS)
        
        self.text_log = st.ScrolledText(self, wrap = tk.WORD, width = 40, height = 20)
        self.text_log.grid(row = 2, column = 0, columnspan = 2, pady = (10,0))
        self.text_log['state'] = 'disabled'

        self.after(const.UPDATE_TIME, self.periodic_call)

    def hook(self):
        if self.btn_hook_stt.get() == lb.KEYLOGGER_HOOK:
            self.btn_hook_stt.set(lb.KEYLOGGER_UNHOOK)
        else:
            self.btn_hook_stt.set(lb.KEYLOGGER_HOOK)
    def clear(self):
        return
    def block(self):
        if self.btn_block_stt.get() == lb.KEYLOGGER_BLOCK:
            self.btn_block_stt.set(lb.KEYLOGGER_UNBLOCK)
        else:
            self.btn_block_stt.set(lb.KEYLOGGER_BLOCK)

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