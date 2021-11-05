import tkinter as tk
import ui.label as lb
import ui.constraints as const
from PIL import ImageTk
from tkinter.filedialog import asksaveasfilename
from tkinter.messagebox import showerror, showinfo, askokcancel
from services.count import Count
import queue

class UI_screen_stream(tk.Toplevel):
    def __init__(self, parent, socket_queue, ui_queues):
        super().__init__(parent)
        self.ui_queue = queue.Queue()
        self.socket_queue = socket_queue
        ui_queues['screen'] = self.ui_queue

        self.title = lb.SCREEN_STREAM_TITLE
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.resizable(False, False)
        self['padx'] = const.WINDOW_BORDER_PADDING
        self['pady'] = const.WINDOW_BORDER_PADDING

        self.canvas = tk.Canvas(self, width = const.FRAME_WIDTH, height = const.FRAME_HEIGHT, bg = 'black')
        self.canvas.grid(row = 0, column = 0)
        self.img_on_canvas = self.canvas.create_image(0, 0, anchor = tk.NW)

        self.frame = tk.Frame(self)
        self.btn_pause_stt = tk.StringVar(self.frame, lb.PAUSE)
        self.btn_pause = tk.Button(self.frame, textvariable = self.btn_pause_stt, width = 10, height = 2, command = self.pause_stream)
        self.btn_pause.grid(row = 0, column = 0, padx = (0,5))

        self.btn_capture_stt = tk.StringVar(self.frame, lb.CAPTURE)
        self.btn_capture = tk.Button(self.frame, textvariable=self.btn_capture_stt, width = 15, height = 2, command = self.capture_stream)
        self.btn_capture.grid(row = 0, column = 1)
        self.frame.grid(row = 1, column = 0, pady = (5,0), sticky = tk.E)
        
        self.update_counting = Count(1, self.socket_cmd, 'update-stream', (const.FRAME_WIDTH, const.FRAME_HEIGHT))
        self.update_counting.count_up(-1)
        self.after(const.UPDATE_TIME, self.periodic_call)

    def pause_stream(self):
        if self.btn_pause_stt.get() == lb.PAUSE:
            self.btn_pause_stt.set(lb.RESUME)
        else:
            self.btn_pause_stt.set(lb.PAUSE)

    def capture_stream(self):
        if self.btn_capture_stt.get() == lb.CAPTURE:
            self.socket_cmd('capture-stream')
            self.btn_capture_stt.set(lb.WAIT)

    def close(self):
        self.destroy()

    def update_ui(self, task):
        DEBUG("task", task)
        cmd, ext = task

        if cmd == 'update-stream':
            self.render = ImageTk.PhotoImage(ext)
            self.canvas.itemconfig(self.img_on_canvas, image = self.render)
        elif cmd == 'save-image':
            try:
                f = asksaveasfilename(initialfile = 'screenshot.png', defaultextension=".png", filetypes=[("PNG Files", "*.png")], parent=self)
                ext.save(f)
            except:
                showerror(lb.ERR, lb.ERROR_SAVE_FILE, parent=self)
            finally:
                self.btn_capture_stt.set(lb.CAPTURE)

    def periodic_call(self):
        if self.btn_pause_stt.get() == lb.PAUSE and self.btn_capture_stt.get() == lb.CAPTURE:
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

def DEBUG(*args,**kwargs):
    print("UI:", *args,**kwargs)