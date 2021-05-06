import tkinter as tk
from tkinter import ttk
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
        self.master.geometry('300x420')
        self.master.resizable(0, 0)

        # configure the grid
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=3)
        self.master.columnconfigure(2, weight=1)

        self.lbl_IP_input = Label(self.master, text = "Server IP: ")
        self.lbl_IP_input.grid(column = 0, row = 0, sticky = tk.W, padx = 10, pady = 10)

        self.txt_IP_input = Entry(self.master)
        self.txt_IP_input.insert(-1, 'localhost')
        self.txt_IP_input.focus()
        self.txt_IP_input.grid(column = 1, row = 0)

        self.btn_connect = Button(self.master, text="Connect", command = self.connect)
        self.btn_connect.grid(column=2, row=0, sticky = tk.W, padx = 10, pady = 10)

        self.btn_screenshot = Button(self.master, text = "Screenshot", width = 10, command = self.screenshot)
        self.btn_screenshot.grid(column = 1, row = 2, sticky = tk.N, pady = 5, ipadx = 20, ipady = 8)

        self.btn_process_running = Button(self.master, text = "Process running", width = 10, command = self.runningProcess)
        self.btn_process_running.grid(column = 1, row = 3, sticky = tk.N, pady = 5, ipadx = 20, ipady = 8)

        self.btn_app_running = Button(self.master, text = "App running", width = 10, command = self.runningApp)
        self.btn_app_running.grid(column = 1, row = 4, sticky = tk.N, pady = 5, ipadx = 20, ipady = 8)

        self.btn_keystroke = Button(self.master, text = "Keystroke", width = 10, command=self.keystroke)
        self.btn_keystroke.grid(column = 1, row = 5, sticky = tk.N, pady = 5, ipadx = 20, ipady = 8)

        self.btn_edit_registry = Button(self.master, text = "Edit registry", width = 10, command = self.editRegistry)
        self.btn_edit_registry.grid(column = 1, row = 6, sticky = tk.N, pady = 5, ipadx = 20, ipady = 8)

        self.btn_shutdown = Button(self.master, text = "Shutdown", width = 10, command = self.shutdown)
        self.btn_shutdown.grid(column = 1, row = 7, sticky = tk.N, pady = 5, ipadx = 20, ipady = 8)

        self.btn_exit = Button(self.master, text = "Exit", width = 10, command = self.exit)
        self.btn_exit.grid(column = 1, row = 8, sticky = tk.N, pady = 5, ipadx = 20, ipady = 8)
    
    def connect(self):
        if self.buff == None:
            try:
                self.buff = client.connectServer(self.txt_IP_input.get())
            except:
                showerror(title = 'Error', message = 'Cannot connect to server.')
        else:
            client.sendCloseConection(self.buff)
            self.buff = None

    def screenshot(self):
        if self.buff == None:
            showerror(title = 'Error', message = 'Not connected to the server.')
            return
        window_screenshot = Toplevel()
        screenshotGUI(window_screenshot, self.buff)
        window_screenshot.mainloop()

    def runningProcess(self):
        if self.buff == None:
            showerror(title = 'Error', message = 'Not connected to the server.')
            return        
        window_runningProcess = Toplevel()
        runningProcessGUI(window_runningProcess, self.buff)
        window_runningProcess.mainloop()

    def runningApp(self):
        if self.buff == None:
            showerror(title = 'Error', message = 'Not connected to the server.')
            return        
        window_runningApp = Toplevel()
        runningAppGUI(window_runningApp, self.buff)
        window_runningApp.mainloop()

    def keystroke(self):
        if self.buff == None:
            showerror(title = 'Error', message = 'Not connected to the server.')
            return        
        window_keystroke = Toplevel()
        keystrokeGUI(window_keystroke, self.buff)
        window_keystroke.mainloop()

    def editRegistry(self):
        if self.buff == None:
            showerror(title = 'Error', message = 'Not connected to the server.')
            return        
        window_editRegistry = Toplevel()
        editRegistryGUI(window_editRegistry, self.buff)
        window_editRegistry.mainloop()
    def shutdown(self):
        showinfo(title='Shutdown', message='Shutdown request sent.')

    def exit(self):
        self.master.destroy()
    
