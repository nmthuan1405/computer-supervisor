from tkinter import *
import server

def func_start(window_name):
    def clicked_start():
        server.createSocket()

    btn_start = Button(window_name, text="Start", width = 20, height = 3, command = clicked_start)
    btn_start.pack()
    # btn_start.grid(column = 0, row = 0)

def GUI_Server():
    window_server = Tk()
    window_server.title("Server")
    window_server.geometry('200x100')

    func_start(window_server)

    window_server.mainloop()

GUI_Server()