import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.messagebox import showerror, showinfo
from tkinter import scrolledtext
from PIL import ImageTk, Image
import client
from tkinter.filedialog import asksaveasfilename, askopenfilename
from functools import partial

def center(toplevel):
    toplevel.update_idletasks()

    screen_width = toplevel.winfo_screenwidth()
    screen_height = toplevel.winfo_screenheight()

    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = screen_width/2 - size[0]/2
    y = screen_height/2 - size[1]/2

    toplevel.geometry("+%d+%d" % (x, y))

class ClientGUI:
    def __init__(self, master):
        self.services = None
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

        self.btn_connect = Button(self.master, text="Connect", width = 10, command = self.connect)
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
        if self.services == None:
            try:
                self.services = client.ClientServices(self.txt_IP_input.get())
                self.services.connectServer()

                self.txt_IP_input.config(state = 'disabled')
                self.btn_connect.config(text = 'Disconnect')
                showinfo("Sucess", "Connect to server sucessfully")
            except:
                showerror(title = 'Error', message = 'Cannot connect to server.')
                self.services = None
        else:
            self.services.sendCloseConection()
            self.services = None

            self.txt_IP_input.config(state = 'normal')
            self.btn_connect.config(text = 'Connect')

    def screenshot(self):
        if self.services == None:
            showerror(title = 'Error', message = 'Not connected to the server.')
            return

        window_screenshot = Toplevel(self.master)
        screenshotGUI(window_screenshot, self.services)
        center(window_screenshot)
        window_screenshot.mainloop()

    def runningProcess(self):
        if self.services == None:
            showerror(title = 'Error', message = 'Not connected to the server.')
            return        

        window_runningProcess = Toplevel(self.master)
        runningProcessGUI(window_runningProcess, self.services)
        center(window_runningProcess)
        window_runningProcess.mainloop()

    def runningApp(self):
        if self.buff == None:
            showerror(title = 'Error', message = 'Not connected to the server.')
            return        
        window_runningApp = Toplevel()
        runningAppGUI(window_runningApp, self.services)
        center(window_runningApp)
        window_runningApp.mainloop()

    def keystroke(self):
        if self.services == None:
            showerror(title = 'Error', message = 'Not connected to the server.')
            return        
        window_keystroke = Toplevel()
        keystrokeGUI(window_keystroke, self.services)
        center(window_keystroke)
        window_keystroke.mainloop()

    def editRegistry(self):
        if self.services == None:
            showerror(title = 'Error', message = 'Not connected to the server.')
            return        
        window_editRegistry = Toplevel()
        editRegistryGUI(window_editRegistry, self.services)
        center(window_editRegistry)
        window_editRegistry.mainloop()
    def shutdown(self):
        showinfo(title='Shutdown', message='Shutdown request sent.')

    def exit(self):
        self.master.destroy()
    
class screenshotGUI:
    def __init__(self, master, services):
        self.master = master
        self.services = services
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
        self.image = self.services.getScreenShot()

        try:
            imageShow = self.image.resize((600, 400), Image.ANTIALIAS)
            self.render = ImageTk.PhotoImage(imageShow)
            self.canvas.itemconfig(self.imgOnCanvas, image = self.render)
        except:
            showerror("Error", "Unable to get screenshot", parent = self.master)

    def save(self):
        print('SAVE SCREENSHOT')
        try:
            f = asksaveasfilename(initialfile = 'screenshot.png', defaultextension=".png", filetypes=[("PNG Files", "*.png")], parent = self.master)
            print('\tPath: ' + f)
            
            self.image.save(f)
        except:
            print('\tErr: Unable to save screenshot')

