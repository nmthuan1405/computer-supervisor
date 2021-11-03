from services.Socket import Socket
import socket
import threading
import queue

PORT = 1234

class Client(Socket, threading.Thread):
    def __init__(self, DELIM=b'\x00'):
        Socket.__init__(self, socket= None, DELIM=DELIM)
        threading.Thread.__init__(self, name="client")

        self.ui_queue = None
        self.socket_queue = queue.Queue()

    def add_ui_queue(self, ui_queue):
        self.ui_queue = ui_queue
    
    def ui_cmd(self, cmd, ext = None, ui='main'):
        self.ui_queue[ui].put((cmd, ext))

    def start_socket(self, SERVER):
        self.socket = socket.socket()
        self.socket.connect((SERVER, PORT))

    def stop_socket(self):
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()
        except:
            pass

    def task_start(self, ip):
        try:
            self.start_socket(ip)
        except:
            self.ui_cmd("err", "cannot start")
            self.ui_cmd("start")
        else:
            self.ui_cmd("stop")

    def task_stop(self):
        try:
            self.send_str("close")
            self.stop_socket()
        except:
            DEBUG("ERR when stop socket")
        finally:
            self.ui_cmd("start")
    
    def task_update_stream(self, size):
        self.send_str("screen-stream")
        self.send_obj(size)

        img = self.recv_obj()
        self.ui_cmd("update-stream", img,'screen')

    def task_capture_stream(self):
        self.send_str("screen-capture")

        img = self.recv_obj()
        DEBUG("received screenshot")
        self.ui_cmd("save-image", img,'screen')

    def task_keyboard_start(self):
        self.send_str("listener-start")

    def task_keyboard_stop(self):
        self.send_str("listener-stop")

    def task_hook(self):
        self.send_str("listener-hook")

    def task_unhook(self):
        self.send_str("listener-unhook")

    def task_log_clear(self):
        self.send_str("listener-clear")

    def task_log_get(self):
        self.send_str("listener-get")
        self.ui_cmd("update-log", self.recv_str(), "keyboard")

    def task_keyboard_block(self):
        self.send_str("listener-block")

    def task_keyboard_unblock(self):
        self.send_str("listener-unblock")

    def task_update_dir(self, dir):
        self.send_str("get-dir")
        self.send_str(dir)

        self.ui_cmd("update-dir", self.recv_obj(), "file")

    def task_get_MAC(self):
        self.send_str("get-MAC")
        self.ui_cmd("update-MAC", self.recv_str(), "main")

    def task_send_logout(self):
        self.send_str("logout")

    def task_send_shutdown(self):
        self.send_str("shutdown")

    def task_send_restart(self):
        self.send_str("restart")

    def run(self):
        while True:
            task = self.socket_queue.get()
            DEBUG("task", task)

            cmd, ext = task
            if cmd == "exit":
                break
            elif cmd == "start":
                self.task_start(ext)
            elif cmd == "stop":    
                self.task_stop()
            elif cmd == "update-stream":
                self.task_update_stream(ext)
            elif cmd == "capture-stream":
                self.task_capture_stream()
            elif cmd == 'listener-start':
                self.task_keyboard_start()
            elif cmd == 'listener-stop':
                self.task_keyboard_stop()
            elif cmd == "listener-hook":
                self.task_hook()
            elif cmd == "listener-unhook":
                self.task_unhook()
            elif cmd == "listener-clear":
                self.task_log_clear()
            elif cmd == "listener-get":
                self.task_log_get()
            elif cmd == 'listener-block':
                self.task_keyboard_block()
            elif cmd == 'listener-unblock':
                self.task_keyboard_unblock()
            elif cmd == "update-dir":
                self.task_update_dir(ext)
            elif cmd == "get-MAC":
                self.task_get_MAC()
            elif cmd == "logout":
                self.task_send_logout()
            elif cmd == "shutdown":
                self.task_send_shutdown()
            elif cmd == "restart":
                self.task_send_restart()

def DEBUG(*args,**kwargs):
    print("Client:", *args,**kwargs)