import queue
import tkinter as tk
import ui.constraints as const

class UI_Template():
    def __init__(self, name, socket_queue, ui_queues):
        self.name = name
        self.socket_queue = socket_queue

        self.ui_queue = queue.Queue()
        self.ui_queues = ui_queues
        ui_queues[name] = self.ui_queue

    def add_socket_queue(self, socket_queue):
        self.socket_queue = socket_queue

    def socket_cmd(self, cmd, *args):
        self.socket_queue.put((cmd, args))

    def close(self):
        self.ui_queues.pop(self.name)

    def DEBUG(self, *args, **kwargs):
        print((self.name, ':', args, kwargs))

class UI_MainTemplate(UI_Template, tk.Tk):
    def __init__(self, name, ui_queues):
        tk.Tk.__init__(self)
        UI_Template.__init__(self, name, None, ui_queues)
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.after(const.UPDATE_TIME[self.name], self.periodic_call)
    
    def update_ui(self, task):
        pass

    def periodic_call(self):
        while True:
            try:
                task = self.ui_queue.get_nowait()
                if task == 'socket-error':
                    self.handle_error()
                    
                else:
                    self.update_ui(task)
                
            except queue.Empty:
                break
        self.after(const.UPDATE_TIME[self.name], self.periodic_call)
    
    def handle_error(self):
        self.close()

    def close(self):
        super().close()
        self.destroy()

class UI_ToplevelTemplate(UI_Template, tk.Toplevel):
    def __init__(self, parent, name, socket_queue, ui_queues):
        tk.Toplevel.__init__(self, parent)
        UI_Template.__init__(self, name, socket_queue, ui_queues)
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.after(const.UPDATE_TIME[self.name], self.periodic_call)
    
    def update_ui(self, task):
        pass

    def periodic_call(self):
        while True:
            try:
                task = self.ui_queue.get_nowait()
                if task == 'socket-error':
                    self.handle_error()
                    return
            
                else:
                    self.update_ui(task)
                
            except queue.Empty:
                break
        self.after(const.UPDATE_TIME[self.name], self.periodic_call)

    def handle_error(self):
        self.close()

    def close(self):
        super().close()
        self.destroy()