class runningProcessGUI:
    def __init__(self, master, services):
        self.master = master
        self.services = services
        self.master.title("Running process")
        self.master.focus()
        self.master.grab_set()
        self.master['padx'] = 10
        self.master['pady'] = 10

        self.btn_kill = Button(self.master, text = "Kill", width = 10, command = partial(self.kill, self.master))
        self.btn_kill.grid(column = 0, row = 0, sticky = tk.N, padx = 5, pady = 5, ipady = 10)

        self.btn_show = Button(self.master, text = "Refresh", width = 10, command = self.refresh)
        self.btn_show.grid(column = 1, row = 0, sticky = tk.N, padx = 5, pady = 5, ipady = 10)

        self.btn_hide = Button(self.master, text = "Clear", width = 10, command = self.clear)
        self.btn_hide.grid(column = 2, row = 0, sticky = tk.N, padx = 5, pady = 5, ipady = 10)

        self.btn_start = Button(self.master, text = "Start", width = 10, command = partial(self.start, self.master))
        self.btn_start.grid(column = 3, row = 0, sticky = tk.N, padx = 5, pady = 5, ipady = 10)

        # columns
        columns = ('#1', '#2', '#3')
        self.tree = ttk.Treeview(self.master, columns = columns, show = 'headings', height = 20)

        #config column width
        self.tree.column("#1", minwidth = 0, width = 10)
        self.tree.column("#2", minwidth = 0, width = 10)
        self.tree.column("#3", minwidth = 0, width = 10)

        # define headings
        self.tree.heading('#1', text='Process Name')
        self.tree.heading('#2', text='Process ID')
        self.tree.heading('#3', text='Thread Count')

        # add data
        self.insert(self.services.getProcessList())

        self.tree.grid(row = 1, rowspan = 1, column = 0, padx = 0, pady = 5, columnspan = 4, sticky='nsew')

        # add a scrollbar
        self.scrollbar = ttk.Scrollbar(self.master, orient = tk.VERTICAL, command = self.tree.yview)
        self.tree.configure(yscroll = self.scrollbar.set)
        self.scrollbar.grid(row = 1, column = 4, padx = 0, pady = 5, sticky = 'ns')

    def kill(self, parent):
        uid = self.tree.item(self.tree.focus())['values']
        if uid != '':
            uid = uid[1]

        window_killProcess = Toplevel()
        killProcessGUI(window_killProcess, parent, self.services, uid)
        center(window_killProcess)
        window_killProcess.mainloop()

    def insert(self, data):
        for line in data:
            self.tree.insert('', tk.END, values = line)

    def refresh(self):
        self.clear()
        self.insert(self.services.getProcessList())

    def clear(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

    def start(self, parent):
        window_startProcess = Toplevel()
        startProcessGUI(window_startProcess, parent, self.services)
        center(window_startProcess)
        window_startProcess.mainloop()

class killProcessGUI:
    def __init__(self, master, parent, services, uid):
        self.services = services
        self.master = master
        self.master.title("Kill")
        self.master.focus()
        self.master.grab_set()
        self.master['padx'] = 10
        self.master['pady'] = 10

        self.parent = parent

        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=2)
        self.master.columnconfigure(2, weight=1)

        self.lbl_ID_input = Label(self.master, text = "Process ID: ")
        self.lbl_ID_input.grid(column = 0, row = 0, sticky = tk.W, padx = 0, pady = 0)

        self.txt_ID_input = Entry(self.master)
        self.txt_ID_input.insert(-1, uid)
        self.txt_ID_input.focus()
        self.txt_ID_input.grid(column = 1, row = 0, sticky = tk.W, padx = 10, pady = 0)

        self.btn_kill = Button(self.master, text="Kill", command = self.killProcess)
        self.btn_kill.grid(column=2, row=0, sticky = tk.W, padx = 0, pady = 0, ipadx = 10)

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
    def on_closing(self):
        self.master.destroy()
        self.parent.focus()
        self.parent.grab_set()

    def killProcess(self):
        if (self.services.sendKillProcess(self.txt_ID_input.get()) == 'OK'):
            showinfo("Sucess", "Kill process successful !", parent = self.master)
        else:
            showerror("Error", "Unable to kill this process", parent = self.master)

