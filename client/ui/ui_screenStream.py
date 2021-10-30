import tkinter as tk
import ui.label as lb
import queue

class UI_screenStream(tk.Toplevel):
    def __init__(self, parent):
        self.ui_queue = queue.Queue()
        self.socket_queue = None

        super().__init__(parent)
        self.title = lb.SCREEN_STREAM_TITLE
        self.resizable(False, False)

        self.canvas = tk.Canvas(self, width = 600, height = 400, bg = 'black')
        self.canvas.grid(row = 0, column = 0, columnspan = 2, padx = 10, pady = 10)
        self.imgOnCanvas = self.canvas.create_image(0, 0, anchor = tk.NW)

        self.btn_pause_stt = tk.StringVar(self, lb.PAUSE)
        self.btn_pause = tk.Button(self, textvariable = self.btn_pause_stt, width = 10, height = 2, command = self.pauseStream)
        self.btn_pause.grid(row = 1, column = 0, padx = 10, pady = 10)

        self.btn_capture = tk.Button(self, text = lb.CAPTURE, width = 10, height = 2, command = self.captureStream)
        self.btn_capture.grid(row = 1, column = 1, padx = 10, pady = 10)
        
        self.after(200, self.periodic_call)

    def pauseStream(self):
        if self.btn_pause_stt.get() == lb.PAUSE:
            self.btn_pause_stt.set(lb.RESUME)
        else:
            self.btn_pause_stt.set(lb.PAUSE)

    def captureStream(self):
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