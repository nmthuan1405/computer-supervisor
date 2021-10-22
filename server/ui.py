from tkinter import *
from tkinter.messagebox import askokcancel, showerror

class server_main(Tk):
    def __init__(self):
        super().__init__()

        self.title("Server")
        self.protocol("WM_DELETE_WINDOW", self.close)
        
        self.btn_start = Button(text = "Start Server", width = 20, height = 5, command = self.start)
        self.btn_start.grid(row = 0, column = 0)

        self.btn_close = Button(text = "Exit", width = 20, height = 2, command = self.close)
        self.btn_close.grid(row = 1, column = 0)

    def start(self):
        pass

    def close(self):
        self.destroy()