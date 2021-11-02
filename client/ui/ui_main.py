from tkinter.messagebox import askokcancel, showerror, showinfo
import tkinter as tk
import ui.label as lb
import ui.constraints as const
import queue

import ui.ui_screenStream as sc
import ui.ui_keylogger as kl
import ui.ui_fileExplorer as fe
import ui.ui_registry as reg
import ui.ui_runningApps as ra
import ui.ui_runningProcesses as rp

class UI_main(tk.Tk):
    def __init__(self):
        self.ui_queue = queue.Queue()
        self.ui_queues = {'main': self.ui_queue}
        self.socket_queue = None

        super().__init__()
        self.title(lb.MAIN_TITLE)
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.resizable(False, False)

        self.lbl_app_name = tk.Label(text = lb.THIS_APP_NAME, font = ("Arial", 16))
        self.lbl_app_name.grid(row = 0, column = 0, columnspan = 3, padx = 10, pady = 10)

        self.lbl_IP_input = tk.Label(text = lb.LBL_SERVER_IP)
        self.lbl_IP_input.grid(row= 1, column = 0, sticky = tk.W, padx = 10, pady = 10)

        self.txt_IP_input = tk.Entry()
        self.txt_IP_input.insert(-1, lb.DEFAULT_IP)
        self.txt_IP_input.focus()
        self.txt_IP_input.grid(row = 1, column = 1)

        self.btn_connect_stt = tk.StringVar(self, lb.CONNECT)
        self.btn_connect = tk.Button(textvariable = self.btn_connect_stt, width = 10, command = self.connect)
        self.btn_connect.grid(row = 1, column=2, sticky = tk.W, padx = 10, pady = 10)

        self.lbl_MAC_address_stt = tk.StringVar(self, lb.MAC_ADDRESS)
        self.lbl_MAC_address = tk.Label(textvariable = self.lbl_MAC_address_stt, cursor = "hand2")
        self.lbl_MAC_address.grid(row = 2, column = 0, columnspan = 3, sticky = tk.W, padx = 10)
        # bind mouse click event
        self.lbl_MAC_address.bind("<Button-1>", self.onClickMACAddress)

        self.btn_screen_stream = tk.Button(text = lb.SCREEN_STREAM, width = 15, height = 2, command = self.screenStream)
        self.btn_screen_stream.grid(row = 3, column=0, sticky = tk.W, padx = 10, pady = 10)

        self.btn_keylogger = tk.Button(text = lb.KEYLOGGER, width = 15, height = 2, command = self.keylogger)
        self.btn_keylogger.grid(row = 3, column=1, sticky = tk.W, padx = 10, pady = 10)

        self.btn_file_explorer = tk.Button(text = lb.FILE_EXPLORER, width = 15, height = 2, command = self.fileExplorer)
        self.btn_file_explorer.grid(row = 3, column=2, sticky = tk.W, padx = 10, pady = 10)

        self.btn_edit_registry = tk.Button(text = lb.EDIT_REGISTRY, width = 15, height = 2, command = self.editRegistry)
        self.btn_edit_registry.grid(row = 4, column=0, sticky = tk.W, padx = 10, pady = 10)

        self.btn_running_apps = tk.Button(text = lb.RUNNING_APPS, width = 15, height = 2, command = self.runningApps)
        self.btn_running_apps.grid(row = 4, column=1, sticky = tk.W, padx = 10, pady = 10)

        self.btn_running_processes = tk.Button(text = lb.RUNNING_PROCESSES, width = 15, height = 2, command = self.runningProcesses)
        self.btn_running_processes.grid(row = 4, column=2, sticky = tk.W, padx = 10, pady = 10)

        self.btn_shutdown = tk.Button(text = lb.SHUTDOWN, width = 15, height = 2, command = self.shutdown)
        self.btn_shutdown.grid(row = 5, column=0, columnspan = 2, sticky = tk.NS, padx = 10, pady = 10)

        self.btn_logout = tk.Button(text = lb.LOGOUT, width = 15, height = 2, command = self.logout)
        self.btn_logout.grid(row = 5, column=1, columnspan = 2, sticky = tk.NS, padx = 10, pady = 10)

        self.lbl_about_us = tk.Label(text = lb.ABOUT_US, cursor = "hand2")
        self.lbl_about_us.grid(row = 6, column = 0, columnspan = 3, padx = 10, pady = 10)
        self.lbl_about_us.bind("<Button-1>", self.onClickAboutUs)
        
        self.after(const.UPDATE_TIME, self.periodic_call)

    def close(self):
        if self.btn_connect_stt.get() == lb.DISCONNECT:
            if askokcancel(lb.QUIT, lb.ASK_QUIT):
                self.socket_cmd("stop")
            else:
                return
        
        self.socket_cmd('exit')
        self.destroy()

    def connect(self):
        if self.btn_connect_stt.get() == lb.CONNECT:
            ip = self.txt_IP_input.get()
            self.socket_cmd("start", ip)
        elif self.btn_connect_stt.get() == lb.DISCONNECT:
            self.socket_cmd("stop")

        self.btn_connect_stt.set(lb.WAIT)
    

    def onClickMACAddress(self, event):
        if self.lbl_MAC_address_stt.get() == lb.MAC_ADDRESS:
            self.lbl_MAC_address_stt.set(lb.MAC_ADDRESS +" default MAC address")
        else:
            self.lbl_MAC_address_stt.set(lb.MAC_ADDRESS)
        self.socket_cmd("getMACAddress")


    def screenStream(self):
        window = sc.UI_screenStream(self, self.socket_queue)
        self.ui_queues['screen'] = window.ui_queue

        window.grab_set()
        window.focus()

    def keylogger(self):
        window = kl.UI_keylogger(self, self.socket_queue)
        self.ui_queues['keyboard'] = window.ui_queue

        window.grab_set()
        window.focus()

    def fileExplorer(self):
        window = fe.UI_fileExplorer(self, self.socket_queue)
        self.ui_queues['file'] = window.ui_queue
        
        window.grab_set()
        window.focus()

    def editRegistry(self):
        window = reg.UI_Registry(self, self.socket_queue)
        self.ui_queues['registry'] = window.ui_queue

        window.grab_set()
        window.focus()

    def runningApps(self):
        window = ra.UI_runningApps(self, self.socket_queue)
        self.ui_queues['apps'] = window.ui_queue

        window.grab_set()
        window.focus()

    def runningProcesses(self):
        window = rp.UI_runningProcesses(self, self.socket_queue)
        self.ui_queues['processes'] = window.ui_queue

        window.grab_set()
        window.focus()

    def shutdown(self):
        if askokcancel(lb.SHUTDOWN, lb.SHUTDOWN_CONFIRM):
            self.socket_cmd("shutdown")
            showinfo(lb.SHUTDOWN, lb.SHUTDOWN_SUCCESS)

    def logout(self):
        if askokcancel(lb.LOGOUT, lb.LOGOUT_CONFIRM):
            self.socket_cmd("logout")
            showinfo(lb.LOGOUT, lb.LOGOUT_SUCCESS)

    def onClickAboutUs(self, event):
        showinfo(lb.ABOUT_US, lb.ABOUT_US_TEXT)
    
    def update_ui(self, task):
        DEBUG("task", task)
        cmd, ext = task
        if cmd == "start":
            self.btn_connect_stt.set(lb.CONNECT)
            self.txt_IP_input.config(state = tk.NORMAL)
        elif cmd == "stop":
            self.btn_connect_stt.set(lb.DISCONNECT)
            self.txt_IP_input.config(state = tk.DISABLED)
        elif cmd == "err":
            if ext == "cannot start":
                showerror(lb.ERR, lb.CANNOT_CONNECT)

    def periodic_call(self):
        while True:
            try:
                task = self.ui_queue.get_nowait()
                self.update_ui(task)
                
            except queue.Empty:
                break
        
        self.after(const.UPDATE_TIME, self.periodic_call)

    def add_socket_queue(self, socket_queue):
        self.socket_queue = socket_queue
    
    def socket_cmd(self, cmd, ext = None):
        self.socket_queue.put((cmd, ext))

def DEBUG(*args,**kwargs):
    print("UI:", *args,**kwargs)