class startProcessGUI:
    def __init__(self, master, parent, services):
        self.services = services
        self.master = master
        self.master.title("Start")
        # self.master.geometry('400x200')
        self.master.focus()
        self.master.grab_set()
        self.master['padx'] = 10
        self.master['pady'] = 10

        self.parent = parent

        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=2)
        self.master.columnconfigure(2, weight=1)

        self.lbl_ID_input = Label(self.master, text = "Process Name: ")
        self.lbl_ID_input.grid(column = 0, row = 0, sticky = tk.W, padx = 0, pady = 0)

        self.txt_ID_input = Entry(self.master)
        self.txt_ID_input.focus()
        self.txt_ID_input.grid(column = 1, row = 0, sticky = tk.W, padx = 10, pady = 0)

        self.btn_start = Button(self.master, text="Start", command = self.startProcess)
        self.btn_start.grid(column=2, row=0, sticky = tk.W, padx = 0, pady = 0, ipadx = 10)

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
    def on_closing(self):
        self.master.destroy()
        self.parent.focus()
        self.parent.grab_set()

    def startProcess(self):
        if (self.services.sendStartProcess(self.txt_ID_input.get()) == 'OK'):
            showinfo("Sucess", "Start process successful !", parent = self.master)
        else:
            showerror("Error", "Unable to start this process", parent = self.master)

class runningAppGUI:
    def __init__(self, master, services):
        self.services = services
        self.master = master
        self.master.title("Running app")
        # self.master.geometry('300x200')
        self.master.focus()
        self.master.grab_set()
        self.master['padx'] = 10
        self.master['pady'] = 10

        self.btn_kill = Button(self.master, text = "Kill", width = 10, command = self.kill)
        self.btn_kill.grid(column = 0, row = 0, sticky = tk.N, padx = 5, pady = 5, ipady = 10)

        self.btn_show = Button(self.master, text = "Show", width = 10, command = self.show)
        self.btn_show.grid(column = 1, row = 0, sticky = tk.N, padx = 5, pady = 5, ipady = 10)

        self.btn_hide = Button(self.master, text = "Hide", width = 10, command = self.hide)
        self.btn_hide.grid(column = 2, row = 0, sticky = tk.N, padx = 5, pady = 5, ipady = 10)

        self.btn_start = Button(self.master, text = "Start", width = 10, command = self.start)
        self.btn_start.grid(column = 3, row = 0, sticky = tk.N, padx = 5, pady = 5, ipady = 10)

        # columns
        columns = ('#1', '#2', '#3')
        self.tree = ttk.Treeview(self.master, columns = columns, show = 'headings', height = 20)

        #config column width
        self.tree.column("#1", minwidth = 0, width = 10)
        self.tree.column("#2", minwidth = 0, width = 10)
        self.tree.column("#3", minwidth = 0, width = 10)

        # define headings
        self.tree.heading('#1', text='Application Name')
        self.tree.heading('#2', text='Application ID')
        self.tree.heading('#3', text='Thread Count')

        # generate sample data
        contacts = []
        for n in range(1, 100):
            contacts.append((f'Application {n}', f'ID {n}', f'{n}'))
        
        # adding data to the treeview
        for contact in contacts:
            self.tree.insert('', tk.END, values = contact)

        self.tree.grid(row = 1, rowspan = 1, column = 0, padx = 0, pady = 5, columnspan = 4, sticky='nsew')

        # add a scrollbar
        self.scrollbar = ttk.Scrollbar(self.master, orient = tk.VERTICAL, command = self.tree.yview)
        self.tree.configure(yscroll = self.scrollbar.set)
        self.scrollbar.grid(row = 1, column = 4, padx = 0, pady = 5, sticky = 'ns')

    def kill(self):
        window_killApp = Toplevel()
        killAppGUI(window_killApp, self.buff)
        center(window_killApp)
        window_killApp.mainloop()
    def show(self):
        pass
    def hide(self):
        pass
    def start(self):
        window_startApp = Toplevel()
        startAppGUI(window_startApp, self.buff)
        center(window_startApp)
        window_startApp.mainloop()

