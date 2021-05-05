import tkinter
from tkinter import *
from tkinter.messagebox import showerror, showwarning, showinfo
from PIL import ImageTk, Image
import client
from functools import partial
from tkinter.filedialog import asksaveasfile

class ClientGUI:
    def __init__(self, master):
        self.buff = None
        self.master = master
        self.master.title("Client")
        self.master.geometry('240x330')


        self.lbl_IP_input = Label(self.master, text = "IP: ")
        self.lbl_IP_input.grid(column = 0, row = 0)

        self.txt_IP_input = Entry(self.master, width = 20)
        self.txt_IP_input.focus()
        self.txt_IP_input.grid(column = 1, row = 0)

        self.btn_connect = Button(self.master, text="Connect", command = self.connect)
        self.btn_connect.grid(column=2, row=0)

        self.btn_screenshot = Button(self.master, text = "Screenshot", width = 20, height = 2, command = self.screenshot)
        self.btn_screenshot.grid(column = 1, row = 2)

        self.btn_process_running = Button(self.master, text = "Process running", width = 20, height = 2, command = self.processRunning)
        self.btn_process_running.grid(column = 1, row = 3)

        self.btn_app_running = Button(self.master, text = "App running", width = 20, height = 2, command = self.appRunning)
        self.btn_app_running.grid(column = 1, row = 4)

        self.btn_keystroke = Button(self.master, text = "Keystroke", width = 20, height = 2, command=self.keystroke)
        self.btn_keystroke.grid(column = 1, row = 5)

        self.btn_edit_registry = Button(self.master, text = "Edit registry", width = 20, height = 2, command = self.editRegistry)
        self.btn_edit_registry.grid(column = 1, row = 6)

        self.btn_shutdown = Button(self.master, text = "Shutdown", width = 20, height = 2, command = self.shutdown)
        self.btn_shutdown.grid(column = 1, row = 7)

        self.btn_exit = Button(self.master, text = "Exit", width = 20, height = 2, command = self.exit)
        self.btn_exit.grid(column = 1, row = 8)
    
    def connect(self):
        self.buff = client.connectServer('temp')

    def screenshot(self):
        window_screenshot = Toplevel()
        screenshotGUI(window_screenshot, self.buff)
        window_screenshot.mainloop()

    def processRunning(self):
        pass
    def appRunning(self):
        pass
    def keystroke(self):
        pass
    def editRegistry(self):
        pass
    def shutdown(self):
        pass
    def exit(self):
        pass
    
class screenshotGUI:
    def __init__(self, master, buff):
        self.buff = buff
        self.master = master
        self.image = None
        self.render = None
        self.master.title("Screenshot")
        self.master.geometry('700x500')
        self.master.focus()
        self.master.grab_set()
        
        self.canvas = Canvas(self.master, width = 600, height = 400)  
        self.canvas.grid(column = 0, row = 0)
        self.imgOnCanvas = self.canvas.create_image(0, 0, anchor = NW)

        self.btn_cap = Button(self.master, text = "Capture", width = 10, height = 2, command = self.capture)
        self.btn_cap.grid(column = 0, row= 1)

        self.btn_save = Button(self.master, text = "Save", width = 10, height = 2, command = self.save)
        self.btn_save.grid(column = 1, row = 1)
        
        self.capture()

    def capture(self):
        self.image = client.getScreenShot(self.buff)

        imageShow = self.image.resize((600, 400), Image.ANTIALIAS)
        self.render = ImageTk.PhotoImage(imageShow)
        self.canvas.itemconfig(self.imgOnCanvas, image = self.render)

    def save(self):
        f = asksaveasfile(mode='w', initialfile = 'screenshot.png', defaultextension=".png",filetypes=[("PNG Files", "*.png")])
        self.image.save(f.name)


# def GUI_process_running():
#     window_process_running=Toplevel()
#     window_process_running.title("Process running")
#     window_process_running.geometry('320x200')
#     window_process_running.focus()
#     window_process_running.grab_set()

