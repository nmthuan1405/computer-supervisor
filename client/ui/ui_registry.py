import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as st
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter.messagebox import showerror, showinfo

import ui.label as lb
import ui.constraints as const
import queue

class UI_Registry(tk.Toplevel):
    def __init__(self, parent):
        self.ui_queue = queue.Queue()
        self.socket_queue = None

        super().__init__(parent)
        self.title = lb.REGISTRY_TITLE
        self.geometry('430x637')
        self.resizable(False, False)
        self['padx'] = const.WINDOW_BORDER_PADDING
        self['pady'] = const.WINDOW_BORDER_PADDING
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.lbl_pathInput = tk.Label(self, text = "Path")
        self.lbl_pathInput.grid(column = 0, row = 0, sticky = tk.SW)

        self.txt_pathInput = tk.Entry(self, width = 53)
        self.txt_pathInput.grid(column = 0, row = 1)
        self.txt_pathInput['state'] = 'readonly'

        self.btn_browse = tk.Button(self, text="Browse", command = self.browse)
        self.btn_browse.grid(column = 1, row = 1, padx = 4, ipadx = 10, sticky = tk.E)

        self.lbl_data = tk.Label(self, text = "Data")
        self.lbl_data.grid(column = 0, row = 2, sticky = tk.SW)

        self.text_area = st.ScrolledText(self, wrap = tk.WORD, width = 38, height = 10)
        self.text_area.grid(column = 0, row = 3)

        self.btn_send = tk.Button(self, text="Send", command = self.sendReg)
        self.btn_send.grid(column = 1, row = 3, padx = 4, ipadx = 15, ipady = 70, sticky = tk.E)

        self.frame_editDirectly = tk.LabelFrame(self, text = "Edit value directly", relief = tk.RIDGE)
        self.frame_editDirectly.place(x = 3, y = 245, height = 370)

        self.lbl_option = tk.Label(self.frame_editDirectly, text = "Select option")
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

                self.lbl_value.place_forget()
                self.txt_value.grid_remove()

                self.txt_seperator.grid_remove()

                self.lbl_dataType.grid_remove()
                self.cbb_dataType.grid_remove()

            if(self.cbb_option.get() == self.options[1]):
                self.lbl_nameValue.grid()
                self.txt_nameValue.grid()

                self.lbl_value.place(x = 108, y = 82)
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

                self.lbl_value.place_forget()
                self.txt_value.grid_remove()

                self.txt_seperator.grid_remove()

                self.lbl_dataType.grid_remove()
                self.cbb_dataType.grid_remove()

            if(self.cbb_option.get() == self.options[3]):
                self.lbl_nameValue.grid_remove()
                self.txt_nameValue.grid_remove()

                self.lbl_value.place_forget()
                self.txt_value.grid_remove()

                self.txt_seperator.grid_remove()

                self.lbl_dataType.grid_remove()
                self.cbb_dataType.grid_remove()

            if(self.cbb_option.get() == self.options[4]):
                self.lbl_nameValue.grid_remove()
                self.txt_nameValue.grid_remove()

                self.lbl_value.place_forget()
                self.txt_value.grid_remove()

                self.txt_seperator.grid_remove()

                self.lbl_dataType.grid_remove()
                self.cbb_dataType.grid_remove()

        self.cbb_option.bind('<<ComboboxSelected>>', optionChanged)

        self.lbl_pathInput2 = tk.Label(self.frame_editDirectly, text = "Path")
        self.lbl_pathInput2.grid(column = 0, row = 2, padx = 2, pady = 0, sticky = tk.SW)

        self.txt_pathInput2 = tk.Entry(self.frame_editDirectly, width = 64)
        self.txt_pathInput2.grid(column = 0, row = 3, columnspan = 4, padx = 5)

        self.lbl_nameValue = tk.Label(self.frame_editDirectly, text = "Name Value")
        self.lbl_nameValue.grid(column = 0, row = 4, padx = 2, pady = 0, sticky = tk.SW)

        self.txt_nameValue = tk.Entry(self.frame_editDirectly, width = 15)
        self.txt_nameValue.grid(column = 0, row = 5, padx = 5, pady = 0, sticky = tk.W)

        self.lbl_value = tk.Label(self.frame_editDirectly, text = "Value")

        self.txt_value = tk.Entry(self.frame_editDirectly, width = 25)

        self.txt_seperator = tk.Entry(self.frame_editDirectly, width = 3, justify = 'center')
        self.txt_seperator.insert(-1, '\\0')

        self.lbl_dataType = tk.Label(self.frame_editDirectly, text = "Data type")

        self.dataTypes = ('String', 'Binary', 'DWORD', 'QWORD', 'Multi-String', 'Expandable String')
        self.selected_dataType = tk.StringVar()
        self.cbb_dataType = ttk.Combobox(self.frame_editDirectly, width = 16, textvariable = self.selected_dataType)
        self.cbb_dataType['values'] = self.dataTypes
        self.cbb_dataType.current(0)
        self.cbb_dataType['state'] = 'readonly'  # normal

        def dataTypeChanged(event):
            if(self.cbb_dataType.get() == self.dataTypes[0]):
                self.lbl_nameValue.grid()
                self.txt_nameValue.grid()

                self.lbl_value.place(x = 108, y = 82)
                self.txt_value.config(width = 25)
                self.txt_value.grid(column = 1, columnspan = 2, row = 5, padx = 5, pady = 0)

                self.txt_seperator.grid_remove()

                self.lbl_dataType.grid()
                self.cbb_dataType.grid()
            
            if(self.cbb_dataType.get() == self.dataTypes[1]):
                self.lbl_nameValue.grid()
                self.txt_nameValue.grid()

                self.lbl_value.place(x = 108, y = 82)
                self.txt_value.config(width = 25)
                self.txt_value.grid(column = 1, columnspan = 2, row = 5, padx = 5, pady = 0)

                self.txt_seperator.grid_remove()

                self.lbl_dataType.grid()
                self.cbb_dataType.grid()

            if(self.cbb_dataType.get() == self.dataTypes[2]):
                self.lbl_nameValue.grid()
                self.txt_nameValue.grid()

                self.lbl_value.place(x = 108, y = 82)
                self.txt_value.config(width = 25)
                self.txt_value.grid(column = 1, columnspan = 2, row = 5, padx = 5, pady = 0)

                self.txt_seperator.grid_remove()

                self.lbl_dataType.grid()
                self.cbb_dataType.grid()

            if(self.cbb_dataType.get() == self.dataTypes[3]):
                self.lbl_nameValue.grid()
                self.txt_nameValue.grid()

                self.lbl_value.place(x = 108, y = 82)
                self.txt_value.config(width = 25)
                self.txt_value.grid(column = 1, columnspan = 2, row = 5, padx = 5, pady = 0)

                self.txt_seperator.grid_remove()

                self.lbl_dataType.grid()
                self.cbb_dataType.grid()

            if(self.cbb_dataType.get() == self.dataTypes[4]):
                self.lbl_nameValue.grid()
                self.txt_nameValue.grid()

                self.lbl_value.place(x = 108, y = 82)
                self.txt_value.config(width = 19)
                self.txt_value.grid(column = 1, columnspan = 1, row = 5, padx = 5, pady = 0)

                self.txt_seperator.grid(column = 2, row = 5, padx = 5, pady = 0)

                self.lbl_dataType.grid()
                self.cbb_dataType.grid()

            if(self.cbb_dataType.get() == self.dataTypes[5]):
                self.lbl_nameValue.grid()
                self.txt_nameValue.grid()

                self.lbl_value.place(x = 108, y = 82)
                self.txt_value.config(width = 25)
                self.txt_value.grid(column = 1, columnspan = 2, row = 5, padx = 5, pady = 0)

                self.txt_seperator.grid_remove()

                self.lbl_dataType.grid()
                self.cbb_dataType.grid()

        self.cbb_dataType.bind('<<ComboboxSelected>>', dataTypeChanged)

        self.lbl_result = tk.Label(self.frame_editDirectly, text = "Result")
        self.lbl_result.place(x = 4, y = 130)

        self.result_area = st.ScrolledText(self.frame_editDirectly, wrap = tk.WORD, width = 46, height = 10, bg = "gray92", state = tk.DISABLED)
        self.result_area.place(x = 4, y = 150)

        self.button1 = ttk.Button(self.frame_editDirectly, text="Send", command = self.sendCommand)
        self.button1.place(x = 100, y = 320)
        self.button2 = ttk.Button(self.frame_editDirectly, text="Clear log", command = self.clearLog)
        self.button2.place(x = 220, y = 320)

        self.after(const.UPDATE_TIME, self.periodic_call)

    def browse(self):
        try:
            filename = askopenfilename(defaultextension=".reg", filetypes=[("Registry Files", "*.reg"), ("All Files", "*.*")], parent = self)
            self.txt_pathInput.config(state = 'normal')
            self.txt_pathInput.delete(0, tk.END)
            self.txt_pathInput.insert(-1, filename)
            self.txt_pathInput.config(state = 'readonly')

            f = open(filename, 'r', encoding = "utf-16")
            data = f.read()
            f.close()
        except:
            data = 'ERROR'

        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.INSERT, data)

    def sendReg(self):
        # if self.service.sendRegFile(self.text_area.get(1.0, tk.END)) == 'OK':
        #     showinfo('Success', 'Merge registry successfully', parent = self)
        # else:
            showerror('Error', 'Unable to merge registry', parent = self)

    def sendCommand(self):
        # if self.cbb_option.get() == self.options[0]:
        #     data = self.service.sendRegGetVal(self.txt_pathInput2.get(), self.txt_nameValue.get())
        #     if (len(data) == 2):

        #         if data[1] == self.dataTypes[1]:
        #             dataDisplay = str(data[0].hex())
        #         else:
        #             dataDisplay = str(data[0])

        #         self.writeLog(self.txt_nameValue.get() + ': ' + dataDisplay)
        #         self.writeLog('\t\tType: ' + data[1])
        #     else:
        #         self.writeLog(self.txt_nameValue.get() + ': Error')

        # elif self.cbb_option.get() == self.options[1]:
        #     data = self.txt_value.get()
        #     type = self.cbb_dataType.get()

        #     try:
        #         if type == self.dataTypes[1]:
        #             data = bytearray.fromhex(data)
        #         elif type == self.dataTypes[2] or type == self.dataTypes[3]:
        #             data = int(data)
        #         elif type == self.dataTypes[4]:
        #             data = data.split(self.txt_seperator.get())

        #             dataDisplay = ['\'' + element + '\'' for element in data]
        #             self.writeLog('Data: ' + ', '.join(dataDisplay))
        #     except:
        #         self.writeLog('Unable to parse data')
        #         return

        #     if self.service.sendRegSetVal(self.txt_pathInput2.get(), self.txt_nameValue.get(), data, type) == 'OK':
        #         self.writeLog('Set value successfully')
        #     else:
        #         self.writeLog('Unable to set value')

        # elif (self.cbb_option.get() == self.options[2]):
        #     if self.service.sendRegDeVal(self.txt_pathInput2.get(), self.txt_nameValue.get()) == 'OK':
        #         self.writeLog('Delete value successfully')
        #     else:
        #         self.writeLog('Unable to delete value')
            
        # elif (self.cbb_option.get() == self.options[3]):
        #     if self.service.sendRegCreateKey(self.txt_pathInput2.get()) == 'OK':
        #         self.writeLog('Create key successfully')
        #     else:
        #         self.writeLog('Unable to create key')
            
        # elif (self.cbb_option.get() == self.options[4]):
        #     if self.service.sendRegDelKey(self.txt_pathInput2.get()) == 'OK':
        #         self.writeLog('Delete key successfully')
        #     else:
                self.writeLog('Unable to delete key')
            
    def clearLog(self):
        self.result_area.config(state = 'normal')
        self.result_area.delete(1.0, tk.END)
        self.result_area.config(state = 'disabled')

    def writeLog(self, data):
        self.result_area.config(state='normal')
        self.result_area.insert(tk.INSERT, data + '\n')
        self.result_area.config(state='disabled')
        self.result_area.see('end')

    def update_ui(self, task):
        DEBUG("task", task)
        cmd, ext = task

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