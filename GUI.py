from tkinter import *
from PIL import ImageTk, Image

def func_connect(window_name):
    lbl_IP_input = Label(window_name, text="IP: ", fg="black")
    lbl_IP_input.grid(column=0, row=0)

    txt_IP_input = Entry(window_name,width=20)
    txt_IP_input.focus()
    txt_IP_input.grid(column=1, row=0)

    def clicked_connect():
        return

    btn_connect = Button(window_name, text="Connect", command=clicked_connect)
    btn_connect.grid(column=2, row=0)

def func_screenshot(window_name):
    def clicked_screenshot():
        window_screenshot=Tk()
        window_screenshot.title("Screenshot")
        window_screenshot.geometry('300x200')
        cvs_screenshot=Canvas(window_screenshot, width = 300, height = 300)
        cvs_screenshot.pack()
        img = ImageTk.PhotoImage(Image.open("water.png"))
        cvs_screenshot.create_image(20, 20, anchor=NW, image=img)  
        window_screenshot.mainloop()
    
    btn_screenshot=Button(window_name, text="Screenshot", width=20, height=2, command=clicked_screenshot)
    btn_screenshot.grid(column=1, row=2)

def func_process_running(window_name):
    def clicked_process_running():
        return
    
    btn_process_running=Button(window_name, text="Process running", width=20, height=2, command=clicked_process_running)
    btn_process_running.grid(column=1, row=3)

def func_app_running(window_name):
    def clicked_app_running():
        return
    
    btn_app_running=Button(window_name, text="App running", width=20, height=2, command=clicked_app_running)
    btn_app_running.grid(column=1, row=4)

def func_keystroke(window_name):
    def clicked_keystroke():
        return
    
    btn_keystroke=Button(window_name, text="Keystroke", width=20, height=2, command=clicked_keystroke)
    btn_keystroke.grid(column=1, row=5)

def func_edit_registry(window_name):
    def clicked_edit_registry():
        return
    
    btn_edit_registry=Button(window_name, text="Edit registry", width=20, height=2, command=clicked_edit_registry)
    btn_edit_registry.grid(column=1, row=6)

def func_shutdown(window_name):
    def clicked_shutdown():
        return
    
    btn_shutdown=Button(window_name, text="Shutdown", width=20, height=2, command=clicked_shutdown)
    btn_shutdown.grid(column=1, row=7)

def func_exit(window_name):
    def clicked_exit():
        window_name.destroy()
    
    btn_exit=Button(window_name, text="Exit", width=20, height=2, command=clicked_exit)
    btn_exit.grid(column=1, row=8)

def GUI_client():
    window_client = Tk()
    window_client.title("Client")
    window_client.geometry('240x330')

    func_connect(window_client)
    func_screenshot(window_client)
    func_process_running(window_client)
    func_app_running(window_client)
    func_keystroke(window_client)
    func_edit_registry(window_client)
    func_shutdown(window_client)
    func_exit(window_client)

    window_client.mainloop()

def main():
    GUI_client()

if __name__ == "__main__":
    main()