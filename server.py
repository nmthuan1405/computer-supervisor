from tkinter import *


class GUI(Frame):


    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        self.master = master
        self.my_frame = Frame(self.master)
        self.my_frame.pack()

        self.button1 = Button(self.master, text="Open New Window", command = self.open_toplevel_window)
        self.button1.pack()

        self.text = Text(self.master, width = 20, height = 3)
        self.text.pack()
        self.text.insert(END, "Before\ntop window\ninteraction")

    def open_toplevel_window(self):
        self.top = Toplevel(self.master)                                                                                            
        #this forces all focus on the top level until Toplevel is closed
        self.top.grab_set() 

        def replace_text():
            self.text.delete(1.0, END)
            self.text.insert(END, "Text From\nToplevel")

        top_button = Button(self.top, text = "Replace text in main window",
                            command = replace_text)
        top_button.pack()


if __name__ == "__main__":
    root = Tk()
    app = GUI(root)
    root.mainloop()