class killAppGUI:
    def __init__(self, master, buff):
        self.buff = buff
        self.master = master
        self.master.title("Kill")
        # self.master.geometry('400x200')
        self.master.focus()
        self.master.grab_set()
        self.master['padx'] = 10
        self.master['pady'] = 10

        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=2)
        self.master.columnconfigure(2, weight=1)

        self.lbl_ID_input = Label(self.master, text = "Application ID: ")
        self.lbl_ID_input.grid(column = 0, row = 0, sticky = tk.W, padx = 0, pady = 0)

        self.txt_ID_input = Entry(self.master)
        self.txt_ID_input.focus()
        self.txt_ID_input.grid(column = 1, row = 0, sticky = tk.W, padx = 10, pady = 0)

        self.btn_kill = Button(self.master, text="Kill", command = self.killApp)
        self.btn_kill.grid(column=2, row=0, sticky = tk.W, padx = 0, pady = 0, ipadx = 10)

    def killApp(self):
        pass

class startAppGUI:
    def __init__(self, master, buff):
        self.buff = buff
        self.master = master
        self.master.title("Start")
        # self.master.geometry('400x200')
        self.master.focus()
        self.master.grab_set()
        self.master['padx'] = 10
        self.master['pady'] = 10

        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=2)
        self.master.columnconfigure(2, weight=1)

        self.lbl_ID_input = Label(self.master, text = "Application Name: ")
        self.lbl_ID_input.grid(column = 0, row = 0, sticky = tk.W, padx = 0, pady = 0)

        self.txt_ID_input = Entry(self.master)
        self.txt_ID_input.focus()
        self.txt_ID_input.grid(column = 1, row = 0, sticky = tk.W, padx = 10, pady = 0)

        self.btn_start = Button(self.master, text="Start", command = self.startApp)
        self.btn_start.grid(column=2, row=0, sticky = tk.W, padx = 0, pady = 0, ipadx = 10)

    def startApp(self):
        pass

class keystrokeGUI:
    def __init__(self, master, services):
        self.services = services
        self.master = master
        self.master.title("Keystroke")
        # self.master.geometry('300x200')
        self.master.focus()
        self.master.grab_set()
        self.master['padx'] = 10
        self.master['pady'] = 10

        self.btn_hook = Button(self.master, text = "Hook", width = 10, command = self.hook)
        self.btn_hook.grid(column = 0, row = 0, sticky = tk.N, padx = 5, pady = 5, ipady = 10)

        self.btn_unhook = Button(self.master, text = "Unhook", width = 10, command = self.unhook)
        self.btn_unhook.grid(column = 1, row = 0, sticky = tk.N, padx = 5, pady = 5, ipady = 10)
        self.btn_unhook.config(state = 'disabled')

        self.btn_print = Button(self.master, text = "Print", width = 10, command = self.print)
        self.btn_print.grid(column = 2, row = 0, sticky = tk.N, padx = 5, pady = 5, ipady = 10)

        self.btn_clear = Button(self.master, text = "Clear", width = 10, command = self.clear)
        self.btn_clear.grid(column = 3, row = 0, sticky = tk.N, padx = 5, pady = 5, ipady = 10)

        self.text_area = scrolledtext.ScrolledText(self.master, wrap = tk.WORD, width = 41, height = 25)
        self.text_area.grid(column = 0, row = 1, columnspan = 4, pady = 10)
        self.text_area['state'] = 'disabled'

        self.master.protocol("WM_DELETE_WINDOW", self.exit)
        self.services.keylogger_Start()

    def hook(self):
        self.services.keylogger_Command('hook')

        self.btn_hook.config(state = 'disabled')
        self.btn_unhook.config(state = 'normal')

    def unhook(self):
        self.services.keylogger_Command('unhook')

        self.btn_hook.config(state = 'normal')
        self.btn_unhook.config(state = 'disabled')

    def print(self):
        self.text_area.config(state = 'normal')
        self.text_area.delete(1.0, END)
        self.text_area.insert(INSERT, self.services.keylogger_Send())
        self.text_area.config(state = 'disabled')

    def clear(self):
        self.services.keylogger_Command('clear')

        self.text_area.config(state = 'normal')
        self.text_area.delete(1.0, END)
        self.text_area.config(state = 'disabled')
    
    def exit(self):
        self.services.keylogger_Command('exit')
        self.master.destroy()


