import tkinter as tk
from tkinter.filedialog import asksaveasfilename
from tkinter.messagebox import showerror, showinfo, askokcancel

import ui.label as lb
import ui.constraints as const
import ui.ui_template as tpl

import queue
from PIL import ImageTk
from services.count import Count

class UI_screen_stream(tpl.UI_ToplevelTemplate):
    def __init__(self, parent, socket_queue, ui_queues):
        tpl.UI_ToplevelTemplate.__init__(self, parent, const.SCREEN, socket_queue, ui_queues)
        self.FRAME_HEIGHT = None

        self.title = lb.SCREEN_STREAM_TITLE
        self.resizable(False, False)
        self['padx'] = const.WINDOW_BORDER_PADDING
        self['pady'] = const.WINDOW_BORDER_PADDING

        self.canvas = tk.Canvas(self, width = const.FRAME_WIDTH, height = 0, bg = 'black')
        self.canvas.grid(row = 0, column = 0)
        self.img_on_canvas = self.canvas.create_image(0, 0, anchor = tk.NW)

        self.frame = tk.Frame(self)
        self.btn_pause_stt = tk.StringVar(self.frame, lb.SCREEN_STREAM_PAUSE)
        self.btn_pause = tk.Button(self.frame, textvariable = self.btn_pause_stt, width = 10, height = 2, command = self.pause_stream)
        self.btn_pause.grid(row = 0, column = 0, padx = (0,5))

        self.btn_capture_stt = tk.StringVar(self.frame, lb.SCREEN_STREAM_CAPTURE)
        self.btn_capture = tk.Button(self.frame, textvariable=self.btn_capture_stt, width = 15, height = 2, command = self.capture_stream)
        self.btn_capture.grid(row = 0, column = 1)
        self.frame.grid(row = 1, column = 0, pady = (5,0), sticky = tk.E)
        
        self.update_counter = Count(0, self.socket_cmd, 'update-stream', const.FRAME_WIDTH, self.FRAME_HEIGHT)
        self.update_counter.count_up(-1)

    def pause_stream(self):
        if self.btn_pause_stt.get() == lb.SCREEN_STREAM_PAUSE:
            self.btn_pause_stt.set(lb.SCREEN_STREAM_RESUME)
        else:
            self.btn_pause_stt.set(lb.SCREEN_STREAM_PAUSE)

    def capture_stream(self):
        if self.btn_capture_stt.get() == lb.SCREEN_STREAM_CAPTURE:
            self.socket_cmd('capture-stream')
            self.btn_capture_stt.set(lb.WAIT)

    def update_ui(self, task):
        cmd, ext = task

        if cmd == 'update-stream':
            if self.FRAME_HEIGHT is None:
                self.FRAME_HEIGHT = ext.size[1]
                self.canvas.config(height = self.FRAME_HEIGHT)
                self.update_counter.update_args('update-stream', const.FRAME_WIDTH, self.FRAME_HEIGHT)

            self.render = ImageTk.PhotoImage(ext)
            self.canvas.itemconfig(self.img_on_canvas, image = self.render)
        
        elif cmd == 'save-image':
            try:
                f = asksaveasfilename(initialfile = 'screenshot.png', defaultextension=".png", filetypes=[("PNG Files", "*.png")], parent=self)
                ext.save(f)
            except:
                showerror(lb.ERR, lb.SCREEN_STREAM_ERROR_SAVE_FILE, parent=self)
            finally:
                self.btn_capture_stt.set(lb.SCREEN_STREAM_CAPTURE)

    def periodic_call(self):
        if self.btn_pause_stt.get() == lb.SCREEN_STREAM_PAUSE and self.btn_capture_stt.get() == lb.SCREEN_STREAM_CAPTURE:
            self.update_counter.count_up()

        super().periodic_call()