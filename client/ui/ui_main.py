from tkinter.messagebox import askokcancel, showerror, showinfo
import tkinter as tk
import ui.label as lb
import ui.constraints as const
import ui.ui_template as tpl
import ui.ui_screenStream as sc
import ui.ui_keylogger as kl
import ui.ui_fileExplorer as fe
import ui.ui_registry as reg
import ui.ui_runningApps as ra
import ui.ui_runningProcesses as rp

class UI_main(tpl.UI_MainTemplate):
    def __init__(self, ui_queues):
        tpl.UI_MainTemplate.__init__(self, const.MAIN, ui_queues)

        self.title(lb.MAIN_TITLE)
        self.resizable(False, False)

        self.lbl_app_name = tk.Label(self, text = lb.MAIN_APP_NAME, font = ("Arial", 16))
        self.lbl_app_name.grid(row = 0, column = 0, columnspan = 3, padx = 10, pady = 10)

        self.lbl_IP_input = tk.Label(self, text = lb.MAIN_LBL_SERVER_IP)
        self.lbl_IP_input.grid(row= 1, column = 0, sticky = tk.W, padx = 10, pady = 10)

        self.txt_IP_input = tk.Entry(self)
        self.txt_IP_input.insert(-1, lb.MAIN_DEFAULT_IP)
        self.txt_IP_input.focus()
        self.txt_IP_input.grid(row = 1, column = 1)

        self.btn_connect_stt = tk.StringVar(self, lb.MAIN_CONNECT)
        self.btn_connect = tk.Button(self, textvariable = self.btn_connect_stt, width = 10, command = self.connect)
        self.btn_connect.grid(row = 1, column = 2, sticky = tk.W, padx = 10, pady = 10)

        self.lbl_MAC_address_stt = tk.StringVar(self, lb.MAIN_LBL_MAC_ADDRESS)
        self.lbl_MAC_address = tk.Label(self, textvariable = self.lbl_MAC_address_stt)
        self.lbl_MAC_address.grid(row = 2, column = 0, sticky = tk.W, padx = 10)

        self.MAC_address_stt = tk.StringVar(self, lb.MAIN_MAC_ADDRESS)
        self.MAC_address = tk.Label(self, textvariable = self.MAC_address_stt, cursor = "hand2")
        self.MAC_address.grid(row = 2, column = 1, columnspan = 2, sticky = tk.W)
        # bind mouse click event
        self.MAC_address.bind("<Button-1>", self.on_click_MAC_address)

        self.btn_screen_stream = tk.Button(self, text = lb.MAIN_SCREEN_STREAM, width = 15, height = 2, command = self.screen_stream)
        self.btn_screen_stream.grid(row = 3, column = 0, sticky = tk.W, padx = 10, pady = 10)

        self.btn_keylogger = tk.Button(self, text = lb.MAIN_KEYLOGGER, width = 15, height = 2, command = self.keylogger)
        self.btn_keylogger.grid(row = 3, column = 1, sticky = tk.W, padx = 10, pady = 10)

        self.btn_file_explorer = tk.Button(self, text = lb.MAIN_FILE_EXPLORER, width = 15, height = 2, command = self.file_explorer)
        self.btn_file_explorer.grid(row = 3, column = 2, sticky = tk.W, padx = 10, pady = 10)

        self.btn_running_apps = tk.Button(self, text = lb.MAIN_RUNNING_APPS, width = 15, height = 2, command = self.running_apps)
        self.btn_running_apps.grid(row = 4, column = 0, sticky = tk.W, padx = 10, pady = 10)

        self.btn_running_processes = tk.Button(self, text = lb.MAIN_RUNNING_PROCESSES, width = 15, height = 2, command = self.running_processes)
        self.btn_running_processes.grid(row = 4, column = 1, sticky = tk.W, padx = 10, pady = 10)
        
        self.btn_edit_registry = tk.Button(self, text = lb.MAIN_EDIT_REGISTRY, width = 15, height = 2, command = self.edit_registry)
        self.btn_edit_registry.grid(row = 4, column = 2, sticky = tk.W, padx = 10, pady = 10)

        self.btn_logout = tk.Button(self, text = lb.MAIN_LOGOUT, width = 15, height = 2, command = self.logout)
        self.btn_logout.grid(row = 5, column = 0, sticky = tk.W, padx = 10, pady = 10)

        self.btn_shutdown = tk.Button(self, text = lb.MAIN_SHUTDOWN, width = 15, height = 2, command = self.shutdown)
        self.btn_shutdown.grid(row = 5, column = 1, sticky = tk.W, padx = 10, pady = 10)

        self.btn_restart = tk.Button(self, text = lb.MAIN_RESTART, width = 15, height = 2, command = self.restart)
        self.btn_restart.grid(row = 5, column = 2, sticky = tk.W, padx = 10, pady = 10)

        self.btn_exit = tk.Button(self, text = lb.MAIN_EXIT, width = 15, height = 2, command = self.close)
        self.btn_exit.grid(row = 6, column = 0, columnspan = 3, padx = 10, pady = 10)

        self.lbl_about_us = tk.Label(self, text = lb.MAIN_ABOUT_US, cursor = "hand2")
        self.lbl_about_us.grid(row = 7, column = 0, columnspan = 3, padx = 10, pady = 10)
        self.lbl_about_us.bind("<Button-1>", self.about_us)

    def on_click_MAC_address(self, event):
        self.socket_cmd("get-MAC")
        
    def close(self):
        if self.btn_connect_stt.get() == lb.MAIN_DISCONNECT:
            if askokcancel(lb.QUIT, lb.MAIN_ASK_QUIT):
                self.socket_cmd("stop")
            else:
                return
        
        self.socket_cmd('exit')
        super().close()

    def connect(self):
        if self.btn_connect_stt.get() == lb.MAIN_CONNECT:
            ip = self.txt_IP_input.get()
            self.socket_cmd("start", ip)
        elif self.btn_connect_stt.get() == lb.MAIN_DISCONNECT:
            self.socket_cmd("stop")

        self.btn_connect_stt.set(lb.WAIT)

    def screen_stream(self):
        if self.btn_connect_stt.get() != lb.MAIN_DISCONNECT:
            showinfo(lb.INFO, lb.MAIN_PLEASE_CONNECT)
            return

        window = sc.UI_screen_stream(self, self.socket_queue, self.ui_queues)
        window.grab_set()
        window.focus()

    def keylogger(self):
        if self.btn_connect_stt.get() != lb.MAIN_DISCONNECT:
            showinfo(lb.INFO, lb.MAIN_PLEASE_CONNECT)
            return

        window = kl.UI_keylogger(self, self.socket_queue, self.ui_queues)
        window.grab_set()
        window.focus()

    def file_explorer(self):
        if self.btn_connect_stt.get() != lb.MAIN_DISCONNECT:
            showinfo(lb.INFO, lb.MAIN_PLEASE_CONNECT)
            return

        window = fe.UI_file_explorer(self, self.socket_queue, self.ui_queues)
        window.grab_set()
        window.focus()

    def edit_registry(self):
        if self.btn_connect_stt.get() != lb.MAIN_DISCONNECT:
            showinfo(lb.INFO, lb.MAIN_PLEASE_CONNECT)
            return

        window = reg.UI_registry(self, self.socket_queue, self.ui_queues)
        window.grab_set()
        window.focus()

    def running_apps(self):
        if self.btn_connect_stt.get() != lb.MAIN_DISCONNECT:
            showinfo(lb.INFO, lb.MAIN_PLEASE_CONNECT)
            return

        window = ra.UI_running_apps(self, self.socket_queue, self.ui_queues)
        window.grab_set()
        window.focus()

    def running_processes(self):
        if self.btn_connect_stt.get() != lb.MAIN_DISCONNECT:
            showinfo(lb.INFO, lb.MAIN_PLEASE_CONNECT)
            return

        window = rp.UI_running_processes(self, self.socket_queue, self.ui_queues)                               
        window.grab_set()
        window.focus()

    def logout(self):
        if self.btn_connect_stt.get() != lb.MAIN_DISCONNECT:
            showinfo(lb.INFO, lb.MAIN_PLEASE_CONNECT)
            return

        if askokcancel(lb.MAIN_LOGOUT, lb.MAIN_LOGOUT_CONFIRM):
            self.socket_cmd("logout")
            showinfo(lb.MAIN_LOGOUT, lb.MAIN_LOGOUT_SUCCESS)

    def shutdown(self):
        if self.btn_connect_stt.get() != lb.MAIN_DISCONNECT:
            showinfo(lb.INFO, lb.MAIN_PLEASE_CONNECT)
            return

        if askokcancel(lb.MAIN_SHUTDOWN, lb.MAIN_SHUTDOWN_CONFIRM):
            self.socket_cmd("shutdown")
            showinfo(lb.MAIN_SHUTDOWN, lb.MAIN_SHUTDOWN_SUCCESS)

    def restart(self):
        if self.btn_connect_stt.get() != lb.MAIN_DISCONNECT:
            showinfo(lb.INFO, lb.MAIN_PLEASE_CONNECT)
            return
            
        if askokcancel(lb.MAIN_RESTART, lb.MAIN_RESTART_CONFIRM):
            self.socket_cmd("restart")
            showinfo(lb.MAIN_RESTART, lb.MAIN_RESTART_SUCCESS)

    def about_us(self, event):
        showinfo(lb.MAIN_ABOUT_US, lb.MAIN_ABOUT_US_TEXT)
    
    def change_connect_btn_default(self):
            self.btn_connect_stt.set(lb.MAIN_CONNECT)
            self.txt_IP_input.config(state = tk.NORMAL)
            self.MAC_address_stt.set("")
    
    def handle_error(self):
        self.change_connect_btn_default()
        showerror(lb.ERR, lb.MAIN_SOCKET_ERROR, parent = self)
        self.socket_cmd("continue-work")
    
    def update_ui(self, task):
        print('task in main', task)
        cmd, ext = task
        if cmd == "start":
            if ext == "ok":
                self.btn_connect_stt.set(lb.MAIN_DISCONNECT)
                self.txt_IP_input.config(state = tk.DISABLED)
                self.socket_cmd("get-MAC")
            else:
                self.change_connect_btn_default()
                showerror(lb.ERR, lb.MAIN_CANNOT_CONNECT, parent = self)
        
        elif cmd == "stop":
            self.change_connect_btn_default()

        elif cmd == "update-MAC":
            self.MAC_address_stt.set(ext)