class screenshotGUI:
    def __init__(self, master, buff):
        self.buff = buff
        self.master = master
        self.image = None
        self.render = None
        self.master.title("Screenshot")
        self.master.geometry('800x500')
        self.master.focus()
        self.master.grab_set()

        # configure the grid
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        self.master.columnconfigure(2, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=1)
        self.master.rowconfigure(2, weight=1)        
        self.canvas = Canvas(self.master, width = 600, height = 400)  
        self.canvas.grid(column = 0, columnspan = 2, row = 0, rowspan = 2)
        self.imgOnCanvas = self.canvas.create_image(0, 0, anchor = NW)

        self.btn_cap = Button(self.master, text = "Capture", width = 10, height = 2, command = self.capture)
        self.btn_cap.grid(column = 2, row= 0, sticky = tk.W, padx = 5, pady = 5, ipadx = 8, ipady = 40)

        self.btn_save = Button(self.master, text = "Save", width = 10, height = 2, command = self.save)
        self.btn_save.grid(column = 2, row = 1, sticky = tk.W, padx = 5, pady = 5, ipadx = 8, ipady = 40)
        
        self.capture()

    def capture(self):
        self.image = client.getScreenShot(self.buff)

        imageShow = self.image.resize((600, 400), Image.ANTIALIAS)
        self.render = ImageTk.PhotoImage(imageShow)
        self.canvas.itemconfig(self.imgOnCanvas, image = self.render)

    def save(self):
        f = asksaveasfile(mode='w', initialfile = 'screenshot.png', defaultextension=".png",filetypes=[("PNG Files", "*.png")])
        self.image.save(f.name)

class runningProcessGUI:
    def __init__(self, master, buff):
        self.buff = buff
        self.master = master
        self.master.title("Running process")
        self.master.geometry('400x400')
        self.master.focus()
        self.master.grab_set()

        # configure the grid
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        self.master.columnconfigure(2, weight=1)
        self.master.columnconfigure(3, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=1)
        self.master.rowconfigure(2, weight=1)  
        self.master.rowconfigure(3, weight=1) 

        self.btn_kill = Button(self.master, text = "Kill", width = 10, command = self.kill)
        self.btn_kill.grid(column = 0, row = 0, sticky = tk.N, pady = 5, ipady = 10)

        self.btn_show = Button(self.master, text = "Show", width = 10, command = self.show)
        self.btn_show.grid(column = 1, row = 0, sticky = tk.N, pady = 5, ipady = 10)

        self.btn_hide = Button(self.master, text = "Hide", width = 10, command = self.hide)
        self.btn_hide.grid(column = 2, row = 0, sticky = tk.N, pady = 5, ipady = 10)

        self.btn_start = Button(self.master, text = "Start", width = 10, command = self.start)
        self.btn_start.grid(column = 3, row = 0, sticky = tk.N, pady = 5, ipady = 10)

        # columns
        columns = ('#1', '#2', '#3')
        self.tree = ttk.Treeview(self.master, columns = columns, show = 'headings')

        #config column width
        self.tree.column("#1", minwidth = 0, width = 10)
        self.tree.column("#2", minwidth = 0, width = 10)
        self.tree.column("#3", minwidth = 0, width = 10)

        # define headings
        self.tree.heading('#1', text='First Name')
        self.tree.heading('#2', text='Last Name')
        self.tree.heading('#3', text='Email')

        # generate sample data
        contacts = []
        for n in range(1, 100):
            contacts.append((f'first {n}', f'last {n}', f'email{n}@example.com'))
        
        # adding data to the treeview
        for contact in contacts:
            self.tree.insert('', tk.END, values = contact)

        self.tree.grid(row = 1, rowspan = 1, column = 0, columnspan = 4, sticky='nsew')

        # add a scrollbar
        self.scrollbar = ttk.Scrollbar(self.master, orient = tk.VERTICAL, command = self.tree.yview)
        self.tree.configure(yscroll = self.scrollbar.set)
        self.scrollbar.grid(row = 1, column = 4, sticky = 'ns')

    def kill(self):
        pass
    def show(self):
        pass
    def hide(self):
        pass
    def start(self):
        pass

class runningAppGUI:
    def __init__(self, master, buff):
        self.buff = buff
        self.master = master
        self.master.title("Running app")
        self.master.geometry('300x200')
        self.master.focus()
        self.master.grab_set()

class keystrokeGUI:
    def __init__(self, master, buff):
        self.buff = buff
        self.master = master
        self.master.title("Keystroke")
        self.master.geometry('300x200')
        self.master.focus()
        self.master.grab_set()    

class editRegistryGUI:
    def __init__(self, master, buff):
        self.buff = buff
        self.master = master
        self.master.title("Edit registry")
        self.master.geometry('300x200')
        self.master.focus()
        self.master.grab_set()    


window_client = Tk()
a = ClientGUI(window_client)
window_client.mainloop()