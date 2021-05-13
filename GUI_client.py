import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.messagebox import showerror, showwarning, showinfo
from tkinter import scrolledtext
from PIL import ImageTk, Image
import client
from tkinter.filedialog import asksaveasfilename, askopenfilename
from functools import partial

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

        window_screenshot = Toplevel()
        screenshotGUI(window_screenshot, self.services)
        window_screenshot.mainloop()

    def runningProcess(self):
        if self.services == None:
            showerror(title = 'Error', message = 'Not connected to the server.')
            return        

        window_runningProcess = Toplevel()
        runningProcessGUI(window_runningProcess, self.services)
        window_runningProcess.mainloop()

    def runningApp(self):
        if self.buff == None:
            showerror(title = 'Error', message = 'Not connected to the server.')
            return        
        window_runningApp = Toplevel()
        runningAppGUI(window_runningApp, self.services)
        window_runningApp.mainloop()

    def keystroke(self):
        if self.services == None:
            showerror(title = 'Error', message = 'Not connected to the server.')
            return        
        window_keystroke = Toplevel()
        keystrokeGUI(window_keystroke, self.services)
        window_keystroke.mainloop()

    def editRegistry(self):
        # if self.services == None:
        #     showerror(title = 'Error', message = 'Not connected to the server.')
        #     return        
        window_editRegistry = Toplevel()
        editRegistryGUI(window_editRegistry, self.services)
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

        imageShow = self.image.resize((600, 400), Image.ANTIALIAS)
        self.render = ImageTk.PhotoImage(imageShow)
        self.canvas.itemconfig(self.imgOnCanvas, image = self.render)

    def save(self):
        f = asksaveasfilename(initialfile = 'screenshot.png', defaultextension=".png",filetypes=[("PNG Files", "*.png")])
        self.image.save(f)

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
        self.tree = ttk.Treeview(self.master, columns = columns, show = 'headings')

        #config column width
        self.tree.column("#1", minwidth = 0, width = 10)
        self.tree.column("#2", minwidth = 0, width = 10)
        self.tree.column("#3", minwidth = 0, width = 10)

        # define headings
        self.tree.heading('#1', text='Process Name')
        self.tree.heading('#2', text='Process ID')
        self.tree.heading('#3', text='Thread Count')

        # generate sample data
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
        self.tree = ttk.Treeview(self.master, columns = columns, show = 'headings')

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
        window_killApp.mainloop()
    def show(self):
        pass
    def hide(self):
        pass
    def start(self):
        window_startApp = Toplevel()
        startAppGUI(window_startApp, self.buff)
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

        self.text_area = scrolledtext.ScrolledText(self.master, wrap = tk.WORD, width = 41, height = 10)
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
        # self.master.geometry('400x200')
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

        self.txt_pathInput = Entry(self.master, width = 60)
        self.txt_pathInput.insert(-1, 'Path')
        # self.txt_pathInput.focus()
        self.txt_pathInput.grid(column = 0, row = 0)
        self.txt_pathInput['state'] = 'readonly'

        self.btn_browse = Button(self.master, text="Browse", command = self.browse)
        self.btn_browse.grid(column=1, row=0, padx = 5, ipadx = 10)

        self.text_area = scrolledtext.ScrolledText(self.master, wrap = tk.WORD, width = 43, height = 10)
        self.text_area.grid(column = 0, row = 1, pady = 10)

        self.btn_send = Button(self.master, text="Send", command = self.sendReg)
        self.btn_send.grid(column=1, row=1, padx = 0, ipadx = 15, ipady = 70)

        self.frame_editDirectly = ttk.LabelFrame(self.master, text = "Edit value directly", relief = tk.RIDGE)
        self.frame_editDirectly.grid(row = 2, columnspan = 2, column = 0, sticky = tk.E + tk.W + tk.N + tk.S, padx = 0, pady = 4)
        self.frame_editDirectly.columnconfigure(0, weight=1)
        self.frame_editDirectly.columnconfigure(1, weight=1)
        self.frame_editDirectly.columnconfigure(2, weight=1)
        self.frame_editDirectly.columnconfigure(3, weight=1)

        self.options = ('Get value', 'Set value', 'Delete value', 'Create key', 'Delete key')
        selected_option = tk.StringVar()
        self.cbb_option = ttk.Combobox(self.frame_editDirectly, width = 67, textvariable = selected_option)
        self.cbb_option.set('default') #chưa hiện đc chữ default
        self.cbb_option['values'] = self.options
        self.cbb_option['state'] = 'readonly'  # normal
        self.cbb_option.grid(column = 0, row = 0, columnspan = 4, padx = 5, pady = 5)

        def optionChanged(event):
            if(self.cbb_option.get() == self.options[0]):
                self.txt_nameValue.grid()
                self.txt_value.grid_remove()
                self.cbb_dataType.grid_remove()
            if(self.cbb_option.get() == self.options[1]):
                self.txt_nameValue.grid()
                self.txt_value.grid()
                self.cbb_dataType.grid()
            if(self.cbb_option.get() == self.options[2]):
                self.txt_nameValue.grid()
                self.txt_value.grid_remove()
                self.cbb_dataType.grid_remove()
            if(self.cbb_option.get() == self.options[3]):
                self.txt_nameValue.grid_remove()
                self.txt_value.grid_remove()
                self.cbb_dataType.grid_remove()
            if(self.cbb_option.get() == self.options[4]):
                self.txt_nameValue.grid_remove()
                self.txt_value.grid_remove()
                self.cbb_dataType.grid_remove()
                
        self.cbb_option.bind('<<ComboboxSelected>>', optionChanged)

        self.txt_pathInput2 = Entry(self.frame_editDirectly, width = 70)
        self.txt_pathInput2.insert(-1, 'Path')
        self.txt_pathInput2.grid(column = 0, row = 1, columnspan = 4, padx = 5)

        self.txt_nameValue = Entry(self.frame_editDirectly, width = 15)
        self.txt_nameValue.insert(-1, 'Name value')
        self.txt_nameValue.grid(column = 0, row = 2, padx = 5, pady = 5)

        self.txt_value = Entry(self.frame_editDirectly, width = 20)
        self.txt_value.insert(-1, 'Value')
        self.txt_value.grid(column = 1, row = 2, padx = 5, pady = 5)

        self.txt_seperator = Entry(self.frame_editDirectly, width = 10)
        self.txt_seperator.insert(-1, 'Seperator')
        self.txt_seperator.grid(column = 2, row = 2, padx = 5, pady = 5)

        dataTypes = ('String', 'Binary', 'DWORD', 'QWORD', 'Multi-String', 'Expandable String')
        selected_dataType = tk.StringVar()
        self.cbb_dataType = ttk.Combobox(self.frame_editDirectly, width = 15, textvariable = selected_dataType)
        self.cbb_dataType.set('default') # chưa hiện đc chữ default
        self.cbb_dataType['values'] = dataTypes
        self.cbb_dataType['state'] = 'readonly'  # normal
        self.cbb_dataType.grid(column = 3, row = 2, padx = 5, pady = 5)

        self.result_area = scrolledtext.ScrolledText(self.frame_editDirectly, wrap = tk.WORD, width = 51, height = 10, bg = "gray92", state = tk.DISABLED)
        self.result_area.grid(column = 0, row = 3, columnspan = 4, padx = 5, pady = 5)

        self.button1 = ttk.Button(self.frame_editDirectly, text="Send", command = self.sendCommand)
        self.button1.grid(row=4, column=1, pady = 5)
        self.button2 = ttk.Button(self.frame_editDirectly, text="Delete", command = self.clearLog)
        self.button2.grid(row=4, column=2, pady = 5)

    def browse(self):
        try:
            filename = askopenfilename(defaultextension=".reg", filetypes=[("Registry Files", "*.reg"), ("All Files", "*.*")])
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
        if (self.service.sendRegFile(self.text_area.get(1.0, END)) == 'OK'):
            pass

    def sendCommand(self):
        # get value
        if (self.cbb_option.get() == self.options[0]):
            data = self.service.sendRegGetVal(self.txt_pathInput2.get(), self.txt_nameValue.get())

            self.result_area.config(state='normal')
            self.result_area.insert(INSERT, str(data[0]))
            self.result_area.config(state='disabled')
            pass

        elif (self.cbb_option.get() == self.options[1]):
            pass
        elif (self.cbb_option.get() == self.options[2]):
            pass
        elif (self.cbb_option.get() == self.options[3]):
            pass
        elif (self.cbb_option.get() == self.options[4]):
            pass

    def clearLog(self):
        self.result_area.config(state = 'normal')
        self.result_area.delete(1.0, END)
        self.result_area.config(state = 'disabled')

window_client = Tk()
a = ClientGUI(window_client)
window_client.mainloop()