import tkinter
from tkinter import *
from PIL import ImageTk, Image
import client

buff = None
#window_name: biến giữ cửa sổ window tên name
#func_name: chức năng tên name
#lbl_name: label hiển thị chữ ra cửa sổ
#txt_name: textbox để nhập text vào
#btn_name: button để bấm

#hàm tạo GUI khi nhấn button connect
def GUI_connect():
    window_connect=Tk()                     #tạo cửa sổ mới
    window_connect.title("Connect status")  #tên cửa sổ
    window_connect.geometry('300x200')      #kính thước ngang x dọc
    window_connect.mainloop()

#hàm chức năng connect, tham số là cửa sổ window_name
def func_connect(window_name):
    #hàm gọi tạo GUI connect
    def clicked_connect():
        global buff
        buff = client.connectServer('temp')
        # GUI_connect()

    lbl_IP_input = Label(window_name, text = "IP: ")  #label "IP: " ở cửa sổ window_name
    lbl_IP_input.grid(column = 0, row = 0)              #đặt ở cột 0 dòng 0

    txt_IP_input = Entry(window_name, width = 20)      #textbox để nhập địa chỉ IP
    txt_IP_input.focus()                            #con trỏ chuột trỏ sẵn vào textbox khi chạy
    txt_IP_input.grid(column = 1, row = 0)              #đặt ở cột 1 dòng 0

    btn_connect = Button(window_name, text="Connect", command = clicked_connect)  #bấm button connect sẽ gọi hàm clicked_connect
    btn_connect.grid(column=2, row=0)

def GUI_screenshot():
    window_screenshot = Tk()
    window_screenshot.title("Screenshot")
    window_screenshot.geometry('1000x1000')
    image = client.getScreenShot(buff)
    image.show()

    render = ImageTk.PhotoImage(image)
    label1 = Label(image = render)
    label1.image = render
    label1.place(x=0, y=0)

    window_screenshot.mainloop()

def func_screenshot(window_name):
    def clicked_screenshot():
        GUI_screenshot()
    
    btn_screenshot = Button(window_name, text="Screenshot", width=20, height=2, command=clicked_screenshot)
    btn_screenshot.grid(column = 1, row = 2)

def GUI_process_running():
    window_process_running=Tk()
    window_process_running.title("Process running")
    window_process_running.geometry('320x200')

    def clicked_kill():
        return
    btn_kill=Button(window_process_running, text="Kill", width=10, height=2, command=clicked_kill)
    btn_kill.grid(column=0, row=0)
    def clicked_show():
        return
    btn_show=Button(window_process_running, text="Show", width=10, height=2, command=clicked_show)
    btn_show.grid(column=1, row=0)
    def clicked_hide():
        return
    btn_hide=Button(window_process_running, text="Hide", width=10, height=2, command=clicked_hide)
    btn_hide.grid(column=2, row=0)
    def clicked_start():
        return
    btn_start=Button(window_process_running, text="Start", width=10, height=2, command=clicked_start)
    btn_start.grid(column=3, row=0)

    window_process_running.mainloop()

def func_process_running(window_name):
    def clicked_process_running():
        GUI_process_running()
    
    btn_process_running=Button(window_name, text="Process running", width=20, height=2, command=clicked_process_running)
    btn_process_running.grid(column=1, row=3)

def GUI_app_running():
    window_app_running=Tk()
    window_app_running.title("App running")
    window_app_running.geometry('300x200')
    window_app_running.mainloop()

def func_app_running(window_name):
    def clicked_app_running():
        GUI_app_running()
    
    btn_app_running=Button(window_name, text="App running", width=20, height=2, command=clicked_app_running)
    btn_app_running.grid(column=1, row=4)

def GUI_keystroke():
    window_keystroke=Tk()
    window_keystroke.title("Keystroke")
    window_keystroke.geometry('300x200')
    window_keystroke.mainloop()

def func_keystroke(window_name):
    def clicked_keystroke():
        GUI_keystroke()
    
    btn_keystroke=Button(window_name, text="Keystroke", width=20, height=2, command=clicked_keystroke)
    btn_keystroke.grid(column=1, row=5)

def GUI_edit_registry():
    window_edit_registry=Tk()
    window_edit_registry.title("Edit registry")
    window_edit_registry.geometry('300x200')
    window_edit_registry.mainloop()

def func_edit_registry(window_name):
    def clicked_edit_registry():
        GUI_edit_registry()
    
    btn_edit_registry=Button(window_name, text="Edit registry", width=20, height=2, command=clicked_edit_registry)
    btn_edit_registry.grid(column=1, row=6)

def GUI_shutdown():
    window_shutdown=Tk()
    window_shutdown.title("Shutdown")
    window_shutdown.geometry('300x200')
    window_shutdown.mainloop()

def func_shutdown(window_name):
    def clicked_shutdown():
        GUI_shutdown()
    
    btn_shutdown=Button(window_name, text="Shutdown", width=20, height=2, command=clicked_shutdown)
    btn_shutdown.grid(column=1, row=7)

def func_exit(window_name):
    def clicked_exit():
        window_name.destroy()   #đóng cửa sổ window_name
    
    btn_exit=Button(window_name, text="Exit", width=20, height=2, command=clicked_exit)
    btn_exit.grid(column=1, row=8)

def GUI_client():
    window_client = Tk()
    window_client.title("Client")
    window_client.geometry('240x330')

    #gọi các hàm chức năng của client
    func_connect(window_client)         #tham số là cửa sổ window_client
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