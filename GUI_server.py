from tkinter import *
from tkinter.messagebox import askokcancel
import server


class Server_GUI:
    def __init__(self, master):
        self.services = None
        self.master = master

        self.master.title("Server")
        self.master.geometry('200x200')

        self.btn_start = Button(self.master, text = "Start Server", width = 20, height = 5, command = self.start)
        self.btn_start.place(relx = 0.5, rely = 0.5, anchor = CENTER)

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def start(self):
        if self.services == None:
            try:
                self.services = server.ServerServices()
                self.services.startServices()

                self.btn_start.config(text = "Stop Server")
            except:
                print('Cannot create server')
                self.services = None
        else:
            self.services.stopServices()
            self.services = None

            self.btn_start.config(text = "Start Server")

    def on_closing(self):
        if self.services != None:
            if askokcancel("Quit", "Server is running.\nDo you want to quit?"):
                self.services.stopServices()
            else:
                return
            
        self.master.destroy()

            

window_server = Tk()
Server_GUI(window_server)
window_server.mainloop()
