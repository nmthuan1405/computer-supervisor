import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as st
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter.messagebox import showerror, showinfo

import ui.label as lb
import ui.constraints as const
import ui.ui_template as tpl
import queue
class UI_registry(tpl.UI_ToplevelTemplate):
    def __init__(self, parent, socket_queue, ui_queues):
        super().__init__(parent, const.REGISTRY, socket_queue, ui_queues)

        self.title = lb.REGISTRY_TITLE
        self.geometry('430x637')
        self.resizable(False, False)
        self['padx'] = const.WINDOW_BORDER_PADDING
        self['pady'] = const.WINDOW_BORDER_PADDING
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.lbl_path_input = tk.Label(self, text = lb.REGISTRY_LBL_PATH_INPUT)
        self.lbl_path_input.grid(column = 0, row = 0, sticky = tk.SW)

        self.txt_path_input = tk.Entry(self, width = 53)
        self.txt_path_input.grid(column = 0, row = 1)
        self.txt_path_input['state'] = 'readonly'

        self.btn_browse = tk.Button(self, text=lb.REGISTRY_BROWSE, command = self.browse)
        self.btn_browse.grid(column = 1, row = 1, padx = 4, ipadx = 10, sticky = tk.E)

        self.lbl_data = tk.Label(self, text = lb.REGISTRY_LBL_DATA)
        self.lbl_data.grid(column = 0, row = 2, sticky = tk.SW)

        self.text_area = st.ScrolledText(self, wrap = tk.WORD, width = 38, height = 10)
        self.text_area.grid(column = 0, row = 3)
    
        self.btn_send_stt = tk.StringVar(value = lb.REGISTRY_SEND)
        self.btn_send = tk.Button(self, textvariable=self.btn_send_stt, command = self.send_reg)
        self.btn_send.grid(column = 1, row = 3, padx = 4, ipadx = 15, ipady = 70, sticky = tk.E)

        self.frame_edit_directly = tk.LabelFrame(self, text = lb.REGISTRY_FRAME_EDIT_DIRECT, relief = tk.RIDGE)
        self.frame_edit_directly.place(x = 3, y = 245, height = 370)

        self.lbl_option = tk.Label(self.frame_edit_directly, text = lb.REGISTRY_LBL_OPTION)
        self.lbl_option.grid(column = 0, row = 0, padx = 2, pady = 0, sticky = tk.SW)

        self.options = ('Get value', 'Set value', 'Delete value', 'Create key', 'Delete key')
        self.selected_option = tk.StringVar()
        self.cbb_option = ttk.Combobox(self.frame_edit_directly, width = 61, textvariable = self.selected_option)
        self.cbb_option['values'] = self.options
        self.cbb_option.current(0)
        self.cbb_option['state'] = 'readonly'  # normal
        self.cbb_option.grid(column = 0, row = 1, columnspan = 4, padx = 5, pady = 0)

        def option_changed(event):
            if(self.cbb_option.get() == self.options[0]):
                self.lbl_name_value.grid()
                self.txt_name_value.grid()

                self.lbl_value.place_forget()
                self.txt_value.grid_remove()

                self.txt_seperator.grid_remove()

                self.lbl_data_type.grid_remove()
                self.cbb_data_type.grid_remove()

            if(self.cbb_option.get() == self.options[1]):
                self.lbl_name_value.grid()
                self.txt_name_value.grid()

                self.lbl_value.place(x = 108, y = 82)
                self.txt_value.grid(column = 1, columnspan = 2, row = 5, padx = 5, pady = 0)

                self.lbl_data_type.grid(column = 3, row = 4, padx = 2, pady = 0, sticky = tk.SW)
                self.cbb_data_type.grid(column = 3, row = 5, padx = 5, pady = 0)

                if(self.cbb_data_type.get() == self.data_types[4]):
                    self.txt_value.config(width = 19)
                    self.txt_value.grid_remove()
                    self.txt_value.grid(column = 1, columnspan = 1, row = 5, padx = 5, pady = 0)
                    self.txt_seperator.grid(column = 2, row = 5, padx = 5, pady = 0)

            if(self.cbb_option.get() == self.options[2]):
                self.lbl_name_value.grid()
                self.txt_name_value.grid()

                self.lbl_value.place_forget()
                self.txt_value.grid_remove()

                self.txt_seperator.grid_remove()

                self.lbl_data_type.grid_remove()
                self.cbb_data_type.grid_remove()

            if(self.cbb_option.get() == self.options[3]):
                self.lbl_name_value.grid_remove()
                self.txt_name_value.grid_remove()

                self.lbl_value.place_forget()
                self.txt_value.grid_remove()

                self.txt_seperator.grid_remove()

                self.lbl_data_type.grid_remove()
                self.cbb_data_type.grid_remove()

            if(self.cbb_option.get() == self.options[4]):
                self.lbl_name_value.grid_remove()
                self.txt_name_value.grid_remove()

                self.lbl_value.place_forget()
                self.txt_value.grid_remove()

                self.txt_seperator.grid_remove()

                self.lbl_data_type.grid_remove()
                self.cbb_data_type.grid_remove()

        self.cbb_option.bind('<<ComboboxSelected>>', option_changed)

        self.lbl_path_input_direct = tk.Label(self.frame_edit_directly, text = lb.REGISTRY_LBL_PATH_INPUT)
        self.lbl_path_input_direct.grid(column = 0, row = 2, padx = 2, pady = 0, sticky = tk.SW)

        self.txt_path_input_direct = tk.Entry(self.frame_edit_directly, width = 64)
        self.txt_path_input_direct.grid(column = 0, row = 3, columnspan = 4, padx = 5)

        self.lbl_name_value = tk.Label(self.frame_edit_directly, text = lb.REGISTRY_LBL_NAME_VALUE)
        self.lbl_name_value.grid(column = 0, row = 4, padx = 2, pady = 0, sticky = tk.SW)

        self.txt_name_value = tk.Entry(self.frame_edit_directly, width = 15)
        self.txt_name_value.grid(column = 0, row = 5, padx = 5, pady = 0, sticky = tk.W)

        self.lbl_value = tk.Label(self.frame_edit_directly, text = lb.REGISTRY_LBL_VALUE)

        self.txt_value = tk.Entry(self.frame_edit_directly, width = 25)

        self.txt_seperator = tk.Entry(self.frame_edit_directly, width = 3, justify = 'center')
        self.txt_seperator.insert(-1, lb.REGISTRY_SEPERATOR)

        self.lbl_data_type = tk.Label(self.frame_edit_directly, text = lb.REGISTRY_DATA_TYPE)

        self.data_types = ('String', 'Binary', 'DWORD', 'QWORD', 'Multi-String', 'Expandable String')
        self.selected_data_type = tk.StringVar()
        self.cbb_data_type = ttk.Combobox(self.frame_edit_directly, width = 16, textvariable = self.selected_data_type)
        self.cbb_data_type['values'] = self.data_types
        self.cbb_data_type.current(0)
        self.cbb_data_type['state'] = 'readonly'  # normal

        def data_type_changed(event):
            if(self.cbb_data_type.get() == self.data_types[0]):
                self.lbl_name_value.grid()
                self.txt_name_value.grid()

                self.lbl_value.place(x = 108, y = 82)
                self.txt_value.config(width = 25)
                self.txt_value.grid(column = 1, columnspan = 2, row = 5, padx = 5, pady = 0)

                self.txt_seperator.grid_remove()

                self.lbl_data_type.grid()
                self.cbb_data_type.grid()
            
            if(self.cbb_data_type.get() == self.data_types[1]):
                self.lbl_name_value.grid()
                self.txt_name_value.grid()

                self.lbl_value.place(x = 108, y = 82)
                self.txt_value.config(width = 25)
                self.txt_value.grid(column = 1, columnspan = 2, row = 5, padx = 5, pady = 0)

                self.txt_seperator.grid_remove()

                self.lbl_data_type.grid()
                self.cbb_data_type.grid()

            if(self.cbb_data_type.get() == self.data_types[2]):
                self.lbl_name_value.grid()
                self.txt_name_value.grid()

                self.lbl_value.place(x = 108, y = 82)
                self.txt_value.config(width = 25)
                self.txt_value.grid(column = 1, columnspan = 2, row = 5, padx = 5, pady = 0)

                self.txt_seperator.grid_remove()

                self.lbl_data_type.grid()
                self.cbb_data_type.grid()

            if(self.cbb_data_type.get() == self.data_types[3]):
                self.lbl_name_value.grid()
                self.txt_name_value.grid()

                self.lbl_value.place(x = 108, y = 82)
                self.txt_value.config(width = 25)
                self.txt_value.grid(column = 1, columnspan = 2, row = 5, padx = 5, pady = 0)

                self.txt_seperator.grid_remove()

                self.lbl_data_type.grid()
                self.cbb_data_type.grid()

            if(self.cbb_data_type.get() == self.data_types[4]):
                self.lbl_name_value.grid()
                self.txt_name_value.grid()

                self.lbl_value.place(x = 108, y = 82)
                self.txt_value.config(width = 19)
                self.txt_value.grid(column = 1, columnspan = 1, row = 5, padx = 5, pady = 0)

                self.txt_seperator.grid(column = 2, row = 5, padx = 5, pady = 0)

                self.lbl_data_type.grid()
                self.cbb_data_type.grid()

            if(self.cbb_data_type.get() == self.data_types[5]):
                self.lbl_name_value.grid()
                self.txt_name_value.grid()

                self.lbl_value.place(x = 108, y = 82)
                self.txt_value.config(width = 25)
                self.txt_value.grid(column = 1, columnspan = 2, row = 5, padx = 5, pady = 0)

                self.txt_seperator.grid_remove()

                self.lbl_data_type.grid()
                self.cbb_data_type.grid()

        self.cbb_data_type.bind('<<ComboboxSelected>>', data_type_changed)

        self.lbl_result = tk.Label(self.frame_edit_directly, text = lb.REGISTRY_LBL_RESULT)
        self.lbl_result.place(x = 4, y = 130)

        self.result_area = st.ScrolledText(self.frame_edit_directly, wrap = tk.WORD, width = 46, height = 10, bg = "gray92", state = tk.DISABLED)
        self.result_area.place(x = 4, y = 150)

        self.btn_send_direct_stt = tk.StringVar(value = lb.REGISTRY_SEND_DIRECT)
        self.btn_send_direct = tk.Button(self.frame_edit_directly, textvariable=self.btn_send_direct_stt, width = 8, command = self.send_command)
        self.btn_send_direct.place(x = 100, y = 320)
        self.btn_clear = tk.Button(self.frame_edit_directly, text = lb.REGISTRY_CLEAR, width = 8, command = self.clear_log)
        self.btn_clear.place(x = 220, y = 320)

    def browse(self):
        try:
            filename = askopenfilename(defaultextension=".reg", filetypes=[("Registry Files", "*.reg"), ("All Files", "*.*")], parent = self)
            self.txt_path_input.config(state = 'normal')
            self.txt_path_input.delete(0, tk.END)
            self.txt_path_input.insert(-1, filename)
            self.txt_path_input.config(state = 'readonly')

            f = open(filename, 'r', encoding = "utf-16")
            data = f.read()
            f.close()
        except:
            data = lb.REGISTRY_ERR_READ_FILE

        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.INSERT, data)

    def send_reg(self):
        if self.btn_send_stt.get() == lb.REGISTRY_SEND:
            file_data = self.text_area.get(1.0, tk.END)
            self.socket_cmd('merge-reg-file', file_data)
            self.btn_send_stt.set(lb.REGISTRY_WAIT)
    
    def query_reg_value(self):
        path = self.txt_path_input_direct.get()
        value = self.txt_name_value.get()

        self.socket_cmd('query-reg-value', path, value)
        self.btn_send_direct_stt.set(lb.REGISTRY_WAIT)

    def parse_reg_value(self, data, type):
        if type == 'Binary':
            data = bytearray.fromhex(data)
        elif type == 'DWORD' or type == 'QWORD':
            data = int(data)
        elif type == 'Multi-String':
            data = data.split(self.txt_seperator.get())

        return data

    def set_reg_value(self):
        path = self.txt_path_input_direct.get()
        value = self.txt_name_value.get()
        type = self.cbb_data_type.get()
        data = self.txt_value.get()
        try:
            data = self.parse_reg_value(data, type)
        except:
            showerror(lb.ERR, lb.REGISTRY_ERR_PARSE_DATA)
            return

        self.socket_cmd('set-reg-value', path, value, type, data)
        self.btn_send_direct_stt.set(lb.REGISTRY_WAIT)

    def delete_reg_value(self):
        path = self.txt_path_input_direct.get()
        value = self.txt_name_value.get()
        self.socket_cmd('delete-reg-value', path, value)
        self.btn_send_direct_stt.set(lb.REGISTRY_WAIT)

    def create_reg_key(self):
        path = self.txt_path_input_direct.get()
        self.socket_cmd('create-reg-key', path)
        self.btn_send_direct_stt.set(lb.REGISTRY_WAIT)

    def delete_reg_key(self):
        path = self.txt_path_input_direct.get()
        self.socket_cmd('delete-reg-key', path)
        self.btn_send_direct_stt.set(lb.REGISTRY_WAIT)

    
    def send_command(self):
        if self.btn_send_direct_stt.get() == lb.REGISTRY_SEND_DIRECT:
            if self.cbb_option.get() == self.options[0]:
                self.query_reg_value()
            elif self.cbb_option.get() == self.options[1]:
                self.set_reg_value()
            elif (self.cbb_option.get() == self.options[2]):
                self.delete_reg_value()   
            elif (self.cbb_option.get() == self.options[3]):
                self.create_reg_key()   
            elif (self.cbb_option.get() == self.options[4]):
                self.delete_reg_key()
            
    def clear_log(self):
        self.result_area.config(state = 'normal')
        self.result_area.delete(1.0, tk.END)
        self.result_area.config(state = 'disabled')

    def write_log(self, data):
        self.result_area.config(state='normal')
        self.result_area.insert(tk.INSERT, data + '\n')
        self.result_area.config(state='disabled')
        self.result_area.see('end')

    def update_ui(self, task):
        cmd, ext = task

        if cmd == 'merge':
            if ext == 'ok':
                showinfo(lb.REGISTRY_MERGE, lb.REGISTRY_MERGE_OK, parent = self)
            else:
                showerror(lb.REGISTRY_MERGE, lb.REGISTRY_MERGE_ERR, parent = self)
            self.btn_send_stt.set(lb.REGISTRY_SEND)

        else:
            if cmd == 'query':
                value, data, type = ext

                if data is None:
                    self.write_log(f'{value}: Query error')
                else:
                    self.write_log(f'{value}: {data}\n\tType: {type}')

            elif cmd == 'set-value':
                if ext == 'ok':
                    self.write_log(lb.REGISTRY_SET_VALUE_OK)
                else:
                    self.write_log(lb.REGISTRY_SET_VALUE_ERR)

            elif cmd == 'delete-value':
                if ext == 'ok':
                    self.write_log(lb.REGISTRY_DELETE_VALUE_OK)
                else:
                    self.write_log(lb.REGISTRY_DELETE_VALUE_ERR)

            elif cmd == 'create-key':
                if ext == 'ok':
                    self.write_log(lb.REGISTRY_CREATE_KEY_OK)
                else:
                    self.write_log(lb.REGISTRY_CREATE_KEY_ERR)

            elif cmd == 'delete-key':
                if ext == 'ok':
                    self.write_log(lb.REGISTRY_DELETE_KEY_OK)
                else:
                    self.write_log(lb.REGISTRY_DELETE_KEY_ERR)

            self.btn_send_direct_stt.set(lb.REGISTRY_SEND_DIRECT)