class editRegistryGUI:
    def __init__(self, master, services):
        self.service = services
        self.master = master
        self.master.title("Edit registry")
        self.master.geometry('430x637')
        self.master.resizable(0, 0)
        self.master.focus()
        self.master.grab_set()

        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        # self.master.columnconfigure(2, weight=1)
        # self.master.columnconfigure(3, weight=1)
        # self.master.rowconfigure(0, weight=1)
        # self.master.rowconfigure(1, weight=1)
        # self.master.rowconfigure(2, weight=1)  
        # self.master.rowconfigure(3, weight=1)
        self.master['padx'] = 10
        self.master['pady'] = 10

        self.lbl_pathInput = Label(self.master, text = "Path")
        self.lbl_pathInput.grid(column = 0, row = 0, sticky = tk.SW)

        self.txt_pathInput = Entry(self.master, width = 53)
        self.txt_pathInput.grid(column = 0, row = 1)
        self.txt_pathInput['state'] = 'readonly'

        self.btn_browse = Button(self.master, text="Browse", command = self.browse)
        self.btn_browse.grid(column = 1, row = 1, padx = 4, ipadx = 10, sticky = E)

        self.lbl_data = Label(self.master, text = "Data")
        self.lbl_data.grid(column = 0, row = 2, sticky = tk.SW)

        self.text_area = scrolledtext.ScrolledText(self.master, wrap = tk.WORD, width = 38, height = 10)
        self.text_area.grid(column = 0, row = 3)

        self.btn_send = Button(self.master, text="Send", command = self.sendReg)
        self.btn_send.grid(column = 1, row = 3, padx = 4, ipadx = 15, ipady = 70, sticky = E)

        self.frame_editDirectly = ttk.LabelFrame(self.master, text = "Edit value directly", relief = tk.RIDGE)
        # self.frame_editDirectly.grid(row = 4, columnspan = 2, column = 0, sticky = tk.E + tk.W + tk.N + tk.S, padx = 0, pady = 4)
        self.frame_editDirectly.place(x = 3, y = 245, height = 370)

        self.lbl_option = Label(self.frame_editDirectly, text = "Select option")
        self.lbl_option.grid(column = 0, row = 0, padx = 2, pady = 0, sticky = tk.SW)

        self.options = ('Get value', 'Set value', 'Delete value', 'Create key', 'Delete key')
        self.selected_option = tk.StringVar()
        self.cbb_option = ttk.Combobox(self.frame_editDirectly, width = 61, textvariable = self.selected_option)
        self.cbb_option['values'] = self.options
        self.cbb_option.current(0)
        self.cbb_option['state'] = 'readonly'  # normal
        self.cbb_option.grid(column = 0, row = 1, columnspan = 4, padx = 5, pady = 0)

        def optionChanged(event):
            if(self.cbb_option.get() == self.options[0]):
                self.lbl_nameValue.grid()
                self.txt_nameValue.grid()

                self.lbl_value.grid_remove()
                self.txt_value.grid_remove()

                self.txt_seperator.grid_remove()

                self.lbl_dataType.grid_remove()
                self.cbb_dataType.grid_remove()

            if(self.cbb_option.get() == self.options[1]):
                self.lbl_nameValue.grid()
                self.txt_nameValue.grid()

                self.lbl_value.grid(column = 1, row = 4, padx = 2, pady = 0, sticky = tk.SW)
                self.txt_value.grid(column = 1, columnspan = 2, row = 5, padx = 5, pady = 0)

                self.lbl_dataType.grid(column = 3, row = 4, padx = 2, pady = 0, sticky = tk.SW)
                self.cbb_dataType.grid(column = 3, row = 5, padx = 5, pady = 0)

                if(self.cbb_dataType.get() == self.dataTypes[4]):
                    self.txt_value.config(width = 19)
                    self.txt_value.grid_remove()
                    self.txt_value.grid(column = 1, columnspan = 1, row = 5, padx = 5, pady = 0)
                    self.txt_seperator.grid(column = 2, row = 5, padx = 5, pady = 0)

            if(self.cbb_option.get() == self.options[2]):
                self.lbl_nameValue.grid()
                self.txt_nameValue.grid()

                self.lbl_value.grid_remove()
                self.txt_value.grid_remove()

                self.txt_seperator.grid_remove()

                self.lbl_dataType.grid_remove()
                self.cbb_dataType.grid_remove()

            if(self.cbb_option.get() == self.options[3]):
                self.lbl_nameValue.grid_remove()
                self.txt_nameValue.grid_remove()

                self.lbl_value.grid_remove()
                self.txt_value.grid_remove()

                self.txt_seperator.grid_remove()

                self.lbl_dataType.grid_remove()
                self.cbb_dataType.grid_remove()

            if(self.cbb_option.get() == self.options[4]):
                self.lbl_nameValue.grid_remove()
                self.txt_nameValue.grid_remove()

                self.lbl_value.grid_remove()
                self.txt_value.grid_remove()

                self.txt_seperator.grid_remove()

                self.lbl_dataType.grid_remove()
                self.cbb_dataType.grid_remove()

        self.cbb_option.bind('<<ComboboxSelected>>', optionChanged)

        self.lbl_pathInput2 = Label(self.frame_editDirectly, text = "Path")
        self.lbl_pathInput2.grid(column = 0, row = 2, padx = 2, pady = 0, sticky = tk.SW)

        self.txt_pathInput2 = Entry(self.frame_editDirectly, width = 64)
        self.txt_pathInput2.grid(column = 0, row = 3, columnspan = 4, padx = 5)

        self.lbl_nameValue = Label(self.frame_editDirectly, text = "Name Value")
        self.lbl_nameValue.grid(column = 0, row = 4, padx = 2, pady = 0, sticky = tk.SW)

        self.txt_nameValue = Entry(self.frame_editDirectly, width = 15)
        self.txt_nameValue.grid(column = 0, row = 5, padx = 5, pady = 0, sticky = tk.W)

        self.lbl_value = Label(self.frame_editDirectly, text = "Value")
        # self.lbl_value.grid(column = 1, row = 4, padx = 2, pady = 0, sticky = tk.SW)

        self.txt_value = Entry(self.frame_editDirectly, width = 25)
        # self.txt_value.grid(column = 1, columnspan = 2, row = 5, padx = 5, pady = 0)

        self.txt_seperator = Entry(self.frame_editDirectly, width = 3, justify = 'center')
        self.txt_seperator.insert(-1, '\\0')
        # self.txt_seperator.grid(column = 2, row = 5, padx = 5, pady = 0)

        self.lbl_dataType = Label(self.frame_editDirectly, text = "Data type")
        # self.lbl_dataType.grid(column = 3, row = 4, padx = 2, pady = 0, sticky = tk.SW)

        self.dataTypes = ('String', 'Binary', 'DWORD', 'QWORD', 'Multi-String', 'Expandable String')
        self.selected_dataType = tk.StringVar()
        self.cbb_dataType = ttk.Combobox(self.frame_editDirectly, width = 16, textvariable = self.selected_dataType)
        self.cbb_dataType.set('default') # chưa hiện đc chữ default
        self.cbb_dataType['values'] = self.dataTypes
        self.cbb_dataType.current(0)
        self.cbb_dataType['state'] = 'readonly'  # normal
        # self.cbb_dataType.grid(column = 3, row = 5, padx = 5, pady = 0)

        def dataTypeChanged(event):
            if(self.cbb_dataType.get() == self.dataTypes[0]):
                self.lbl_nameValue.grid()
                self.txt_nameValue.grid()

                self.lbl_value.grid()
                self.txt_value.config(width = 25)
                self.txt_value.grid(column = 1, columnspan = 2, row = 5, padx = 5, pady = 0)

                self.txt_seperator.grid_remove()

                self.lbl_dataType.grid()
                self.cbb_dataType.grid()
            
            if(self.cbb_dataType.get() == self.dataTypes[1]):
                self.lbl_nameValue.grid()
                self.txt_nameValue.grid()

                self.lbl_value.grid()
                self.txt_value.config(width = 25)
                self.txt_value.grid(column = 1, columnspan = 2, row = 5, padx = 5, pady = 0)

                self.txt_seperator.grid_remove()

                self.lbl_dataType.grid()
                self.cbb_dataType.grid()

            if(self.cbb_dataType.get() == self.dataTypes[2]):
                self.lbl_nameValue.grid()
                self.txt_nameValue.grid()

                self.lbl_value.grid()
                self.txt_value.config(width = 25)
                self.txt_value.grid(column = 1, columnspan = 2, row = 5, padx = 5, pady = 0)

                self.txt_seperator.grid_remove()

                self.lbl_dataType.grid()
                self.cbb_dataType.grid()

            if(self.cbb_dataType.get() == self.dataTypes[3]):
                self.lbl_nameValue.grid()
                self.txt_nameValue.grid()

                self.lbl_value.grid()
                self.txt_value.config(width = 25)
                self.txt_value.grid(column = 1, columnspan = 2, row = 5, padx = 5, pady = 0)

                self.txt_seperator.grid_remove()

                self.lbl_dataType.grid()
                self.cbb_dataType.grid()

            if(self.cbb_dataType.get() == self.dataTypes[4]):
                self.lbl_nameValue.grid()
                self.txt_nameValue.grid()

                self.lbl_value.grid()
                self.txt_value.config(width = 19)
                self.txt_value.grid(column = 1, columnspan = 1, row = 5, padx = 5, pady = 0)

                self.txt_seperator.grid(column = 2, row = 5, padx = 5, pady = 0)

                self.lbl_dataType.grid()
                self.cbb_dataType.grid()

            if(self.cbb_dataType.get() == self.dataTypes[5]):
                self.lbl_nameValue.grid()
                self.txt_nameValue.grid()

                self.lbl_value.grid()
                self.txt_value.config(width = 25)
                self.txt_value.grid(column = 1, columnspan = 2, row = 5, padx = 5, pady = 0)

                self.txt_seperator.grid_remove()

                self.lbl_dataType.grid()
                self.cbb_dataType.grid()

        self.cbb_dataType.bind('<<ComboboxSelected>>', dataTypeChanged)

        self.lbl_result = Label(self.frame_editDirectly, text = "Result")
        self.lbl_result.place(x = 4, y = 130)
        # self.lbl_result.grid(column = 0, row = 6, padx = 2, pady = 0, sticky = tk.SW)

        self.result_area = scrolledtext.ScrolledText(self.frame_editDirectly, wrap = tk.WORD, width = 46, height = 10, bg = "gray92", state = tk.DISABLED)
        self.result_area.place(x = 4, y = 150)
        # self.result_area.grid(column = 0, row = 7, columnspan = 4, padx = 5, pady = 0)

        self.button1 = ttk.Button(self.frame_editDirectly, text="Send", command = self.sendCommand)
        self.button1.place(x = 100, y = 320)
        # self.button1.grid(row=8, column=0, pady = 5, sticky = W)
        self.button2 = ttk.Button(self.frame_editDirectly, text="Clear log", command = self.clearLog)
        self.button2.place(x = 220, y = 320)
        # self.button2.grid(row=8, column=1, pady = 5, sticky = W)

    def browse(self):
        try:
            filename = askopenfilename(defaultextension=".reg", filetypes=[("Registry Files", "*.reg"), ("All Files", "*.*")], parent = self.master)
            self.txt_pathInput.config(state = 'normal')
            self.txt_pathInput.delete(0, END)
            self.txt_pathInput.insert(-1, filename)
            self.txt_pathInput.config(state = 'readonly')

            f = open(filename, 'r', encoding = "utf-16")
            data = f.read()
            f.close()
        except:
            data = 'ERROR'

        self.text_area.delete(1.0, END)
        self.text_area.insert(INSERT, data)

    def sendReg(self):
        if self.service.sendRegFile(self.text_area.get(1.0, END)) == 'OK':
            showinfo('Success', 'Merge registry successfully')             
        else:
            showerror('Error', 'Unable to merge registry')

    def sendCommand(self):
        if self.cbb_option.get() == self.options[0]:
            data = self.service.sendRegGetVal(self.txt_pathInput2.get(), self.txt_nameValue.get())
            if (len(data) == 2):

                if data[1] == self.dataTypes[1]:
                    dataDisplay = str(data[0].hex())
                else:
                    dataDisplay = str(data[0])

                self.writeLog(self.txt_nameValue.get() + ': ' + dataDisplay)
                self.writeLog('\t\tType: ' + data[1])
            else:
                self.writeLog(self.txt_nameValue.get() + ': Error')

        elif self.cbb_option.get() == self.options[1]:
            data = self.txt_value.get()
            type = self.cbb_dataType.get()

            try:
                if type == self.dataTypes[1]:
                    data = bytearray.fromhex(data)
                elif type == self.dataTypes[2] or type == self.dataTypes[3]:
                    data = int(data)
                elif type == self.dataTypes[4]:
                    data = data.split(self.txt_seperator.get())

                    dataDisplay = ['\'' + element + '\'' for element in data]
                    self.writeLog('Data: ' + ', '.join(dataDisplay))
            except:
                self.writeLog('Unable to parse data')
                return

            if self.service.sendRegSetVal(self.txt_pathInput2.get(), self.txt_nameValue.get(), data, type) == 'OK':
                self.writeLog('Set value successfully')
            else:
                self.writeLog('Unable to set value')

        elif (self.cbb_option.get() == self.options[2]):
            if self.service.sendRegDeVal(self.txt_pathInput2.get(), self.txt_nameValue.get()) == 'OK':
                self.writeLog('Delete value successfully')
            else:
                self.writeLog('Unable to delete value')
            
        elif (self.cbb_option.get() == self.options[3]):
            if self.service.sendRegCreateKey(self.txt_pathInput2.get()) == 'OK':
                self.writeLog('Create key successfully')
            else:
                self.writeLog('Unable to create key')
            
        elif (self.cbb_option.get() == self.options[4]):
            if self.service.sendRegDelKey(self.txt_pathInput2.get()) == 'OK':
                self.writeLog('Delete key successfully')
            else:
                self.writeLog('Unable to delete key')
            

    def clearLog(self):
        self.result_area.config(state = 'normal')
        self.result_area.delete(1.0, END)
        self.result_area.config(state = 'disabled')

    def writeLog(self, data):
        self.result_area.config(state='normal')
        self.result_area.insert(INSERT, data + '\n')
        self.result_area.config(state='disabled')
        self.result_area.see('end')

window_client = Tk()
a = ClientGUI(window_client)
center(window_client)
window_client.mainloop()