#     def clicked_kill():
#         return
#     btn_kill=Button(window_process_running, text="Kill", width=10, height=2, command=clicked_kill)
#     btn_kill.grid(column=0, row=0)
#     def clicked_show():
#         return
#     btn_show=Button(window_process_running, text="Show", width=10, height=2, command=clicked_show)
#     btn_show.grid(column=1, row=0)
#     def clicked_hide():
#         return
#     btn_hide=Button(window_process_running, text="Hide", width=10, height=2, command=clicked_hide)
#     btn_hide.grid(column=2, row=0)
#     def clicked_start():
#         return
#     btn_start=Button(window_process_running, text="Start", width=10, height=2, command=clicked_start)
#     btn_start.grid(column=3, row=0)

#     window_process_running.mainloop()

# def func_process_running(window_name):
#     def clicked_process_running():
#         if connection_status==0:
#             showerror(title='Error', message='Not connected to the server.')
#             return
#         GUI_process_running()
    
#     btn_process_running=Button(window_name, text="Process running", width=20, height=2, command=clicked_process_running)
#     btn_process_running.grid(column=1, row=3)

# def GUI_app_running():
#     window_app_running=Toplevel()
#     window_app_running.title("App running")
#     window_app_running.geometry('300x200')
#     window_app_running.focus()
#     window_app_running.grab_set()
#     window_app_running.mainloop()

# def func_app_running(window_name):
#     def clicked_app_running():
#         if connection_status==0:
#             showerror(title='Error', message='Not connected to the server.')
#             return        
#         GUI_app_running()
    
    

# def GUI_keystroke():
#     window_keystroke=Toplevel()
#     window_keystroke.title("Keystroke")
#     window_keystroke.geometry('300x200')
#     window_keystroke.focus()
#     window_keystroke.grab_set()
#     window_keystroke.mainloop()

# def func_keystroke(window_name):
#     def clicked_keystroke():
#         if connection_status==0:
#             showerror(title='Error', message='Not connected to the server.')
#             return                
#         GUI_keystroke()
    
#     btn_keystroke=Button(window_name, text="Keystroke", width=20, height=2, command=clicked_keystroke)
#     btn_keystroke.grid(column=1, row=5)

# def GUI_edit_registry():
#     window_edit_registry=Toplevel()
#     window_edit_registry.title("Edit registry")
#     window_edit_registry.geometry('300x200')
#     window_edit_registry.focus()
#     window_edit_registry.grab_set()
#     window_edit_registry.mainloop()

# def func_edit_registry(window_name):
#     def clicked_edit_registry():
#         if connection_status==0:
#             showerror(title='Error', message='Not connected to the server.')
#             return        
#         GUI_edit_registry()
    
#     btn_edit_registry=Button(window_name, text="Edit registry", width=20, height=2, command=clicked_edit_registry)
#     btn_edit_registry.grid(column=1, row=6)

# def GUI_shutdown():
#     window_shutdown=Toplevel()
#     window_shutdown.title("Shutdown")
#     window_shutdown.geometry('300x200')
#     window_shutdown.focus()
#     window_shutdown.grab_set()
#     window_shutdown.mainloop()

# def func_shutdown(window_name):
#     def clicked_shutdown():
#         if connection_status==0:
#             showerror(title='Error', message='Not connected to the server.')
#             return        
#         GUI_shutdown()
    
#     btn_shutdown=Button(window_name, text="Shutdown", width=20, height=2, command=clicked_shutdown)
#     btn_shutdown.grid(column=1, row=7)

# def func_exit(window_name):
#     def clicked_exit():
#         window_name.destroy()   #đóng cửa sổ window_name
    
#     btn_exit=Button(window_name, text="Exit", width=20, height=2, command=clicked_exit)
#     btn_exit.grid(column=1, row=8)

window_client = Tk()
a = ClientGUI(window_client)
window_client.mainloop()